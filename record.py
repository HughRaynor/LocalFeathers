import cv2
import os
import time
from datetime import datetime, timedelta

def initialize_camera(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)
    return cap

def wait_for_reconnect(delay=60):
    print(f"Camera disconnected. Retrying in {delay} seconds...")
    log_connection_event("Camera disconnected.")
    time.sleep(delay)

def log_connection_event(event):
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'connection_log.txt')
    with open(log_file, 'a') as f:
        f.write(f"{datetime.now()}: {event}\n")

try:
    # RTSP stream URL - Update before running!
    rtsp_url = 'rtsp://cameraIP:8554/main'

    # Directory to save videos (same directory as the script)
    save_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(save_dir, exist_ok=True)

    # Duration to keep videos (in days)
    retention_days = 30

    # Initialize camera
    cap = initialize_camera(rtsp_url)

    while True:
        # Check if camera is opened successfully
        if not cap.isOpened():
            wait_for_reconnect()
            cap.release()
            cap = initialize_camera(rtsp_url)
            if cap.isOpened():
                log_connection_event("Camera reconnected.")
            continue

        # Create a unique filename with timestamp
        filename = os.path.join(save_dir, datetime.now().strftime('%Y-%m-%d %H-%M-%S') + '.mp4')

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(filename, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

        start_time = time.time()
        while int(time.time() - start_time) < 900:  # Record for 15 minutes (900 seconds)
            ret, frame = cap.read()
            if ret:
                out.write(frame)
            else:
                out.release()
                wait_for_reconnect()
                cap.release()
                cap = initialize_camera(rtsp_url)
                if cap.isOpened():
                    log_connection_event("Camera reconnected.")
                break

        out.release()

        # Delete files older than retention period
        for f in os.listdir(save_dir):
            file_path = os.path.join(save_dir, f)
            if os.path.isfile(file_path):
                file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                if datetime.now() - file_time > timedelta(days=retention_days):
                    os.remove(file_path)

    # Release the capture
    cap.release()
    cv2.destroyAllWindows()

except Exception as e:
    print(f"Exception occurred: {str(e)}. Press Enter to exit.")
    input()
