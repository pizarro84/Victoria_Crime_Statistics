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

    var config = {responsive: true};

    Plotly.newPlot('character-races-plot', data, layout,config);

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
buildIncidentBubbleChart();
}

function buildIncidentBubbleChart(selectedincident) {

  var dropdown_values = new Object();
  getDropdownValues(dropdown_values);
  var url = `api/query/${dropdown_values.year}/${dropdown_values.lga}/${dropdown_values.offence}`;


  d3.json(url).then(function (response) {
    var data = [{
      x: response.map(d => d.year),
      y: response.map(d => d.incidents_recorded),
      mode: 'markers',
      marker:{
        size: [20,20, 20, 20,20,20,20,20,20,20]
      }
    }];

    var config = {responsive: true};

    Plotly.newPlot('bubble-plot', data, config);

  });
}

function buildIncidentPieChart(selectedincident) {
  var dropdown_values = new Object();
  getDropdownValues(dropdown_values);

  var url = `api/query/${dropdown_values.year}/${dropdown_values.lga}/${dropdown_values.offence}`;

  d3.json(url).then(function (response) {
    var data = [{
      labels: response.map(d => d.Offence_Division),
      values: response.map(d => d.Incidents_Recorded),
      type: 'pie'
    }];

    var config = {responsive: true};

    Plotly.newPlot('character-races-plot', data, config);
  });
}

function buildIncidentBarChart(dropdown_values) {
  var dropdown_values = new Object();
  getDropdownValues(dropdown_values);

  var url = `api/query/${dropdown_values.year}/${dropdown_values.lga}/${dropdown_values.offence}`;
  
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
      barmode: 'stack'
    };

    var config = {responsive: true};
    
    Plotly.newPlot('races-by-class-plot', traces, layout, config);
  });
}

/***************************************************************
***   Get all data
***************************************************************/
function getAllBarChart() {
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
      title: 'Total Offences in VIC from 2011-2020',
      barmode: 'stack',
      paper_bgcolor:'rgba(255,255,255,.85)'
    };

    var config = {responsive: true};
    
    Plotly.newPlot('races-by-class-plot', traces, layout, config);
  });
}

function getAllPieChart() {
  var url = "api/all";  

  d3.json(url).then(function (response) {
    
    var data = [{
      labels: response.map(d => d.offence_division),
      values: response.map(d => d.incidents_recorded),
      type: 'pie'
    }];
    
    var layout = {
      title: 'Offence Division Distribution in VIC from 2011-2020',
      paper_bgcolor:'rgba(255,255,255,.85)'
    };

    var config = {responsive: true};
    Plotly.newPlot('character-races-plot', data,  layout, config);
  });
  
}



function getAllBubbleChart() {
  var url = 'api/sum_by_year';

  d3.json(url).then(function (response) {
    var data = [{
      x: response.map(d => d.year),
      y: response.map(d => d.total),
      mode: 'markers',
      marker:{
        size: [80,25,45,30,22,40,30,25,45,30],
        sizeref: .2, 
        color: ['rgb(255,0,55)','rgb(255,0,55)','rgb(30,200,15)','rgb(255,55,55)','rgb(0,80,150)','rgb(0,0,105)',
                'rgb(255,0,55)','rgb(30,200,15)','rgb(255,55,55)','rgb(0,80,150)'],
        sizemode: 'area',
        opacity: 0.7
      }
    }];

    var layout = {
      title: 'All crimes in VIC from 2011 - 2020',
      height: 600,
      paper_bgcolor:'rgba(255,255,255,.85)'
    };

    var config = {responsive: true};

    Plotly.newPlot('bubble-plot', data, layout, config);

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


// Upon intial load of the page setup
// the visualisations and the select filter
populateYearFilter();
populateLgaFilter();
populateOffenceFilter();
getAllBarChart();
getAllPieChart();
getAllBubbleChart();