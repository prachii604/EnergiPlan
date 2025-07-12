
// let map;

// // Fetch forecast and update UI + Map
// function getForecast() {
//   const city = document.getElementById("cityInput").value;
//   if (!city) return;

//   fetch(`http://localhost:5000/predict?city=${city}`)
//     .then((res) => res.json())
//     .then((data) => {
//       if (data.error) {
//         alert("City not found or API issue.");
//         return;
//       }

//       const forecastEl = document.getElementById("forecastOutput");
//       forecastEl.classList.remove("hidden");
//       forecastEl.innerHTML = `
//         <h2>Forecast for ${data.city}</h2>
//         <p><strong>Temperature:</strong> ${data.temperature}°C</p>
//         <p><strong>Humidity:</strong> ${data.humidity}%</p>
//         <p><strong>Cloud Cover:</strong> ${data.cloud_cover}%</p>
//         <p><strong>Irradiance:</strong> ${data.irradiance} W/m²</p>
//         <p><strong>Estimated Solar Output:</strong> ${data.prediction} units</p>
//       `;

//       // Save to localStorage for reuse on chores page
//       localStorage.setItem("lastForecast", forecastEl.innerHTML);

//       // Update the map location
//       updateMap(city);
//     })
//     .catch((err) => {
//       alert("Failed to get forecast. Backend might be down.");
//       console.error(err);
//     });
// }

// // Initialize the map on page load
// window.addEventListener("DOMContentLoaded", () => {
//   const mapContainer = document.getElementById("map");
//   if (mapContainer) {
//     map = L.map("map").setView([20.5937, 78.9629], 5); // Center of India

//     L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
//       attribution: "Map data © OpenStreetMap contributors",
//       maxZoom: 18,
//     }).addTo(map);
//   }

//   // Restore forecast on chores page
//   const bestTimeOutput = document.getElementById("bestTimeOutput");
//   if (bestTimeOutput && localStorage.getItem("lastForecast")) {
//     bestTimeOutput.innerHTML = localStorage.getItem("lastForecast");
//   }
// });

// // Move map view to city
// function updateMap(city) {
//   fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${city}`)
//     .then((res) => res.json())
//     .then((data) => {
//       if (data && data.length > 0) {
//         const { lat, lon } = data[0];
//         map.setView([lat, lon], 10);
//         L.marker([lat, lon]).addTo(map).bindPopup(`${city}`).openPopup();
//       }
//     });
// }


document.getElementById("themeToggle").addEventListener("click", () => {
  document.body.classList.toggle("dark-mode");
});

const getForecastBtn = document.getElementById("getForecastBtn");
if (getForecastBtn) {
  getForecastBtn.addEventListener("click", () => {
    const city = document.getElementById("cityInput").value.trim();
    if (!city) return alert("Please enter a city name");

    fetch(`/predict?city=${encodeURIComponent(city)}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.error) throw new Error(data.error);
        localStorage.setItem("forecastData", JSON.stringify(data));
        window.location.href = "forecast.html";
      })
      .catch(() => alert("Failed to get forecast. Backend might be down."));
  });

  const map = L.map("map").setView([20.5937, 78.9629], 5); // India center
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors",
  }).addTo(map);
}

const data = JSON.parse(localStorage.getItem("forecastData"));
if (data && document.getElementById("solarPanel")) {
  document.getElementById("cityTitle").innerText =
    `Solar and Wind Forecast for the City: ${data.city}`;

  document.getElementById("solarPanel").innerHTML = `
    <p><strong>City:</strong> ${data.city}</p>
    <p><strong>Temperature:</strong> ${data.temperature} °C</p>
    <p><strong>Humidity:</strong> ${data.humidity} %</p>
    <p><strong>Cloud Cover:</strong> ${data.cloud_cover} %</p>
    <p><strong>Irradiance:</strong> ${data.irradiance} W/m²</p>
    <p><strong>Solar Output:</strong> ${data.prediction} units</p>
  `;

  document.getElementById("windPanel").innerHTML = `
    <p><strong>Wind Speed:</strong> ${data.wind_speed} m/s</p>
    <p><strong>Wind Direction:</strong> ${data.wind_deg} °</p>
    <p><strong>Avg Wind-Speed to run the windmill:</strong> 3-4 m/s</p>
    
  `;
}

