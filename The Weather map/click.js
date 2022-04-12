let map;
function initMap() {
  const myLatlng = { lat: -31, lng: 26};
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 6,
    center: myLatlng,
  });
  // Create the initial InfoWindow.
  let infoWindow = new google.maps.InfoWindow({
    content: "Click the map to get Lat/Lng!",
    position: myLatlng,
  });

  infoWindow.open(map);
  // Configure the click listener.
  map.addListener("click", (mapsMouseEvent) => {
    // Close the current InfoWindow.
    infoWindow.close();
    // Create a new InfoWindow.
    infoWindow = new google.maps.InfoWindow({
      position: mapsMouseEvent.latLng,
    });
    infoWindow.setContent(
      JSON.stringify(mapsMouseEvent.latLng.toJSON(), null, 2)
    );
    infoWindow.open(map);
  });
map.addListener("click", (mapsMouseEvent)=> {
  let mapInfo = JSON.stringify(mapsMouseEvent.latLng.toJSON(), null, 2)

$.ajax({
  type: 'POST',
  url: 'http://127.0.0.1:5000/',
  data: mapInfo,
  contentType: 'application/json',
  dataType: 'json',
  success: function (response) {
    
    for (let i=0; i<12; i++) {
      document.getElementById (String(i + 1)).innerHTML = 'Time: ' +  response[i]["time"] +'<br>'+'Date: '+ response[i]["date"] + '<br>' + '<br>' 
      + '<canvas id='+('k' + String(i)) + ' width="50" height="50">' + '</canvas>' + '<br>' 
      + 'Temperature: ' + response[i]["temp"] + ' &#176'+'C' + '<br>' 
      + 'Wind Speed: ' + response[i]["windSpeed"] + ' m/s' + '<br>' 
      + 'Wind Direction: ' + response[i]["windDirection"] + '<br>'
    }
    var skycons = new Skycons({"color":"black"});
    for (let i=0; i<12; i++) {
      var hour = (response[i]["time"].split(":")[0]);
      if (hour <= 6 || hour >= 18 ){
        if (response[i]['cloudcover'] < 25){
          skycons.set(('k'+String(i)), Skycons.CLEAR_NIGHT);
        }else if (response[i]['cloudcover'] < 75){
          skycons.set(('k'+String(i)), Skycons.PARTLY_CLOUDY_NIGHT);
        }else{
          skycons.set(('k'+String(i)), Skycons.CLOUDY);
        }
      }
      else{
        if (response[i]['cloudcover'] < 25){
          skycons.set(('k'+String(i)), Skycons.CLEAR_DAY);
        }else if (response[i]['cloudcover'] < 75){
          skycons.set(('k'+String(i)), Skycons.PARTLY_CLOUDY_DAY);
        }else{
          skycons.set(('k'+String(i)), Skycons.CLOUDY);
        }
      }
      skycons.play();
    }
  }
  });
});
}