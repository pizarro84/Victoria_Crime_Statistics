function populateYearFilter() {
  // Let's populate the <option> elements in 
  // our <select> from the database. 
  const url = "api/values/year";

  d3.json(url).then(function (response) {

    var filterOptions = ["All"];
    filterOptions = filterOptions.concat(response);

    d3.select("#sel-filter-year")
      .selectAll("option")
      .data(filterOptions)
      .enter()
      .append("option")
      .text(d => d);

    // Bind an event to refresh the data
    // when an option is selected.
    d3.select("#sel-filter-year").on("change", disableDropdown);
  });
}

function populateLgaFilter() {
  // Let's populate the <option> elements in 
  // our <select> from the database. 
  const url = "api/values/local_government_area";

  d3.json(url).then(function (response) {

    var filterOptions = ["All"];
    filterOptions = filterOptions.concat(response);

    d3.select("#sel-filter-lga")
      .selectAll("option")
      .data(filterOptions)
      .enter()
      .append("option")
      .text(d => d);

    // Bind an event to refresh the data
    // when an option is selected.
    d3.select("#sel-filter-lga").on("change", disableDropdown);
  });
}

function populateOffenceFilter() {
  // Let's populate the <option> elements in 
  // our <select> from the database. 
  const url = "api/values/offence_division";

  d3.json(url).then(function (response) {

    var filterOptions = ["All"];
    filterOptions = filterOptions.concat(response);

    d3.select("#sel-filter-offence")
      .selectAll("option")
      .data(filterOptions)
      .enter()
      .append("option")
      .text(d => d);

    // Bind an event to refresh the data
    // when an option is selected.
    d3.select("#sel-filter-offence").on("change", disableDropdown);
  });
}


function refreshCharts(event) {
  // event.target will refer tp the selector
  // from which we will get the selected option
  var selectedValue = d3.select(event.target).property('value');

  // With the selectedValue we can refresh the charts
  // filtering if needed. 
  buildRacesPieChart(selectedValue);
  buildRacesByClassBarChart(selectedValue);
}


function buildIncidentPieChart(selectedincident) {
  // If we have race to filter by let's pass it
  // in as a querystring parameter
  var url = "api/sum_by_incidents";


  d3.json(url).then(function (response) {
    // In order to render a pie chart we need to 
    // extract the labels and values from the 
    // json response. For an example see:
    // https://plotly.com/javascript/pie-charts/ 
    var data = [{
      labels: response.map(d => d.offence_division),
      values: response.map(d => d.total),
      type: 'pie'
    }];

    var layout = {
      height: 400,
      width: 500
    };

    Plotly.newPlot('character-races-plot', data, layout);

  });
}

function getDropdownValues(dropdown_values) {
  dropdown_values.year = document.getElementById("sel-filter-year").value;
  dropdown_values.lga = document.getElementById("sel-filter-lga").value;
  dropdown_values.offence = document.getElementById("sel-filter-offence").value;
}

function displayValues() {
  var dropdown_values = new Object();
  getDropdownValues(dropdown_values);
    
buildIncidentPieChart();
buildIncidentBarChart();
builddatatable('D');
}


function buildIncidentPieChart(selectedincident) {
  // If we have race to filter by let's pass it
  // in as a querystring parameter
  var dropdown_values = new Object();
  getDropdownValues(dropdown_values);

  var url = `api/query/${dropdown_values.year}/${dropdown_values.lga}/${dropdown_values.offence}`;

  //alert(url);

  d3.json(url).then(function (response) {
    // In order to render a pie chart we need to 
    // extract the labels and values from the 
    // json response. For an example see:
    // https://plotly.com/javascript/pie-charts/ 
    var data = [{
      labels: response.map(d => d.Offence_Division),
      values: response.map(d => d.Incidents_Recorded),
      type: 'pie'
    }];
    var layout = {
      height: 400,
      width: 500
    };
    Plotly.newPlot('character-races-plot', data, layout);
  });
}

function buildIncidentAllBarChart(dropdown_values) {
  var url = "api/all";  

  d3.json(url).then(function (response) {
    
    var data = [{
      labels: response.map(d => d.offence_division),
      values: response.map(d => d.incidents_recorded),
      type: 'pie'
    }];
    var layout = {
      height: 400,
      width: 500
    };
    Plotly.newPlot('character-races-plot', data, layout);
  });
  
}


function buildIncidentBarChart(dropdown_values) {
  var dropdown_values = new Object();
  getDropdownValues(dropdown_values);

  var url = `api/query/${dropdown_values.year}/${dropdown_values.lga}/${dropdown_values.offence}`;

  //alert(url);
  
  d3.json(url).then(function(response) {

    var grouped_data = d3.group(response, d => d.Offence_Division)

    var traces = Array();

    grouped_data.forEach(element => {      
      traces.push({
        x: element.map(d => d.Year),
        y: element.map(d => d.Incidents_Recorded),
        name: element[0].Offence_Division,
        type: 'bar'
      });
    });
    
    var layout = {
      barmode: 'stack',
      height: 400,
      width: 500
    };
    
    Plotly.newPlot('races-by-class-plot', traces, layout);
  });
}

function buildALLIncidentBarChart(dropdown_values) {
  var url = "api/all";
  
  d3.json(url).then(function(response) {

    var grouped_data = d3.group(response, d => d.offence_division)

    var traces = Array();

    grouped_data.forEach(element => {      
      traces.push({
        x: element.map(d => d.year),
        y: element.map(d => d.incidents_recorded),
        name: element[0].offence_division,
        type: 'bar'
      });
    });
    
    var layout = {
      barmode: 'stack',
      height: 400,
      width: 500
    };
    
    Plotly.newPlot('races-by-class-plot', traces, layout);
  });
}

function disableDropdown(){
  var dropdown_values = new Object();
  getDropdownValues(dropdown_values);

  if (dropdown_values.year !== 'All' && dropdown_values.lga !== 'All') {
    document.getElementById("sel-filter-offence").disabled = true;
  } else if (dropdown_values.lga !== 'All' && dropdown_values.offence !== 'All') {
    document.getElementById("sel-filter-year").disabled = true;
  } else if (dropdown_values.offence !== 'All' && dropdown_values.year !== 'All') {
    document.getElementById("sel-filter-lga").disabled = true;
  } else {
    document.getElementById("sel-filter-lga").disabled = false;
    document.getElementById("sel-filter-offence").disabled = false;
    document.getElementById("sel-filter-year").disabled = false;
  }
}


function builddatatable(ttype){
  var dropdown_values = new Object();
  getDropdownValues(dropdown_values);
  var url = `api/query/${dropdown_values.year}/${dropdown_values.lga}/${dropdown_values.offence}`;

  // Get all data
  if (ttype === 'A') {
    url = 'api/query/All/All/All';
  }
  

  //alert(url);
  
  d3.json(url).then(function(response) {
 
 var tableData = response;
 
  var tbody = d3.select("tbody");
 
 function buildTable(data) {
   // First, clear out any existing data
   tbody.html("");
 
   // Next, loop through each object in the data
   // and append a row and cells for each value in the row
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
populateYearFilter();
populateLgaFilter();
populateOffenceFilter();
buildALLIncidentBarChart();
buildIncidentAllBarChart();
builddatatable('A');