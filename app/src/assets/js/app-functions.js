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
