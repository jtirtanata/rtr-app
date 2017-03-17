
function collapseMeasurements() {
   $('#input-measurements').toggle();
}

var selected = "rgb(176, 207, 136)"
var unselected = "rgb(224, 208, 227)";
selected_data = [];

/* fetching body types */
fetchBodyTypes();

function fetchBodyTypes() {
  $.ajax({
   type: "GET",
   contentType: "application/json; charset=utf-8",
   url: "/body_types",
   dataType: "json",
   async: true,
   success: function (data) {
     for (var i = 0; i < data.length; i++) {
       $('select#body-type').append('<option value="' + data[i][1] + '">' + data[i][0] + '</option>');
     }
   },
   error: function (err) {

   }
 });
 }

fetchInputLabels();

function fetchInputLabels() {
  $.ajax({
   type: "GET",
   contentType: "application/json; charset=utf-8",
   url: "/labels",
   dataType: "json",
   async: true,
   success: function (data) {
     for (var i = 0; i < data.length; i++) {
       selected_data.push(0)
     }
     var width = 200;
     var height = 50;
     var gap = 15;
     var padding = 50;

     var svg = d3.select("div#input-squares").append("svg")
                .attr("width", (width + gap) * 4 + padding)
                .attr("height",(height + gap) * 2 + padding);
     var g = svg
             .selectAll("g")
             .data(data)
             .enter()
             .append("g")
             .attr("transform", function(d, i) {
               y = Math.floor(i/4) * (height + gap) + padding;
               x = i%4 * (width + gap) + padding;
               return "translate(" + x + "," + y+ ")";
             })
             .attr("index", function(d, i) {
               return i;
             })
             .attr("selected", 0)
             .on("click", function() {
               var ind = this.getAttribute("index");
               var isSelected = selected_data[ind] == 1;
               if (isSelected){
                 d3.select(this).select('rect')
                   .classed("selected-input", false);
                 selected_data[ind] = 0;
               } else {
                 d3.select(this).select('rect')
                  .classed("selected-input", true);
                 selected_data[ind] = 1;
               }
             });

     g.append("rect").attr("width", width)
       .attr("height", height)
       .text(function(d) {return d;})
       .classed("selected-input", false);

     g.append("text")
       .attr("class", "label")
       .attr("y", function(d, i) { return height/2 + 5; })
       .attr("x", function(d, i) { return 15; })
       .text(function(d) { return d; });
   },
   error: function (err) {
     console.log(err);
   }
 });
}
function fetchResults() {
  var body_info = "";
  var body_inputs = $('.body-input');
  for (var i = 0; i < body_inputs.length; i ++) {
    id = body_inputs[i].getAttribute("id");
    val =  $('#' + id).val();
    if (i != 0 ) {
      body_info += ", ";
    }
    body_info += "\"" + id + "\" : \"" + val + "\"";
  }
  var include_measurement = $('#input-measurements').is(":visible");
  if (include_measurement) {
    include_measurement = 1;
  } else {
    include_measurement = 0;
  }
  body_info += ", \"body-info\" : \"" + include_measurement + "\"";
  input_data = "{\"preferences\": \"" + selected_data + "\","
        + body_info + "}";
  console.log(input_data);
  $.ajax({
   type: "POST",
   contentType: "application/json; charset=utf-8",
   url: "/rec",
   dataType: "json",
   async: true,
   data: input_data,
   success: function (data) {
     console.log(data);
     displayResults(data);
   },
   error: function (err) {
     console.log(err);
   }
 });
}


var comment_holder = document.getElementById('comments');
var dresses = [];
function displayResults(data){
  $('.result').remove();
  dresses = data['dresses'];
  for (var i = 0; i < dresses.length; i++) {
    displayDress(dresses[i], i);
  }
  $('li.result').on('click', function(e)
  {
    var ind = this.getAttribute('index');
    $('#designer').text(dresses[ind][1])
    $('#dress-title').text(dresses[ind][0])
    $('#big-img-link').attr('src', dresses[ind][2])
    $('#rtr-link').attr('href', dresses[ind][3])
    $('#myModal').modal('show');
  });
}
var result_holder = document.getElementById('results-list');

function displayDress(dress, index) {
  console.log(dress);
  li_el = document.createElement('li');
  img_el = document.createElement('img');
  li_el.setAttribute('class', 'result');
  li_el.setAttribute('href', dress[3]);
  li_el.setAttribute('index', index);
  img_el.src = dress[2];
  li_el.append(img_el);
  result_holder.append(li_el);
}
