"""
Live video person detection with real-time display
Shows the model working on video in real-time
"""
from person_detector import PersonDetector
import cv2
import sys

def detect_video_live(video_path, save_output=False, output_path=None):
    """
    Process video and display detections live
    
    Args:
        video_path: Path to input video file
        save_output: Whether to save the annotated video
        output_path: Path to save output video (if save_output=True)
    """
    print("=" * 60)
    print("Live Video Person Detection")
    print("=" * 60)
    
    # Initialize detector
    detector = PersonDetector(model_path="yolov8n.pt", confidence_threshold=0.25)
    
    # Open video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ Error: Could not open video file: {video_path}")
        return
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"\n📹 Video Info:")
    print(f"   Resolution: {width}x{height}")
    print(f"   FPS: {fps}")
    print(f"   Total frames: {total_frames}")
    print(f"\n🎬 Starting live detection...")
    print(f"   Press 'q' to quit")
    print(f"   Press 's' to save current frame")
    print("=" * 60)
    
    # Video writer for output (if saving)
    out = None
    if save_output:
        if not output_path:
            output_path = f"output_{video_path.split('/')[-1].split('.')[0]}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        print(f"💾 Saving output to: {output_path}")
    
    frame_count = 0
    person_counts = []
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Run YOLOv8 inference on frame
            results = detector.model(frame, conf=detector.confidence_threshold, classes=[detector.person_class_id])
            
            person_count = 0
            
            # Process detections and draw on frame
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    if int(box.cls) == detector.person_class_id:
                        person_count += 1
                        confidence = float(box.conf)
                        bbox = box.xyxy[0].cpu().numpy()
                        
                        # Draw bounding box
                        x1, y1, x2, y2 = map(int, bbox)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        
                        # Draw confidence score
                        label = f"Person {person_count} ({confidence:.2f})"
                        (text_width, text_height), baseline = cv2.getTextSize(
                            label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2
                        )
                        cv2.rectangle(frame, (x1, y1 - text_height - 10), 
                                    (x1 + text_width, y1), (0, 255, 0), -1)
                        cv2.putText(frame, label, (x1, y1 - 5), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            
            person_counts.append(person_count)
            crowd_level = detector._classify_crowd_level(person_count)
            
            # Add overlay text with stats
            overlay_text = [
                f"People: {person_count}",
                f"Crowd Level: {crowd_level}",
                f"Frame: {frame_count}/{total_frames}",
                f"FPS: {fps}"
            ]
            
            # Draw semi-transparent background for text
            overlay = frame.copy()
            cv2.rectangle(overlay, (10, 10), (350, 120), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
            
            # Draw text
            y_offset = 35
            for i, text in enumerate(overlay_text):
                color = (0, 255, 0) if i == 0 else (255, 255, 255)
                cv2.putText(frame, text, (20, y_offset + i * 25), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            # Save frame if requested
            if out:
                out.write(frame)
            
            # Display frame
            cv2.imshow('Live Person Detection', frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\n⏹️  Stopped by user")
                break
            elif key == ord('s'):
                screenshot_path = f"screenshot_frame_{frame_count}.jpg"
                cv2.imwrite(screenshot_path, frame)
                print(f"📸 Saved screenshot: {screenshot_path}")
            
            frame_count += 1
            
            # Print progress every 30 frames
            if frame_count % 30 == 0:
                avg_people = sum(person_counts[-30:]) / min(30, len(person_counts))
                print(f"   Frame {frame_count}/{total_frames} | Current: {person_count} people | Avg (last 30): {avg_people:.1f}")
    
    except KeyboardInterrupt:
        print("\n⏹️  Interrupted by user")
    
    finally:
        # Cleanup
        cap.release()
        if out:
            out.release()
        cv2.destroyAllWindows()
        
        # Print final statistics
        if person_counts:
            avg_people = sum(person_counts) / len(person_counts)
            max_people = max(person_counts)
            min_people = min(person_counts)
            overall_level = detector._classify_crowd_level(int(avg_people))
            
            print("\n" + "=" * 60)
            print("📊 Final Statistics:")
            print("=" * 60)
            print(f"   Total frames processed: {frame_count}")
            print(f"   Average people per frame: {avg_people:.2f}")
            print(f"   Maximum people in a frame: {max_people}")
            print(f"   Minimum people in a frame: {min_people}")
            print(f"   Overall crowd level: {overall_level}")
            if save_output:
                print(f"   Output video saved to: {output_path}")
            print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_video_live.py <video_path> [--save] [--output output.mp4]")
        print("\nExample:")
        print("  python test_video_live.py my_video.mp4")
        print("  python test_video_live.py my_video.mp4 --save")
        print("  python test_video_live.py my_video.mp4 --save --output result.mp4")
        sys.exit(1)
    
    video_path = sys.argv[1]
    save_output = "--save" in sys.argv
    output_path = None
    
    if "--output" in sys.argv:
        output_idx = sys.argv.index("--output")
        if output_idx + 1 < len(sys.argv):
            output_path = sys.argv[output_idx + 1]
    
    detect_video_live(video_path, save_output=save_output, output_path=output_path)





