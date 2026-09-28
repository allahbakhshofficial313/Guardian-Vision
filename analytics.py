import pandas as pd
import matplotlib.pyplot as plt

FILE_NAME = "events.csv"

# CSV read
data = pd.read_csv(FILE_NAME)

print("\n===== GUARDIAN VISION ANALYTICS =====")

# Total events
print(f"\nTotal Events: {len(data)}")

# Person detections
person_count = (data["Object"] == "person").sum()
print(f"Person Detections: {person_count}")

# Average confidence
average_confidence = data["Confidence"].mean()
print(f"Average Confidence: {average_confidence:.2f}%")

# Create datetime
data["DateTime"] = pd.to_datetime(
    data["Date"] + " " + data["Time"]
)

# Sort by time
data = data.sort_values("DateTime")

# Show data
print("\nDetection Records:")
print(data[["Date", "Time", "Object", "Confidence"]])

# Activity chart
plt.figure(figsize=(10, 5))

plt.plot(
    data["DateTime"],
    data["Confidence"],
    marker="o"
)

plt.title("Guardian Vision - Detection Confidence")
plt.xlabel("Time")
plt.ylabel("Confidence (%)")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()