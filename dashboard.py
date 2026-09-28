import pandas as pd
import matplotlib.pyplot as plt


# ==============================
# LOAD DATA
# ==============================

df = pd.read_csv(
    "events.csv",
    on_bad_lines="skip"
)


print("\n===== GUARDIAN VISION DASHBOARD =====\n")


# ==============================
# STATISTICS
# ==============================

total_events = len(df)

average_confidence = df["Confidence"].mean()

risk_counts = df["Risk"].value_counts()

object_counts = df["Object"].value_counts()


print("Total Events:", total_events)

print("\nRisk Summary:")
print(risk_counts)

print("\nObjects Detected:")
print(object_counts)

print("\nAverage Confidence:")
print(f"{average_confidence:.2f}%")


# ==============================
# CREATE DASHBOARD
# ==============================

fig, axes = plt.subplots(
    2,
    1,
    figsize=(10, 9)
)

fig.suptitle(
    "GUARDIAN VISION - AI SECURITY DASHBOARD",
    fontsize=16
)


# ==============================
# RISK GRAPH
# ==============================

risk_counts.plot(
    kind="bar",
    ax=axes[0]
)

axes[0].set_title(
    "Risk Detection"
)

axes[0].set_xlabel(
    "Risk Level"
)

axes[0].set_ylabel(
    "Number of Events"
)

axes[0].tick_params(
    axis="x",
    rotation=0
)


# ==============================
# OBJECT GRAPH
# ==============================

object_counts.plot(
    kind="bar",
    ax=axes[1]
)

axes[1].set_title(
    "Objects Detected"
)

axes[1].set_xlabel(
    "Object"
)

axes[1].set_ylabel(
    "Number of Detections"
)

axes[1].tick_params(
    axis="x",
    rotation=45
)


# ==============================
# FINAL LAYOUT
# ==============================

plt.tight_layout()

plt.show()