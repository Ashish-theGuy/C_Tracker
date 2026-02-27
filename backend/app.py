"""
Flask Backend for Kerala Cities Crowd Detection
"""
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import os
from datetime import datetime
from video_processor import VideoProcessor
from data_manager import DataManager
from kerala_cities import KERALA_CITIES, get_city_by_name, get_all_cities
from query_processor import QueryProcessor
from live_analyzer import LiveVideoAnalyzer
import cv2
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Initialize components
video_processor = VideoProcessor()
data_manager = DataManager()
query_processor = QueryProcessor()
live_analyzer = LiveVideoAnalyzer()

@app.route('/')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Kerala Cities Crowd Detection API is running",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/ask', methods=['POST'])
def ask_city():
    """
    Endpoint for queries about Kerala cities
    Returns basic crowd data for the requested city
    """
    try:
        data = request.json
        user_query = data.get('query', '').strip()
        
        if not user_query:
            return jsonify({"error": "query is required"}), 400
        
        # Process the query to extract city name
        processed = query_processor.process_query(user_query)
        city_name = processed['city']
        
        if not city_name:
            # No city found in query
            from kerala_cities import get_city_names
            return jsonify({
                "success": False,
                "error": "I can help you with information about these Kerala cities: " + 
                         ", ".join(get_city_names()) + 
                         ". Please mention a city name in your query.",
                "available_cities": get_city_names()
            }), 200
        
        # Get city info
        city_info = get_city_by_name(city_name)
        if not city_info:
            return jsonify({"error": f"City '{city_name}' not found"}), 404
        
        # Check if video has been processed for this city
        # Force reload to ensure fresh data
        data_manager.load_data()
        location_data = data_manager.get_location_data(city_name)
        
        # If not processed, process the video now
        if not location_data:
            video_path = city_info['video_file']
            if os.path.exists(video_path):
                # Process video
                stats = video_processor.process_location_video(
                    video_path,
                    city_name,
                    city_info['coordinates']
                )
                # Store data
                data_manager.save_location_data(city_name, stats, city_info['coordinates'])
                location_data = data_manager.get_location_data(city_name)
            else:
                return jsonify({
                    "success": False,
                    "error": f"Video for {city_name} not found. Please upload the video first.",
                    "expected_video": video_path
                }), 404
        
        # Get live video analysis frames
        video_path = city_info['video_file']
        live_frames = []
        if os.path.exists(video_path):
            try:
                live_frames = live_analyzer.get_sample_frames(video_path, num_frames=8)
            except Exception as e:
                print(f"Error getting live frames: {e}")
        
        # Format response with basic crowd data
        response = {
            "success": True,
            "city": city_name,
            "query": user_query,
            "data": {
                "current_people": location_data.get('current_people', 0),
                # Backwards-compatibility alias for older frontends
                "current_crowd": location_data.get('current_people', 0),
                "crowd_level": location_data.get('crowd_level', 'Unknown'),
                "average_people": location_data.get('average_people', 0),
                "max_people": location_data.get('max_people', 0),
                "description": city_info['description']
            },
            "live_analysis": {
                "frames": live_frames,
                "video_path": video_path
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        import traceback
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route('/api/process-kerala-videos', methods=['POST'])
def process_kerala_videos():
    """Process all Kerala city videos"""
    try:
        results = []
        cities_processed = 0
        
        for city_name, city_info in KERALA_CITIES.items():
            video_path = city_info['video_file']
            
            if not os.path.exists(video_path):
                results.append({
                    "city": city_name,
                    "status": "skipped",
                    "reason": f"Video not found: {video_path}"
                })
                continue
            
            try:
                # Process video
                stats = video_processor.process_location_video(
                    video_path,
                    city_name,
                    city_info['coordinates']
                )
                
                # Store data
                data_manager.save_location_data(city_name, stats, city_info['coordinates'])
                
                results.append({
                    "city": city_name,
                    "status": "processed",
                    "people_count": stats['current_people'],
                    "crowd_level": stats['crowd_level']
                })
                cities_processed += 1
                
            except Exception as e:
                results.append({
                    "city": city_name,
                    "status": "error",
                    "error": str(e)
                })
        
        return jsonify({
            "success": True,
            "processed": cities_processed,
            "total": len(KERALA_CITIES),
            "results": results
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/live-analysis/<city_name>', methods=['GET'])
def get_live_analysis(city_name):
    """Get live video analysis frames for a city"""
    try:
        city_info = get_city_by_name(city_name)
        if not city_info:
            return jsonify({"error": f"City '{city_name}' not found"}), 404
        
        video_path = city_info['video_file']
        if not os.path.exists(video_path):
            return jsonify({"error": f"Video not found: {video_path}"}), 404
        
        # Get sample frames with YOLO detection
        frames = live_analyzer.get_sample_frames(video_path, num_frames=10)
        
        return jsonify({
            "success": True,
            "city": city_name,
            "frames": frames
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/live-stream/<city_name>')
def live_stream(city_name):
    """MJPEG stream of live YOLO annotated frames for a city video"""
    city_info = get_city_by_name(city_name)
    if not city_info:
        return jsonify({"error": f"City '{city_name}' not found"}), 404

    video_path = city_info['video_file']
    if not os.path.exists(video_path):
        return jsonify({"error": f"Video not found: {video_path}"}), 404

    def generate():
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    # loop video
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue

                annotated_frame, person_count, _ = live_analyzer.analyze_frame(frame)
                # Encode as JPEG
                success, buffer = cv2.imencode('.jpg', annotated_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
                if not success:
                    continue
                frame_bytes = buffer.tobytes()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

                # control streaming framerate
                time.sleep(0.1)
        finally:
            cap.release()

    return Response(stream_with_context(generate()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/api/cities', methods=['GET'])
def get_cities():
    """Get all Kerala cities"""
    try:
        # Force reload to ensure fresh data
        data_manager.load_data()
        
        cities = []
        for city_name, city_info in KERALA_CITIES.items():
            location_data = data_manager.get_location_data(city_name)
            cities.append({
                "name": city_name,
                "description": city_info['description'],
                "coordinates": city_info['coordinates'],
                "video_file": city_info['video_file'],
                "processed": location_data is not None,
                "current_people": location_data.get('current_people', 0) if location_data else None,
                # Backwards-compatibility alias for older frontends
                "current_crowd": location_data.get('current_people', 0) if location_data else None,
                "crowd_level": location_data.get('crowd_level', 'Unknown') if location_data else 'Not Processed'
            })
        
        return jsonify({
            "success": True,
            "cities": cities
        }), 200
    except Exception as e:
        import traceback
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

# Serve frontend static files in production
from flask import send_from_directory

@app.route('/')
def serve_index():
    """Serve frontend index"""
    # Try multiple paths to find frontend (works in both local and Docker)
    possible_paths = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend'),
        '/app/frontend',  # Docker path
        'frontend'  # Relative from backend
    ]
    
    for frontend_dir in possible_paths:
        index_path = os.path.join(frontend_dir, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(frontend_dir, 'index.html')
    
    # Fallback to JSON if frontend not found
    return jsonify({"status": "API is running", "message": "Frontend not found", "debug": {"tried_paths": possible_paths}}), 200

@app.route('/<path:path>')
def serve_frontend(path):
    """Serve frontend static files"""
    # Try multiple paths to find frontend (works in both local and Docker)
    possible_paths = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend'),
        '/app/frontend',  # Docker path
        'frontend'  # Relative from backend
    ]
    
    frontend_dir = None
    for possible_dir in possible_paths:
        if os.path.exists(possible_dir):
            frontend_dir = possible_dir
            break
    
    if not frontend_dir:
        return jsonify({"error": "Frontend directory not found"}), 404
    
    # Don't serve API routes
    if path.startswith('api/'):
        return jsonify({"error": "Not found"}), 404
    
    # Serve static files
    file_path = os.path.join(frontend_dir, path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_from_directory(frontend_dir, path)
    
    # For SPA routing, serve index.html
    if '.' not in path or path.endswith('/'):
        index_path = os.path.join(frontend_dir, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(frontend_dir, 'index.html')
    
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    # Create data and videos directories if they don't exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('videos', exist_ok=True)
    
    # Get port from environment (Cloud Run) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print("=" * 60)
    print("Kerala Cities Crowd Detection Backend")
    print("=" * 60)
    print("Available Cities:")
    for city_name in KERALA_CITIES.keys():
        print(f"  - {city_name}")
    print("=" * 60)
    print("API Endpoints:")
    print("   POST /api/ask - Query about any Kerala city")
    print("   POST /api/process-kerala-videos - Process all city videos")
    print("   GET  /api/cities - Get all cities info")
    print("   GET  /api/live-analysis/<city> - Get live analysis frames")
    print("=" * 60)
    print(f"Starting server on port {port} (debug={debug})")
    print("=" * 60)
    
    app.run(debug=debug, host='0.0.0.0', port=port)
