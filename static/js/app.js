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
    d3.select("#sel-filter-year").on("change", populateLgaFilter);
    d3.select("#sel-filter-year").on("change", populateOffenceFilter);
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
    d3.select("#sel-filter-lga").on("change", populateYearFilter);
    d3.select("#sel-filter-lga").on("change", populateOffenceFilter);
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
    d3.select("#sel-filter-offence").on("change", populateYearFilter);
    d3.select("#sel-filter-offence").on("change", populateLgaFilter);
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

  var url = "http://127.0.0.1:5000/api/query/" + dropdown_values.year + "/" 
              + dropdown_values.lga + "/" + dropdown_values.offence;

  window.open(
    url, "Query Result",
    "height=800,width=500,modal=yes,alwaysRaised=yes");
    
buildIncidentPieChart();
}


function buildIncidentPieChart(selectedincident) {
  // If we have race to filter by let's pass it
  // in as a querystring parameter
  var dropdown_values = new Object();
  getDropdownValues(dropdown_values);

  var url = `api/query/${dropdown_values.year}/${dropdown_values.lga}/${dropdown_values.offence}`;

  alert(url);

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

// Upon intial load of the page setup
// the visualisations and the select filter
populateYearFilter();
populateLgaFilter();
populateOffenceFilter();
buildIncidentPieChart();