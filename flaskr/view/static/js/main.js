// Import google api resources
const { Map } = await google.maps.importLibrary("maps");
const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
const { DirectionsService, DirectionsRenderer } = await google.maps.importLibrary("routes")



//////////////////////////////////////////////////////////////////////////
/////////////////////////////// Globals //////////////////////////////////
//////////////////////////////////////////////////////////////////////////


// The directions service object
const directionsService = new DirectionsService();

// The directions renderer and configuration options object
const directionsRenderer = new DirectionsRenderer();
directionsRenderer.setOptions({suppressMarkers : true})

// The website's "domain" url
const API_URL = "http://localhost:80/api"

// The map object
let map = null;

// This method tracks the number of locations in a new itinerary.
let locationCounter = 2;



//////////////////////////////////////////////////////////////////////////
///////////////////////// Google Maps Rendering //////////////////////////
//////////////////////////////////////////////////////////////////////////


// This function creates and renders the map.
function createMap(center){

    // Input Validation
    if(!(center instanceof Array) || center.length != 2){
        throw new TypeError("Invalid input parameter center, the input should be a coordinate pair [lat, lng].");
    }

    // The HTML map div
    const mapElement = document.getElementById("map");
    
    // Create a centered map
    map = new Map(mapElement, {
        center : {lat: center[0], lng : center[1]},
        zoom : 6,
        mapId : "fe61e7c9f737b87b"
    });

    // The directions renderer is linked to the map
    directionsRenderer.setMap(map);
}


// This function creates an overlay that displays the routes from destination to destination.
function addDirections(coordinates){

    // Input Validation
    if(!(coordinates instanceof Array)){
        throw new TypeError("Invalid input parameter coordinates, the input should a list of coordinate names and pairs.");
    }

    // The route is mapped only if there is more than one location on the itinerary.
    if(coordinates.length > 1){

        let request = {
            origin : {lat: coordinates[0][1], lng : coordinates[0][2]},
            destination : {lat: coordinates[coordinates.length-1][1], lng : coordinates[coordinates.length-1][2]},
            waypoints : {},
            travelMode : "DRIVING"
        };

        // The waypoints are added.
        let waypoints = Array()

        for(let i=1; i<coordinates.length-1; i++){

            // Input Validation
            if(!(coordinates[i] instanceof Array) || coordinates[i].length != 3){
                throw new TypeError("Invalid input parameter coordinates, the input should be a list of location names and coordinate pairs.");
            }

            waypoints.push({
                location : {lat: coordinates[i][1], lng : coordinates[i][2]},
            });
        }

        request.waypoints = waypoints;

        // The route is mapped
        directionsService.route(request, (result, status) => {
            if(status == "OK"){
                directionsRenderer.setDirections(result);
            }
        })

    }else{

        // Routes are cleared.
        directionsRenderer.setMap(null);

    }
}


// This function adds custom html markers to the map - containing the name and weather data.
function addMarkers(coordinates, weather){

    // Input Validation
    if(!(coordinates instanceof Array) || !(weather instanceof Array) || coordinates.length != weather.length){
        throw new TypeError("Invalid input parameters, the itinerary and weather arrays must be of equal length.");
    }

    const markers = new Array()

    // The custom markers are created and rendered to the map.
    for(let i=0; i<weather.length; i++){

        let location = coordinates[i][0]
        let data = weather[i];

        // Custom html marker element
        let customMarker = document.createElement("div")
        customMarker.className = "markerBox";
        customMarker.innerHTML =
        `   
            <div class="weather-marker">
                <h2>${i+1}: ${location}</h2>
                <p>Currently ${data["main"]["description"]} with a temperature of ${data["main"]["current_temp"]}°C</p>
            </div>
            <div class="down-arrow"></div>
        `

        // New markers are added to the map
        markers.push(new AdvancedMarkerElement({
            map : map,
            position: {lat : data["coordinates"][0], lng : data["coordinates"][1]},
            content : customMarker
        }))
    }
}



//////////////////////////////////////////////////////////////////////////
///////////////////////// Itinerary API functions ////////////////////////
//////////////////////////////////////////////////////////////////////////


/**
 * This function retrieves a list of itinerary names from the API
 */
async function getItineraryNames(){

    // A list of itinerary names are retrieved via api
    let response = await fetch(API_URL + "/itineraries", {method : "GET"});

    // The response is validated
    if(!response.ok){
        throw new Error("Something went wrong while requesting the list of itineraries.");
    }

    let data = await response.json();

    return data["itineraries"];
}


/**
 * This function retrieves itinerary from the API
 * 
 * @param {string} name The name of the itinerary to retrieve.
 * 
 */ 
async function getItinerary(name){

    // Input Validation
    if(typeof(name) != "string"){
        throw new TypeError("Invalid input parameters: name => string.");
    }

    // The itinerary is retrieved via the api
    let response = await fetch(API_URL + `/itineraries/${name}`, {method : "GET"});

    // The response is validated.
    if(!response.ok){
        throw new Error("Something went wrong while requesting the list of itineraries.");
    }

    let data = await response.json();

    return data;
}


/**
 * This function creates a new itinerary and saves it via the API
 * 
 * @param {string} name the name of the itinerary being created.
 * 
 * @param {Array} coordinates an array of locations and coordinates.
 */ 
async function createItinerary(name, coordinates){

    // Input Validation
    if(typeof(name) != "string" || !(coordinates instanceof Array)){
        throw new TypeError("Invalid input parameters: the name must be a string and the coordinates an array.");
    }

    // The body of the POST request is generated
    let body = {
        name : name,
        coordinates : coordinates
    };

    // The request is POSTed to create a new itinerary
    let response = await fetch(API_URL + "/itineraries", {
        method : "POST", 
        body : JSON.stringify(body), 
        headers : {
            "Content-Type" : "application/json"
        }
    });

    // Response validation
    if(!response.ok){
        throw new Error("Something went wrong while creating this resource.");
    }
}


/**
 * This function deletes an itinerary using the itineraries name.
 * 
 * @param {string} name the name of the intinerary to be deleted.
 */
async function deleteItinerary(name){

    // Input Validation
    if(typeof(name) != "string"){
        throw new TypeError("Invalid input parameter: the name must be a string.");
    }

    // The itinerary is deleted
    let response = await fetch(API_URL + `/itineraries/${name}`, {method : "DELETE"});

    // Response validation
    if(!response.ok){
        throw new Error("Something went wrong while deleting this itinerary.");
    }
}



//////////////////////////////////////////////////////////////////////////
////////////////////////// Weather API functions /////////////////////////
//////////////////////////////////////////////////////////////////////////


/**
 * This function retrieves the weather data for all the input data points.
 * 
 * @param {Array} coordinates The coordinates by which the weather data
 * is being retrieved. The format here is [[lat, lng]].
 */
async function getWeather(coordinates){

    // Input Validation
    if(!(coordinates instanceof Array)){
        throw new TypeError("Invalid input parameter: itinerary => Array.");
    }

    // The url parameters are set.
    let params = `?lat=${coordinates[0][1]}&lng=${coordinates[0][2]}`;

    for(let i=1; i<coordinates.length; i++){
        params += `&lat=${coordinates[i][1]}&lng=${coordinates[i][2]}`
    }

    // Weather request 
    let response = await fetch(API_URL + `/weather` + params, {method : "GET"});

    // Response validation
    if(!response.ok){
        throw new Error("Something went wrong while retrieving the weather information.");
    }

    let data = await response.json()

    return data["weather-data"]
}



//////////////////////////////////////////////////////////////////////////
////////////////////////// Geocode API functions /////////////////////////
//////////////////////////////////////////////////////////////////////////


/**
 * This function retrieves the coordinates for a plain text location name.
 * 
 * @param {string} location The plain text location to retrieve coordinates for.
 */
async function getCoordinates(location){

    // Input Validation
    if(typeof(location) != "string"){
        throw new TypeError("Invalid input parameter: location => string.");
    }
    
    // Coordinates request 
    let response = await fetch(API_URL + `/geocode/${location}`, {method : "GET"});

    // Response validation
    if(!response.ok){
        throw new Error("Something went wrong while retrieving the coordinates information.");
    }

    let data = await response.json();

    return data["coordinates"]
}


//////////////////////////////////////////////////////////////////////////
//////////////////////// User Interaction Functions //////////////////////
//////////////////////////////////////////////////////////////////////////


// This function displays the map, itinerary and weather data.
async function loadItinerary(name){

    let itinerary = await getItinerary(name);
    let weather = await getWeather(itinerary["coordinates"]);
    createMap(itinerary["center"]);
    addDirections(itinerary["coordinates"]);
    addMarkers(itinerary["coordinates"], weather);

}

window.loadItinerary = loadItinerary;


// This function generates a list of itineraries for the user to select
// and pre-loads the first itinerary for viewing.
async function createItineraryList(){

    // The HTML itinerary selection div
    const itineraryList = document.getElementById("itinerary-list");
    
    itineraryList.innerHTML = "";

    let names = await getItineraryNames();

    for(let name of names){
        itineraryList.innerHTML += 
        `
        <div class="itinerary-container">
            <div class="itinerary-button itinerary-name" onclick="loadItinerary('${name}')">
                <h2>${name}</h2>
            </div>
            <div class="itinerary-button delete-itinerary" onclick="removeItinerary('${name}')">
                <h2>Delete</h2>
            </div>
        <div>
        `
    }

    // The first itinerary is loaded
    loadItinerary(names[0]);
}



// This function removes a given itinerary from the list and then reloads
// the itinerary list and map.
async function removeItinerary(name){

    await deleteItinerary(name);
    await createItineraryList();
}

window.removeItinerary = removeItinerary;



// This function generates coordinates corresponding to the input location
// name.
async function addCoords(id){

    // Search term is retrieved
    const searchTerm = document.getElementById(`location-name-${id}`).value;

    // The elements to be updated are retrieved
    const error = document.getElementById(`error-${id}`);
    const latitude = document.getElementById(`location-lat-${id}`);
    const longitude = document.getElementById(`location-lng-${id}`);

    // Set defaults
    let coordinates = Array();
    error.innerText = "";

    // Coordinates are retrieved and exceptions handled
    try{
        coordinates = await getCoordinates(searchTerm);
    }catch(e){
        error.innerText = e.message;
    }

    // If valid coordinates are returned display to screen if they are valid
    // else an error message is displayed
    if(coordinates.length == 2){

        latitude.value = coordinates[0];
        longitude.value = coordinates[1];

        // Coordinates are validated and errors displayed appropriately.
        if(coordinates[0] < 47.5554486 || coordinates[0] > 61.5471111 
            || coordinates[1] < -18.5319589 || coordinates[1] > 9.5844157) {
            
            error.innerText = "This location is not within the UK";
        }

        // Conditional displays error
        if(error.innerText != ""){            
            error.style.display = "block";
        }else{
            error.style.display = "none";
        }
    }else{
        error.innerText = "This location is not within the UK";
        error.style.display = "block";
    }
}

window.addCoords = addCoords;


// This function adds a form section so that a user can add another location
// to the trip itinerary.
function addFormSection(){

    // Parent element retrieved
    const form = document.getElementById("itinerary-form")

    // New form section element created
    const element = document.createElement("div")
    element.className = "form-section"
    element.innerHTML +=
    `
        <div class="input-component">
            <label for="location-name-${locationCounter}">Location</label>
            <input type="text" name="location-name-${locationCounter}" id="location-name-${locationCounter}" placeholder="Location" required>
            <p id="error-${locationCounter}"></p>
        </div>
        <button type="button" class="form-button" onclick="addCoords(${locationCounter})">Auto</button>
        <div class="input-component">
            <label for="location-lat-${locationCounter}">Latitude</label>
            <input type="number" name="location-lat-${locationCounter}" id="location-lat-${locationCounter}" min="47.5554486" max="61.5471111" step="0.0000000000000001" required>
        </div>
        <div class="input-component">
            <label for="location-lat-${locationCounter}">Longitude</label>
            <input type="number" name="location-lng-${locationCounter}" id="location-lng-${locationCounter}" min="-18.5319589" max="9.5844157" step="0.0000000000000001" required>
        </div>
        <button type="button" class="form-button" onclick="addFormSection()">Add Location</button>
    `

    form.appendChild(element);

    locationCounter++;
}

window.addFormSection = addFormSection;


// This method creates a new Itinerary via POST request.
async function submitItinerary(){

    // Parent element retrieved
    const form = document.getElementById("itinerary-form");

    if(form.checkValidity()){

        // Itinerary name retrieved
        const name = document.getElementById("itinerary-name").value;
        
        // Itinerary locations are retrieved
        const coordinates = Array();

        for(let i=1; i<locationCounter; i++){
            coordinates.push([
                document.getElementById(`location-name-${i}`).value, 
                parseFloat(document.getElementById(`location-lat-${i}`).value), 
                parseFloat(document.getElementById(`location-lng-${i}`).value)
            ]);
        }

        let redirect = true;

        try{
            await createItinerary(name, coordinates);
        }catch(e){
            redirect = false;
        }

        if(redirect){
            window.location.href = "http://localhost/index";
        }
    }
}

window.submitItinerary = submitItinerary;


// On the homepage the itinerary list is generated and the default itinerary
// is loaded on the map.
if(document.URL == "http://localhost/index"){
    createItineraryList();
}

