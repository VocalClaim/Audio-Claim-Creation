import json
import re


def validate_payload(payload_str):
    try:
        json.loads(payload_str)
        return True
    except json.JSONDecodeError:
        return False

        
def format_payload(transcribed_text):
    def extract_field(pattern, text, default="N/A"):
        match = re.search(pattern, text)
        return match.group(1).strip() if match else default

    # Define patterns to extract data from transcribed text
    patterns = {
        "policy_number": r"policy number (\S+)",
        "incident_date": r"incident occurred on (\S+ \d+ \d+)",
        "incident_time": r"at (\d{1,2}:\d{2} \w{2})",
        "intersection": r"intersection of (.+?) and",
        "insured_name": r"ensure name",
        "insured_address": r"resides at (\d+ \S+)",
        "work_phone": r"work phone number (\d+)",
        "home_phone": r"home phone number (\d+)",
        "mobile_phone": r"mobile phone number (\d+)",
        "email": r"(\S+@[\S+\.]+)",
        "accident_number": r"accident number (\d+)",
        "system_damage": r"system damage",
        "considered_for": r"considered for"
    }

    extracted_data = {field: extract_field(pattern, transcribed_text) for field, pattern in patterns.items()}

    # Construct the payload
    payload = {
        "policy_number": extracted_data["policy_number"],
        "LossDate": f"{extracted_data['incident_date']} {extracted_data['incident_time']}",
        "incident": {
            "date": extracted_data["incident_date"],
            "time": extracted_data["incident_time"],
            "location": {
                "intersection": extracted_data["intersection"]
            }
        },
        "insured": {
            "name": extracted_data["insured_name"],
            "address": extracted_data["insured_address"],
            "contact": {
                "work_phone": extracted_data["work_phone"],
                "home_phone": extracted_data["home_phone"],
                "mobile_phone": extracted_data["mobile_phone"],
                "email": extracted_data["email"]
            }
        },
        "accident": {
            "number": extracted_data["accident_number"],
            "system_damage": extracted_data["system_damage"],
            "considered_for": extracted_data["considered_for"]
        }
    }

    try:
        json_payload = json.dumps(payload, indent=4)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Error formatting payload: {str(e)}")

    return json_payload
