// API Base URL
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5000/api'
    : '/api';

// Map instance
let map;
let markers = {};
let subMarkers = {};
let citiesData = [];

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    initMap();
    fetchCitiesData();

    // Refresh button
    document.getElementById('refresh-btn').addEventListener('click', () => {
        const btn = document.getElementById('refresh-btn');
        btn.textContent = 'Refreshing...';
        btn.disabled = true;
        fetchCitiesData().then(() => {
            btn.textContent = 'Refresh Data';
            btn.disabled = false;
        });
    });

    // Modal close
    document.getElementById('live-modal-close').addEventListener('click', closeLiveModal);

    // Auto-refresh data every 5 seconds to better reflect changes
    setInterval(fetchCitiesData, 5000);
});

// Initialize Leaflet Map
function initMap() {
    // Center of Kerala approx
    map = L.map('map', {
        zoomControl: false // Custom position later
    }).setView([10.1505, 76.5711], 7);

    // Add Zoom Control at bottom right
    L.control.zoom({
        position: 'bottomright'
    }).addTo(map);

    // Dark stylish basemap (CartoDB Dark Matter)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map);

    // Hide sub-markers when zoomed out
    map.on('zoomend', function () {
        if (map.getZoom() < 16) {
            Object.values(subMarkers).forEach(parentGroup => {
                Object.values(parentGroup).forEach(marker => {
                    if (map.hasLayer(marker)) {
                        map.removeLayer(marker);
                    }
                });
            });
        }
    });
}

// Fetch cities data from API
async function fetchCitiesData() {
    try {
        const response = await fetch(`${API_BASE_URL}/cities`);
        if (!response.ok) throw new Error('Network response was not ok');

        const data = await response.json();
        if (data.success && data.cities) {
            citiesData = data.cities;
            updateDashboard();
            updateMapMarkers();
        }
    } catch (error) {
        console.error('Error fetching city data:', error);
    }
}

// Update sidebar dashboard
function updateDashboard() {
    const mainCities = citiesData.filter(c => !c.parent);
    document.getElementById('total-tracked').textContent = mainCities.length;

    // Calculate overall status
    let highCount = 0;
    let medCount = 0;

    let totalPeople = 0;

    mainCities.forEach(city => {
        if (city.processed && city.current_people !== null) {
            totalPeople += city.current_people;
            if (city.crowd_level === 'High') highCount++;
            if (city.crowd_level === 'Medium') medCount++;
        }
    });

    let overall = 'Calm';
    if (highCount >= 2) overall = 'Very Busy';
    else if (highCount > 0 || medCount >= 3) overall = 'Busy';

    document.getElementById('overall-status').textContent = overall;

    renderCitiesList();
}

// Render list of cities in sidebar
function renderCitiesList() {
    const listEl = document.getElementById('cities-list');
    listEl.innerHTML = '';

    // Sort cities: High crowd first
    const mainCities = citiesData.filter(c => !c.parent);
    const sorted = [...mainCities].sort((a, b) => {
        const levelScore = { 'High': 3, 'Medium': 2, 'Low': 1, 'Unknown': 0, 'Not Processed': 0 };
        return (levelScore[b.crowd_level] || 0) - (levelScore[a.crowd_level] || 0);
    });

    sorted.forEach(city => {
        const li = document.createElement('li');
        li.className = 'city-item';

        const levelClass = city.crowd_level ? city.crowd_level.toLowerCase().replace(' ', '-') : 'unknown';
        const peopleCount = city.current_people !== null ? city.current_people : '?';

        li.innerHTML = `
            <div class="city-info">
                <h4>${city.name}</h4>
                <p>${peopleCount} people detected</p>
            </div>
            <div class="city-badge level-${levelClass}">
                ${city.crowd_level || 'Unknown'}
            </div>
        `;

        // Click to fly to city on map
        li.addEventListener('click', () => {
            if (city.coordinates) {
                map.flyTo([city.coordinates.lat, city.coordinates.lng], 12, {
                    duration: 1.5
                });

                // Open popup if marker exists
                setTimeout(() => {
                    if (markers[city.name]) {
                        markers[city.name].openPopup();
                    }
                }, 1500);
            }
        });

        listEl.appendChild(li);
    });
}

// Create or update markers on the map
function updateMapMarkers() {
    citiesData.forEach(city => {
        if (!city.coordinates) return;

        const levelClass = city.crowd_level ? city.crowd_level.toLowerCase().replace(' ', '-') : 'unknown';
        const peopleCount = city.current_people !== null ? city.current_people : 0;

        // Create custom HTML icon
        const iconHtml = `
            <div class="pulse-marker-wrapper marker-${levelClass}">
                <div class="pulse-marker-ring"></div>
                <div class="pulse-marker-core"></div>
            </div>
        `;

        const customIcon = L.divIcon({
            html: iconHtml,
            className: '',
            iconSize: city.parent ? [22, 22] : [30, 30],
            iconAnchor: city.parent ? [11, 11] : [15, 15],
            popupAnchor: city.parent ? [0, -11] : [0, -15]
        });

        // Popup HTML content
        const popupContent = `
            <div class="custom-popup">
                <header>
                    <h3>${city.name}</h3>
                    <p>${city.description || 'Kerala City'}</p>
                </header>
                <div class="popup-stats">
                    <div class="popup-stat-item">
                        <span class="popup-stat-lbl">Detection Count</span>
                        <span class="popup-stat-val ${levelClass !== 'unknown' && levelClass !== 'not-processed' ? 'color-' + levelClass : ''}">${peopleCount}</span>
                    </div>
                    <div class="popup-stat-item" style="text-align: right;">
                        <span class="popup-stat-lbl">Density</span>
                        <span class="popup-stat-val">
                            <span class="city-badge level-${levelClass}" style="padding:2px 8px; font-size:11px;">
                                ${city.crowd_level || 'Unknown'}
                            </span>
                        </span>
                    </div>
                </div>
                <button class="live-btn" onclick="openLiveFeed('${encodeURIComponent(city.name)}', ${peopleCount}, '${city.crowd_level}')">
                    <div class="live-indicator"></div> View Live Analysis
                </button>
            </div>
        `;

        if (city.parent) {
            if (!subMarkers[city.parent]) subMarkers[city.parent] = {};

            if (subMarkers[city.parent][city.name]) {
                // Update existing sub-marker
                subMarkers[city.parent][city.name].setIcon(customIcon);
                subMarkers[city.parent][city.name].setPopupContent(popupContent);
            } else {
                // Create new sub-marker, do not add to map
                const marker = L.marker([city.coordinates.lat, city.coordinates.lng], {
                    icon: customIcon
                }).bindPopup(popupContent, {
                    maxWidth: 300,
                    minWidth: 260
                });
                subMarkers[city.parent][city.name] = marker;
            }
        } else {
            if (markers[city.name]) {
                // Update existing marker
                markers[city.name].setIcon(customIcon);
                markers[city.name].setPopupContent(popupContent);
            } else {
                // Create new marker
                const marker = L.marker([city.coordinates.lat, city.coordinates.lng], {
                    icon: customIcon
                }).bindPopup(popupContent, {
                    maxWidth: 300,
                    minWidth: 260
                }).addTo(map);

                marker.on('click', () => {
                    // Fly to this marker
                    map.flyTo([city.coordinates.lat, city.coordinates.lng], 18, {
                        duration: 1.5
                    });

                    // Show submarkers if any
                    setTimeout(() => {
                        if (subMarkers[city.name]) {
                            Object.values(subMarkers[city.name]).forEach(subMarker => {
                                if (!map.hasLayer(subMarker)) {
                                    subMarker.addTo(map);
                                }
                            });
                        }
                    }, 500); // slight delay for smooth transition
                });

                markers[city.name] = marker;
            }
        }
    });

    // Automatically fit bounds to markers if we have any, on initial load
    if (Object.keys(markers).length > 0 && !window.hasFittedBounds) {
        const group = new L.featureGroup(Object.values(markers));
        // Add some padding to bounds
        map.fitBounds(group.getBounds(), { padding: [50, 50] });
        window.hasFittedBounds = true;
    }
}

// Open modal with MJPEG stream
let liveStreamInterval;

window.openLiveFeed = function (encodedCity, peopleCount, crowdLevel) {
    const city = decodeURIComponent(encodedCity);
    const modal = document.getElementById('live-modal');
    const img = document.getElementById('live-stream-img');
    const title = document.getElementById('live-modal-title');
    const stats = document.getElementById('live-modal-stats');

    title.innerHTML = `<div class="live-indicator"></div> Real-time YOLOv8 Feed: ${city}`;
    stats.textContent = `Current Count: ${peopleCount} | Level: ${crowdLevel}`;

    // Connect to MJPEG stream
    const base = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:5000'
        : '';
    img.src = `${base}/api/live-stream/${encodeURIComponent(city)}`;

    modal.style.display = 'flex';

    // Poll the stream stats to live-update the UI dynamically
    if (liveStreamInterval) clearInterval(liveStreamInterval);
    liveStreamInterval = setInterval(async () => {
        try {
            const response = await fetch(`${base}/api/live-stream-stats/${encodeURIComponent(city)}`);
            if (response.ok) {
                const data = await response.json();
                stats.textContent = `Current Count: ${data.count} | Level: ${data.level}`;
            }
        } catch (e) {
            console.error("Error polling live stream stats:", e);
        }
    }, 1000); // 1-second interval for real-time feel
}

function closeLiveModal() {
    const modal = document.getElementById('live-modal');
    const img = document.getElementById('live-stream-img');

    // Stop stream
    img.src = '';
    modal.style.display = 'none';

    // Clear interval when modal closes
    if (liveStreamInterval) {
        clearInterval(liveStreamInterval);
        liveStreamInterval = null;
    }
}
