import requests


TOPIC = "GuardianVision_A7k92X"


def send_alert(risk_level, object_name, confidence):

    if risk_level == "HIGH RISK":

        message = (
            f"🚨 GUARDIAN VISION ALERT\n"
            f"Object: {object_name}\n"
            f"Confidence: {confidence:.2f}%\n"
            f"Risk: HIGH RISK"
        )

        try:
            requests.post(
                f"https://ntfy.sh/{TOPIC}",
                data=message.encode("utf-8"),
                headers={
                    "Title": "Guardian Vision Alert",
                    "Priority": "urgent"
                }
            )

            print("📱 Mobile alert sent!")

        except Exception as e:
            print("Mobile alert error:", e)


    elif risk_level == "WARNING":

        print(
            f"⚠️ WARNING | "
            f"{object_name} | "
            f"{confidence:.2f}%"
        )