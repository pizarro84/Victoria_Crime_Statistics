function alldata(){
  var url = 'api/getalldata';
  
  d3.json(url).then(function(response) {
 
 var tableData = response;
 
  var tbody = d3.select("tbody");
 
 function buildTable(data) {
   // First, clear out any existing data
   tbody.html("");
 
   data.forEach((dataRow) => {
     // Append a row to the table body
     var row = tbody.append("tr");
 
     // Loop through each field in the dataRow and add
     // each value as a table cell (td)
     Object.values(dataRow).forEach((val) => {
       var cell = row.append("td");
       cell.text(val);
     });
   });
 } 
 buildTable(tableData); 
});
};


// Upon intial load of the page setup
// the visualisations and the select filter
alldata();