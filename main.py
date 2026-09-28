import cv2
import time
import os

from ultralytics import YOLO

from event_logger import log_event
from risk_engine import check_risk
from alert_engine import send_alert


# ==============================
# 1. LOAD AI MODEL
# ==============================

print("Loading Guardian Vision AI...")

model = YOLO("yolo11n.pt")


# ==============================
# 2. OPEN CAMERA
# ==============================

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERROR: Camera open nahi ho raha.")
    input("Enter press karke exit karein...")
    exit()

print("Camera opened successfully!")
print("Q = Exit")


# ==============================
# 3. FOLDERS
# ==============================

os.makedirs("recordings", exist_ok=True)
os.makedirs("snapshots", exist_ok=True)


# ==============================
# 4. VIDEO RECORDING
# ==============================

frame_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

record_fps = 15.0

video_file = time.strftime(
    "recordings/guardian_%Y-%m-%d_%H-%M-%S.mp4"
)

fourcc = cv2.VideoWriter_fourcc(*"mp4v")

video_writer = cv2.VideoWriter(
    video_file,
    fourcc,
    record_fps,
    (frame_width, frame_height)
)

if not video_writer.isOpened():
    print("ERROR: Video recording start nahi ho rahi.")
    camera.release()
    exit()

print("Recording started:")
print(video_file)


# ==============================
# 5. ALERT COOLDOWN
# ==============================

last_normal_warning_event = 0
cooldown = 10


# ==============================
# 6. RECORDING TIMER
# ==============================

next_frame_time = time.perf_counter()
frame_interval = 1.0 / record_fps


# ==============================
# 7. CAMERA LOOP
# ==============================

while True:

    success, frame = camera.read()

    if not success:
        print("ERROR: Camera frame nahi mil raha.")
        break


    # ==============================
    # YOLO DETECTION
    # ==============================

    results = model(frame, verbose=False)


    # ==============================
    # DRAW DETECTIONS
    # ==============================

    annotated_frame = results[0].plot()


    # ==============================
    # CHECK ALL OBJECTS
    # ==============================

    for result in results:

        for box in result.boxes:

            class_id = int(box.cls[0])

            confidence = float(box.conf[0]) * 100

            object_name = model.names[class_id]


            # Ignore weak detections
            if confidence < 60:
                continue


            # ==============================
            # PERSON
            # ==============================

            if object_name == "person":

                risk_level = check_risk(
                    object_name,
                    confidence
                )

                print(
                    f"Person detected | "
                    f"Confidence: {confidence:.2f}% | "
                    f"Risk: {risk_level}"
                )

                current_time = time.time()


                # ==============================
                # HIGH RISK
                # ==============================

                if risk_level == "HIGH RISK":

                    log_event(
                        object_name,
                        confidence,
                        risk_level
                    )


                    # Snapshot

                    snapshot_file = time.strftime(
                        "snapshots/high_risk_%Y-%m-%d_%H-%M-%S.jpg"
                    )

                    cv2.imwrite(
                        snapshot_file,
                        annotated_frame
                    )

                    print(
                        "HIGH RISK snapshot saved:"
                    )

                    print(snapshot_file)


                    # Mobile alert

                    send_alert(
                        risk_level,
                        object_name,
                        confidence
                    )

                    print(
                        "🚨 HIGH RISK alert sent!"
                    )


                # ==============================
                # NORMAL / WARNING
                # ==============================

                elif current_time - last_normal_warning_event >= cooldown:

                    log_event(
                        object_name,
                        confidence,
                        risk_level
                    )

                    send_alert(
                        risk_level,
                        object_name,
                        confidence
                    )

                    print(
                        "Alert function called:",
                        risk_level
                    )

                    last_normal_warning_event = current_time


            # ==============================
            # OTHER OBJECTS
            # ==============================

            else:

                print(
                    f"Object detected | "
                    f"Name: {object_name} | "
                    f"Confidence: {confidence:.2f}%"
                )


                # Save other objects to CSV

                log_event(
                    object_name,
                    confidence,
                    "INFO"
                )


    # ==============================
    # SAVE VIDEO
    # ==============================

    video_writer.write(annotated_frame)


    # ==============================
    # SHOW CAMERA
    # ==============================

    cv2.imshow(
        "Guardian Vision - AI",
        annotated_frame
    )


    # ==============================
    # EXIT
    # ==============================

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


    # ==============================
    # RECORDING TIMING
    # ==============================

    next_frame_time += frame_interval

    sleep_time = next_frame_time - time.perf_counter()

    if sleep_time > 0:
        time.sleep(sleep_time)
    else:
        next_frame_time = time.perf_counter()


# ==============================
# 8. CLOSE EVERYTHING
# ==============================

camera.release()

video_writer.release()

cv2.destroyAllWindows()


print("Guardian Vision stopped.")

print("Video saved at:")
print(video_file)