/*
 *	JS functions for the app
 *
 *	@author rob.dunne@manchester.ac.uk
 *	August 2016
 *
 */

// Vars
const {dialog} = require('electron').remote;
const {app} = require('electron').remote;
const Datastore = require('nedb');
const moment = require('moment');
const csv = require('csv');
const NProgress = require('nprogress');

var dbPath = app.getPath('appData');
//var db = new Datastore({ filename: dbPath }); // specify filepath for persistence
var db = new Datastore();
var fs = require('fs');

// Load the database
db.loadDatabase(function(err) {
    if(err) {
      console.log(err);
    } else {
      console.log('Database loaded.');
    }
});

// Switch app view
$(function() {
  $('#eta-nav-main a').click(function() {
    $('#eta-nav-main a span').removeClass('fa fa-check');
    $(this).find('span').addClass('fa fa-check');

    $('#eta-nav-main a').css('opacity', 0.5);
    $(this).css('opacity', 1);

    var view = $(this).attr('href');
    $('.eta-view').hide();
    $(view).show();

    return false;
  });
});

// Fetch data from an analysis module
function getAPIData(analysis, input) {
  // Call the python API
  var dataString = '';
  var json = {};

  try {
    var py = require('child_process').spawn('python3', ['api.py', analysis, input]);
  } catch(error) {
    console.log(error);
  }

  // Get the output data from the python API
  py.stdout.on('data', function(data) {
    dataString += data.toString();
  });

  // When the python API output has finished
  py.stdout.on('end', function() {
    json = JSON.parse(dataString);
    //console.log(json);

    // Save the processed data in the database


    // Show an update message
    notifyUser('Data Analysis Update', 'Analysis complete for '+input);
  });

  // Pass parameters to the API
  //py.stdin.write(parameters);
  //py.stdin.end();

  // Kill the python process once done
  py.kill('SIGINT');
}
