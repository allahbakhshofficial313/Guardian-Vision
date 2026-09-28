# Guardian Vision

AI-based camera security system using YOLO object detection.

## Features

- Real-time person detection
- Confidence score
- Risk classification
- Event logging
- CSV data storage
- Risk dashboard
- Mobile notifications using ntfy
- Automatic HIGH RISK alerts
- 10-second alert cooldown

## Technologies

- Python
- OpenCV
- YOLO
- Ultralytics
- Pandas
- Matplotlib
- ntfy

## Risk Levels

- 60–79% → NORMAL
- 80–89% → WARNING
- 90%+ → HIGH RISK

## Run Guardian Vision

```bash
python main.py