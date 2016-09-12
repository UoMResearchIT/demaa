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

          // Save the file content
          var filename = filepath.replace(/^.*[\\\/]/, '');
          $scope.saveFile(filename, data);
    });
  }

  // Save a file to the database
  $scope.saveFile = function(filename, csvData) {
    console.log('Saving '+filename);

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
          'data': csvJSON,
          'rows': csvRows,
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
}]);
