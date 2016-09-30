/*
 *	JS for the app
 *
 *	@author rob.dunne@manchester.ac.uk
 *	August 2016
 *
 */

// Angular controllers
var etaApp = angular.module('etaApp', ['ui.grid']);

etaApp.controller('appController', ['$scope', function($scope) {
  // Set the vars / models
  $scope.datasetsList = [];
  $scope.datagrid = {
    'data': [],
    'columnDefs': [],
    'selected': 0
  };
  $scope.modulesList = [];
  $scope.analysisOutput = '';

  // Fetch any existing datasets from the database
  db.find({ filename: /./ }, function(err, doc) {
      if(doc.length > 0) {
        $scope.nodatasets = false;

        for(var i=0;i<doc.length;i++) {
          $scope.datasetsList.unshift(doc);
          $scope.$apply();
        }
      } else {
        console.log('No datasets to load.');
      }
  });

  // Get the available analysis modules
  try {
    var py = require('child_process').spawn('python3', ['apioptions.py']);
    var dataString = '';

    py.stdout.on('data', function(data) {
      dataString += data.toString();
    });

    py.stdout.on('end', function() {
      var json = JSON.parse(dataString);
      //console.log(json);
      $scope.modulesList = json;
      $scope.$apply();
    });
  } catch(error) {
    console.log(error);
  }

  // Kill the python process once done
  py.kill('SIGINT');

  // Notification message
  $scope.notifyUser = function(titleText, bodyText) {
    if(window.Notification && Notification.permission !== "denied") {
    	Notification.requestPermission(function(status) {
    		var n = new Notification(titleText, {
    			body: bodyText
    		});
    	});
    }
  }

  // Open a file
  $scope.openFile = function() {
    var options = {
      filters: [
        {name: 'Custom File Type', extensions: ['csv', 'tsv']}
      ]
    };
    dialog.showOpenDialog(options, function(filepath) {
       if(filepath === undefined){
            console.log("No file selected");
       } else {
            $scope.readFile(filepath[0]);
       }
    });
  }

  // Read a file
  $scope.readFile = function(filepath) {
    fs.readFile(filepath, 'utf-8', function (err, data) {
          // Notify the user if there's an error
          if(err){
              notifyUser('Error', "An error ocurred reading the file :" + err.message);
              return;
          }

          // Get the filename from the path
          var filename = filepath.replace(/^.*[\\\/]/, '');

          // Save the file content
          $scope.saveFile(filename, data);
    });
  }

  // Save a file to the database
  $scope.saveFile = function(filename, csvData) {
    // Show a loading bar while parsing
    NProgress.start();

    csv.parse(csvData, function(err, csvArray) {
      // Parse the data into a CSV array of objects
      var csvJSON = [];
      var csvRows = csvArray.length-1;

      // Process the data
      var worker = new Worker("../assets/js/process-dataset.js");
      worker.postMessage(JSON.stringify(csvArray));
      worker.onmessage = function(event){
        csvJSON = JSON.parse(event.data);

        var newData = {
          'timestamp': moment().format('DD-MM-YYYY HH:mm:ss'),
          'filename': filename,
          'analysis': {},
          'data': csvJSON,
          'rows': csvRows,
          'rawdata': csvData,
          'modified': {}
        };

        db.insert(newData, function(err, doc) {
          $scope.notifyUser('New dataset', doc.filename+' added to available data.');
          console.log('Inserted', doc.filename, 'with ID', doc._id);

          // Append to datasetslist
          $scope.datasetsList.unshift(doc);
          $scope.$apply();

          // Complete loading bar
          NProgress.done();

          // Load it into the dataset viewer
          $scope.viewData(doc._id, 0);
        });
      };
    });
  }

  // Load the dataset into the dataset viewer
  $scope.viewData = function(id, index) {
    // Highlight the row
    $scope.datagrid.selected = index;

    // Reset the datagrid
    $scope.datagrid.columnDefs = [];
    $scope.datagrid.data = [];

    // Load some data
    db.findOne({ _id: id }, function(err, doc) {
      //console.log(err);

      // Display the data in a table
      $scope.datagrid.data = doc.data;
      $scope.$apply();
    });
  }

  // Add updated file data to the database (to the 'modified' object key)
  $scope.updatedFileData = function() {

  }

  // The selected analysis options
  $scope.updateAnalysisOptions = function() {
    console.log($scope.selectedDataset);
    console.log($scope.selectedAnalysis);
  }

  $scope.analyseDataset = function() {
    if($scope.selectedAnalysis.length > 0 && $scope.selectedDataset.length > 0 ) {
      $scope.analysisOutput += '> Analysing dataset ID:'+$scope.selectedDataset+' using '+$scope.selectedAnalysis+' module...\n';
      //$scope.analysisOutput += '> Output from analysis: \n';

      var dataString = '';
      var json = {};
      var analysis = $scope.selectedAnalysis;
      var fileID = $scope.selectedDataset;
      var analysisData = ''

      // Get the data
      db.findOne({ _id: fileID }, function(err, doc) {
        // Call the python API
        try {
          var py = require('child_process').spawn('python3', ['api.py', analysis]);
        } catch(error) {
          console.log(error);
        }

        // Get the output data from the python API
        py.stdout.on('data', function(data) {
          // Update the output
          /*
          var message = data.toString();
          message = message.replace(/(?:\r\n|\r|\n)/g, '\n> ');
          $scope.analysisOutput += '> '+message+'\n';
          $scope.$apply();
          */

          analysisData += data.toString();

          // Post update message and scroll down
          $scope.analysisOutput += '> Fetching analysis output: \n\n';
          $scope.analysisOutput += analysisData+'\n\n';
          $scope.$apply();

          var elem = document.getElementById('eta-data-analysis-output-text');
          elem.scrollTop = elem.scrollHeight;
        });

        // When the python API output has finished
        py.stdout.on('end', function() {
          // Update the output
          $scope.analysisOutput += '> Analysis complete. Saving to database.\n';
          $scope.$apply();

          // Scroll down
          var elem = document.getElementById('eta-data-analysis-output-text');
          elem.scrollTop = elem.scrollHeight;

          // Save the processed data in the database
          db.update({ id: fileID }, { $set: { analysis: analysisData } }, { multi: true }, function (err, numReplaced) {
            console.log('DB updated with analysis.');
            //console.log('Data: '+analysisData);

            // Update the output
            $scope.analysisOutput += '> Database updated with analysis.\n';
            $scope.analysisOutput += '> Processed data now available for data visualisation.\n>\n';
            $scope.$apply();
          });

          // Show an update message
          $scope.notifyUser('Data Analysis Update', 'Analysis complete for '+fileID);
        });

        // Send data to the API
        py.stdin.write(JSON.stringify(doc.rawdata));
        py.stdin.end();

        // Kill the python process once done
        py.kill('SIGINT');
      });
    }
  }
}]);
