function fetchData() {
  const apiUrl = "http://redrock.sof60.dk:5000/getdata";
  const query = "SELECT * FROM Tempsensdb WHERE tid BETWEEN '"+document.getElementById("date1").value+" 00:00:00' AND '"+document.getElementById("date2").value+" 23:59:59' ORDER BY tid;"
  console.log(query)
  const requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json', // Set the content type based on your API requirements
      // Add any other headers if needed, such as authorization headers
    },
    body: JSON.stringify(query) // Convert the data to JSON format
  };
  fetch(apiUrl, requestOptions)
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json(); // Parse the response body as JSON
  })
  .then(data => {
    // Handle the response data
    console.log('Response Data:', data);
    drawChart(jsontolist(JSON.parse(data)))
  })
  .catch(error => {
    // Handle errors during the fetch request
    console.error('Fetch Error:', error);
  });
  
  
}



google.charts.load('current',{packages:['corechart']});
google.charts.setOnLoadCallback(drawChart);

function jsontolist(jsondata){
  console.log(jsondata[1]['tid'])
  var result = []
  for(var i in jsondata)
    result.push([jsondata[i]["tid"],jsondata[i]["tempdiff"]]);
  return result
}

function drawChart(jsondata) {

// Set Data
const data = google.visualization.arrayToDataTable([
  ['Tid', 'Celsius'],
  ["",0]
]);
for(var i in jsondata)
  data.addRow(jsondata[i])
// Set Options
const options = {
  title: 'Vandspildsdetektor',
  hAxis: {title: 'Tid'},
  vAxis: {title: 'Celsius'},
  legend: 'none'
};

// Draw
const chart = new google.visualization.LineChart(document.getElementById('myChart'));
chart.draw(data, options);

}


