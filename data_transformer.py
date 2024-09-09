import json
import logging
from nlp_processing.model.llm_inference import infer_payload

# Set up logging
logging.basicConfig(filename='data_transformer.log', level=logging.INFO)

DEFAULTS = {
    "NotifiedOnBehalfOf": "Company XYZ",
    "PolicyNumber": "P123456789",
    "LossDate": "2024-05-10T08:00:00Z",
    "InsuredVRN": "VRN123",
    "ReportersCompanyName": "Reporter Company",
    "ReportersFirstName": "John",
    "ReportersLastName": "Doe",
    "ReportersAddress": "123 Main Street",
    "ReportersWorkPhoneNumber": "123-456-7890",
    "ReportersHomePhoneNumber": "987-654-3210",
    "ReportersMobilePhoneNumber": "789-456-1230",
    "ReportersEmail": "john.doe@example.com",
    "ReportersReference": "Ref123",
    "VATStatus": "VAT Registered",
    "NoticeDate": "2024-05-10T08:30:00Z",
    "WhatHappened": "Accident occurred",
    "IncidentOnly": False,
    "Liability": "Other party at fault",
    "LossLocation": "Main Street",
    "ClaimPersonalEffects": "No",
    "IsVehicleDamaged": "Yes",
    "IsVehicleOperable": "Yes",
    "DamageDescription": "Front bumper damage",
    "ClaimVehicleDamage": "Yes",
    "FirstName": "Alice",
    "LastName": "Smith",
    "Unknown": "No",
    "Address": "789 Oak Avenue",
    "Email": "alice.smith@example.com",
    "WorkPhoneNumber": "456-123-7890",
    "HomePhoneNumber": "789-321-6540",
    "MobilePhoneNumber": "987-654-3210",
    "DateOfBirth": "1990-01-01",
    "DateOfBirthKnown": "Yes",
    "DrivingLicenseType": "Type B",
    "UKResidency": "Yes",
    "Occupation": "Driver",
    "Injuries": "Yes",
    "ThirdPartyVRN": "VRN789",
    "ThirdPartyVRNUnknown": "No",
    "OwnerCompanyName": "Third Party Company",
    "OwnerFirstName": "Jane",
    "OwnerSurname": "Doe",
    "IsVehicleDamaged": "Yes",
    "IsVehicleOperable": "No",
    "DamageDescription": "Rear-end collision damage",
    "OwnerPhoneNumber": "654-789-1230",
    "OwnerEmail": "jane.doe@example.com"
}

def log_error(message):
    logging.error(message)

def validate_input_data(data):
    required_fields = ["GraphID", "PolicyNumber", "LossDate", "InsuredVRN"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(f"Missing required fields: {missing_fields}")

def transform_data(data, defaults=DEFAULTS):
    # Validate the input data
    try:
        validate_input_data(data)
    except ValueError as ve:
        log_error(f"Validation Error: {ve}")
        return None

    # Convert input data to JSON string to prepare for LLM input
    input_context = json.dumps(data)
    
    try:
        # Infer missing fields using LLM and parse the response into a dictionary
        llm_output = infer_payload(input_context)
        llm_predicted_data = json.loads(llm_output)  # Convert the LLM output back to a dictionary

        # Merge original data, inferred data, and defaults
        transformed_data = {
            "GraphID": data.get("GraphID", llm_predicted_data.get("GraphID", "")),
            "NotifiedOnBehalfOf": data.get("NotifiedOnBehalfOf", llm_predicted_data.get("NotifiedOnBehalfOf", defaults["NotifiedOnBehalfOf"])),
            "PolicyNumber": data.get("PolicyNumber", llm_predicted_data.get("PolicyNumber", defaults["PolicyNumber"])),
            "LossDate": data.get("LossDate", llm_predicted_data.get("LossDate", defaults["LossDate"])),
            "InsuredVRN": data.get("InsuredVRN", llm_predicted_data.get("InsuredVRN", defaults["InsuredVRN"])),
            "ReportersCompanyName": data.get("ReportersCompanyName", llm_predicted_data.get("ReportersCompanyName", defaults["ReportersCompanyName"])),
            "ReportersFirstName": data.get("ReportersFirstName", llm_predicted_data.get("ReportersFirstName", defaults["ReportersFirstName"])),
            "ReportersLastName": data.get("ReportersLastName", llm_predicted_data.get("ReportersLastName", defaults["ReportersLastName"])),
            "ReportersAddress": data.get("ReportersAddress", llm_predicted_data.get("ReportersAddress", defaults["ReportersAddress"])),
            "ReportersWorkPhoneNumber": data.get("ReportersWorkPhoneNumber", llm_predicted_data.get("ReportersWorkPhoneNumber", defaults["ReportersWorkPhoneNumber"])),
            "ReportersHomePhoneNumber": data.get("ReportersHomePhoneNumber", llm_predicted_data.get("ReportersHomePhoneNumber", defaults["ReportersHomePhoneNumber"])),
            "ReportersMobilePhoneNumber": data.get("ReportersMobilePhoneNumber", llm_predicted_data.get("ReportersMobilePhoneNumber", defaults["ReportersMobilePhoneNumber"])),
            "ReportersEmail": data.get("ReportersEmail", llm_predicted_data.get("ReportersEmail", defaults["ReportersEmail"])),
            "ReportersReference": data.get("ReportersReference", llm_predicted_data.get("ReportersReference", defaults["ReportersReference"])),
            "InsuredContactDetails": {
                "InsuredName": data.get("InsuredName", llm_predicted_data.get("InsuredName", "Insured Name")),
                "InsuredAddress": data.get("InsuredAddress", llm_predicted_data.get("InsuredAddress", "456 Elm Street")),
                "InsuredEmail": data.get("InsuredEmail", llm_predicted_data.get("InsuredEmail", "insured@example.com")),
                "InsuredWorkPhoneNumber": data.get("InsuredWorkPhoneNumber", llm_predicted_data.get("InsuredWorkPhoneNumber", "456-789-0123")),
                "InsuredHomePhoneNumber": data.get("InsuredHomePhoneNumber", llm_predicted_data.get("InsuredHomePhoneNumber", "321-654-0987")),
                "InsuredMobilePhoneNumber": data.get("InsuredMobilePhoneNumber", llm_predicted_data.get("InsuredMobilePhoneNumber", "987-654-3210")),
                "VATStatus": data.get("VATStatus", llm_predicted_data.get("VATStatus", defaults["VATStatus"]))
            },
            "NoticeDate": data.get("NoticeDate", llm_predicted_data.get("NoticeDate", defaults["NoticeDate"])),
            "ClaimInformation": {
                "WhatHappened": data.get("WhatHappened", llm_predicted_data.get("WhatHappened", defaults["WhatHappened"])),
                "IncidentOnly": data.get("IncidentOnly", llm_predicted_data.get("IncidentOnly", defaults["IncidentOnly"])),
                "Liability": data.get("Liability", llm_predicted_data.get("Liability", defaults["Liability"])),
                "LossLocation": data.get("LossLocation", llm_predicted_data.get("LossLocation", defaults["LossLocation"]))
            },
            "VehicleDetails": {
                "ClaimPersonalEffects": data.get("ClaimPersonalEffects", llm_predicted_data.get("ClaimPersonalEffects", defaults["ClaimPersonalEffects"])),
                "IsVehicleDamaged": data.get("IsVehicleDamaged", llm_predicted_data.get("IsVehicleDamaged", defaults["IsVehicleDamaged"])),
                "IsVehicleOperable": data.get("IsVehicleOperable", llm_predicted_data.get("IsVehicleOperable", defaults["IsVehicleOperable"])),
                "DamageDescription": data.get("DamageDescription", llm_predicted_data.get("DamageDescription", defaults["DamageDescription"])),
                "ClaimVehicleDamage": data.get("ClaimVehicleDamage", llm_predicted_data.get("ClaimVehicleDamage", defaults["ClaimVehicleDamage"]))
            },
            "DriverDetails": {
                "FirstName": data.get("FirstName", llm_predicted_data.get("FirstName", defaults["FirstName"])),
                "LastName": data.get("LastName", llm_predicted_data.get("LastName", defaults["LastName"])),
                "Unknown": data.get("Unknown", llm_predicted_data.get("Unknown", defaults["Unknown"])),
                "Address": data.get("Address", llm_predicted_data.get("Address", defaults["Address"])),
                "Email": data.get("Email", llm_predicted_data.get("Email", defaults["Email"])),
                "WorkPhoneNumber": data.get("WorkPhoneNumber", llm_predicted_data.get("WorkPhoneNumber", defaults["WorkPhoneNumber"])),
                "HomePhoneNumber": data.get("HomePhoneNumber", llm_predicted_data.get("HomePhoneNumber", defaults["HomePhoneNumber"])),
                "MobilePhoneNumber": data.get("MobilePhoneNumber", llm_predicted_data.get("MobilePhoneNumber", defaults["MobilePhoneNumber"])),
                "DateOfBirth": data.get("DateOfBirth", llm_predicted_data.get("DateOfBirth", defaults["DateOfBirth"])),
                "DateOfBirthKnown": data.get("DateOfBirthKnown", llm_predicted_data.get("DateOfBirthKnown", defaults["DateOfBirthKnown"])),
                "DrivingLicenseType": data.get("DrivingLicenseType", llm_predicted_data.get("DrivingLicenseType", defaults["DrivingLicenseType"])),
                "UKResidency": data.get("UKResidency", llm_predicted_data.get("UKResidency", defaults["UKResidency"])),
                "Occupation": data.get("Occupation", llm_predicted_data.get("Occupation", defaults["Occupation"])),
                "Injuries": data.get("Injuries", llm_predicted_data.get("Injuries", defaults["Injuries"]))
            },
            "ThirdPartyDetails": {
                "ThirdPartyVRN": data.get("ThirdPartyVRN", llm_predicted_data.get("ThirdPartyVRN", defaults["ThirdPartyVRN"])),
                "ThirdPartyVRNUnknown": data.get("ThirdPartyVRNUnknown", llm_predicted_data.get("ThirdPartyVRNUnknown", defaults["ThirdPartyVRNUnknown"])),
                "OwnerCompanyName": data.get("OwnerCompanyName", llm_predicted_data.get("OwnerCompanyName", defaults["OwnerCompanyName"])),
                "OwnerFirstName": data.get("OwnerFirstName", llm_predicted_data.get("OwnerFirstName", defaults["OwnerFirstName"])),
                "OwnerSurname": data.get("OwnerSurname", llm_predicted_data.get("OwnerSurname", defaults["OwnerSurname"])),
                "IsVehicleDamaged": data.get("IsVehicleDamaged", llm_predicted_data.get("IsVehicleDamaged", defaults["IsVehicleDamaged"])),
                "IsVehicleOperable": data.get("IsVehicleOperable", llm_predicted_data.get("IsVehicleOperable", defaults["IsVehicleOperable"])),
                "DamageDescription": data.get("DamageDescription", llm_predicted_data.get("DamageDescription", defaults["DamageDescription"])),
                "OwnerPhoneNumber": data.get("OwnerPhoneNumber", llm_predicted_data.get("OwnerPhoneNumber", defaults["OwnerPhoneNumber"])),
                "OwnerEmail": data.get("OwnerEmail", llm_predicted_data.get("OwnerEmail", defaults["OwnerEmail"]))
            }
        }

        return transformed_data  # Return the merged and transformed data

    except json.JSONDecodeError:
        log_error("Error parsing LLM output: Failed to decode JSON.")
        return None
    except Exception as e:
        log_error(f"Error in transforming data: {e}")
        return None
