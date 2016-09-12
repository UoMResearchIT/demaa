/*
 *	NodeJS controller for the app
 *
 *	@author rob.dunne@manchester.ac.uk
 *	August 2016
 *
 */

const electron = require('electron');
const app = electron.app;  // Module to control application life.
const BrowserWindow = electron.BrowserWindow;  // Module to create native browser window.

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the javascript object is GCed.
var mainWindow = null;

// Quit when all windows are closed.
app.on('window-all-closed', function() {
	app.quit();
});

// This method will be called when Electron has done everything
// initialization and ready for creating browser windows.
app.on('ready', function() {
	var openWindow = function() {
		// Create the browser window.
		var {width, height} = electron.screen.getPrimaryDisplay().workAreaSize;
		mainWindow = new BrowserWindow({width, height});

		// and load the index.html of the app.
		mainWindow.loadURL('file://' + __dirname + '/src/templates/index.html');

		// Open the devtools.
		mainWindow.webContents.openDevTools();

		// Emitted when the window is closed.
		mainWindow.on('closed', function() {
			// Dereference the window object, usually you would store windows
			// in an array if your app supports multi windows, this is the time
			// when you should delete the corresponding element.
			mainWindow = null;
		});
	};

	// Start the application
	openWindow();
});
