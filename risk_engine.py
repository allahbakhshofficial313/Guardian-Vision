def check_risk(object_name, confidence):

    if object_name != "person":
        return "IGNORE"

    if confidence >= 90:
        return "HIGH RISK"

    if confidence >= 80:
        return "WARNING"

    if confidence >= 60:
        return "NORMAL"

    return "IGNORE"