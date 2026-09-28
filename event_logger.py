import csv
from datetime import datetime


FILE_NAME = "events.csv"


def log_event(object_name, confidence, risk_level):

    current_time = datetime.now()

    with open(
        FILE_NAME,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        # New CSV file
        if file.tell() == 0:

            writer.writerow([
                "Date",
                "Time",
                "Object",
                "Confidence",
                "Risk"
            ])

        writer.writerow([
            current_time.strftime("%Y-%m-%d"),
            current_time.strftime("%H:%M:%S"),
            object_name,
            round(confidence, 2),
            risk_level
        ])

    print("Event saved to events.csv")