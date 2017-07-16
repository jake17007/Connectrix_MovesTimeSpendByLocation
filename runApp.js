var fs = require('fs');

// Load the data from data.json
var data = require('./data.json');

// Send data to app.py
var PythonShell = require('python-shell');
var pyshell = new PythonShell('app.py', {mode: 'json'});
pyshell.send(data);

// Receive output from the Python script
var output;
pyshell.on('message', function(pythonOutput) {
  console.log('Python output received.');
  output = pythonOutput;
})

// Log the output or any error that occurred within the Python script
.end(function(error) {
  if (error)
    console.log('AN ERROR OCCURED WITHIN THE PYTHON SCRIPT:', error);
  else
    var html = fs.readFileSync('./libraries.html', 'utf8');
    fs.writeFileSync('view.html', html);
    fs.appendFileSync('view.html', output.html);
    console.log('Output has been written to view.html.');

});
