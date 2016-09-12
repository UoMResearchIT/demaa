self.addEventListener("message", function(e) {
  var i=0;
  var k=0;
  var csvJSON = [];
  var csvArray = JSON.parse(e.data);

  for(i;i<csvArray.length;i++) {
    var j=0;

    if(i>0) {
      var csvLine = {};
      for(j;j<csvArray[0].length;j++) {
        csvLine[csvArray[0][j]] = csvArray[i][j];
      }
      csvJSON.push(csvLine);
      k++;
    }
  }

  postMessage(JSON.stringify(csvJSON));
}, false);
