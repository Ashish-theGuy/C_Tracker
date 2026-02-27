// API Base URL - Use relative path in production, absolute in development
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000/api' 
    : '/api';

// Load cities on page load
window.addEventListener('DOMContentLoaded', () => {
    loadCities();
    
    // Allow Enter key to submit
    document.getElementById('user-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            askAI();
        }
    });
});

// Load available cities
async function loadCities() {
    try {
        const response = await fetch(`${API_BASE_URL}/cities`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success && data.cities) {
            const cityNames = data.cities.map(c => c.name).join(', ');
            document.getElementById('cities-list').textContent = cityNames;
        } else {
            document.getElementById('cities-list').textContent = 'No cities available';
        }
    } catch (error) {
        console.error('Error loading cities:', error);
        document.getElementById('cities-list').textContent = 'Error loading cities: ' + error.message;
    }
}

// Ask AI about a city or general question
async function askAI() {
    const userInput = document.getElementById('user-input');
    const query = userInput.value.trim();
    
    if (!query) {
        return;
    }
    
    // Show loading
    showLoading();
    
    // Disable input
    userInput.disabled = true;
    document.getElementById('send-btn').disabled = true;
    
    try {
        const response = await fetch(`${API_BASE_URL}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: query })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResponse(data);
        } else if (data.error) {
            displayError(data.error);
        } else if (data.available_cities) {
            displayError(data.error || 'Please mention a Kerala city name in your query.');
        }
    } catch (error) {
        displayError(`Error: ${error.message}`);
    } finally {
        // Re-enable input
        userInput.disabled = false;
        document.getElementById('send-btn').disabled = false;
        userInput.value = '';
    }
}

// Display response
function displayResponse(data) {
    const responseSection = document.getElementById('response-section');
    const responseContent = document.getElementById('response-content');
    
    const d = data.data || {};
    const liveAnalysis = data.live_analysis || {};
    const frames = liveAnalysis.frames || [];
    
    let html = `
        <div class="city-name">${data.city}</div>
    `;
    
    // Show live YOLO analysis if available
    if (frames.length > 0) {
        html += `
            <div class="live-analysis-box">
                <div class="live-analysis-title">Live YOLO Detection Analysis</div>
                <div class="frames-grid">
        `;
        
        frames.forEach((frameData) => {
            html += `
                <div class="frame-item">
                    <img src="${frameData.frame}" alt="Frame ${frameData.frame_number}" class="detection-frame" />
                    <div class="frame-label">Frame ${frameData.frame_number}: ${frameData.person_count} people detected</div>
                </div>
            `;
        });
        
        html += `
                </div>
                <div class="analysis-note">YOLOv8 model detecting people in real-time from ${data.city} video</div>
            </div>
        `;
    }
    
    html += `
        <div class="analysis-box">
            <div class="analysis-item">
                <span class="analysis-label">Current Crowd:</span>
                <span class="analysis-value">${d.current_people || 0} people</span>
            </div>
            <div class="analysis-item">
                <span class="analysis-label">Crowd Level:</span>
                <span class="analysis-value crowd-${(d.crowd_level || 'unknown').toLowerCase()}">${d.crowd_level || 'Unknown'}</span>
            </div>
            <div class="analysis-item">
                <span class="analysis-label">Average:</span>
                <span class="analysis-value">${d.average_people || 0} people</span>
            </div>
            <div class="analysis-item">
                <span class="analysis-label">Max Seen:</span>
                <span class="analysis-value">${d.max_people || 0} people</span>
            </div>
        </div>
        <div style="text-align:center;margin-bottom:16px;">
            <button class="live-stream-btn" onclick="openLiveStream('${encodeURIComponent(data.city)}')">Show Live Count</button>
        </div>
    `;
    
    if (d.description) {
        html += `<div class="message-text">${d.description}</div>`;
    }
    
    responseContent.innerHTML = html;
    responseSection.style.display = 'block';
    
    responseSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Open live stream modal for a city
function openLiveStream(encodedCity) {
    const city = decodeURIComponent(encodedCity);
    const modal = document.getElementById('live-modal');
    const img = document.getElementById('live-stream-img');
    const title = document.getElementById('live-modal-title');

    title.textContent = `Live Count — ${city}`;

    // Determine base URL (without /api)
    const base = window.location.hostname === 'localhost' ? 'http://localhost:5000' : '';
    img.src = `${base}/api/live-stream/${encodeURIComponent(city)}`;

    modal.style.display = 'flex';
}

// Close live modal
document.addEventListener('DOMContentLoaded', () => {
    const closeBtn = document.getElementById('live-modal-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            const modal = document.getElementById('live-modal');
            const img = document.getElementById('live-stream-img');
            img.src = '';
            modal.style.display = 'none';
        });
    }
});

// Show loading state
function showLoading() {
    const responseSection = document.getElementById('response-section');
    const responseContent = document.getElementById('response-content');
    
    responseContent.innerHTML = '<div class="loading">Analyzing crowd data...</div>';
    responseSection.style.display = 'block';
}

// Display error
function displayError(message) {
    const responseSection = document.getElementById('response-section');
    const responseContent = document.getElementById('response-content');
    
    responseContent.innerHTML = `<div class="error">${message}</div>`;
    responseSection.style.display = 'block';
}
