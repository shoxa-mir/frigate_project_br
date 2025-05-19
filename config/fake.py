import cv2
import time
import json
import random
from multiprocessing import Process
import paho.mqtt.publish as publish

MQTT_HOST = "localhost"
MQTT_PORT = 1883

CAMERA_CONFIGS = {
    "name_your_rtsp_cam": "rtsp://admin:pass@127.0.0.1:8554/name_your_rtsp_cam",
}

def fake_yolo(frame):
    # Simulate detection with random boxes
    h, w, _ = frame.shape
    x1, y1 = random.randint(0, w//2), random.randint(0, h//2)
    x2, y2 = x1 + random.randint(50, 150), y1 + random.randint(50, 150)
    return [{
        "label": "object",
        "confidence": round(random.uniform(0.7, 0.99), 2),
        "bbox": [x1, y1, x2, y2]
    }]

def send_mqtt(camera_name, detections):
    payload = {
        "timestamp": int(time.time()),
        "objects": detections
    }
    publish.single(
        f"frigate/detect/{camera_name}",
        json.dumps(payload),
        hostname=MQTT_HOST,
        port=MQTT_PORT
    )

def camera_worker(camera_name, stream_url):
    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        print(f"[{camera_name}] ❌ Could not open stream")
        return

    print(f"[{camera_name}] ✅ Started processing")

    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"[{camera_name}] ❌ Frame grab failed")
            time.sleep(1)
            continue

        detections = fake_yolo(frame)
        send_mqtt(camera_name, detections)

        # Slow down to simulate real inference
        time.sleep(1)

if __name__ == "__main__":
    processes = []

    for cam_name, stream_url in CAMERA_CONFIGS.items():
        p = Process(target=camera_worker, args=(cam_name, stream_url))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
