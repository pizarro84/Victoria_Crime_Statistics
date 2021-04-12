function populateYearFilter() {
  // Let's populate the <option> elements in 
  // our <select> from the database. 
  const url = "api/values/year";

  d3.json(url).then(function(response) {
    
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

  d3.json(url).then(function(response) {
    
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

  d3.json(url).then(function(response) {
    
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

// Upon intial load of the page setup
// the visualisations and the select filter
populateYearFilter();
populateLgaFilter();
populateOffenceFilter();
