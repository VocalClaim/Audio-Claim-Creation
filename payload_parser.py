# payload_parser.py

import re

def parse_text_to_payload(text):
    """
    Parse transcribed text into a structured payload.
    """
    def safe_search(pattern, text):
        match = re.search(pattern, text)
        return match.group(1) if match else None

    payload = {
        "GraphID": "12345",  # Default or extracted value
        "NotifiedOnBehalfOf": "Reporter Company",
        "PolicyNumber": safe_search(r'policy number (\S+)', text),
        "LossDate": "2024-05-10T08:00:00Z",  # Adjust based on text
        "InsuredVRN": safe_search(r'VRN (\S+)', text),
        "ReportersCompanyName": "Reporter Company",
        "ReportersFirstName": "John",
        "ReportersLastName": "Doe",  # Adjust based on text
        "ReportersAddress": safe_search(r'address (\d+ \S+)', text),
        "ReportersWorkPhoneNumber": safe_search(r'work phone number (\S+)', text),
        "ReportersHomePhoneNumber": safe_search(r'home phone number (\S+)', text),
        "ReportersMobilePhoneNumber": safe_search(r'mobile phone number (\S+)', text),
        "ReportersEmail": safe_search(r'email\.com', text),
        "ReportersReference": safe_search(r'accident number (\S+)', text),
        "InsuredContactDetails": {
            "InsuredName": "Insured Name",
            "InsuredAddress": "456 Elm Street",
            "InsuredEmail": "insured@example.com",
            "InsuredWorkPhoneNumber": "456-789-0123",
            "InsuredHomePhoneNumber": "321-654-0987",
            "InsuredMobilePhoneNumber": "987-654-3210",
            "VATStatus": "VAT Registered"
        },
        "NoticeDate": "2024-05-10T08:30:00Z",
        "ClaimInformation": {
            "WhatHappened": safe_search(r'Accident occurred', text),
            "IncidentOnly": False,
            "Liability": "Other party at fault",
            "LossLocation": "Intersection of Main Street and Downstream"
        },
        "VehicleDetails": {
            "ClaimPersonalEffects": "No",
            "IsVehicleDamaged": "Yes",
            "IsVehicleOperable": "Yes",
            "DamageDescription": "Description of damage",
            "ClaimVehicleDamage": "Yes"
        },
        "DriverDetails": {
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
            "Injuries": "Yes"
        },
        "ThirdPartyVehicleDetails": [
            {
                "ThirdPartyVRN": "VRN789",
                "ThirdPartyVRNUnknown": "No",
                "OwnerCompanyName": "Third Party Company",
                "OwnerFirstName": "Jane",
                "OwnerSurname": "Doe",
                "IsVehicleDamaged": "Yes",
                "DamageDescription": "Rear-end collision",
                "ClaimVehicleDamage": "Yes",
                "ClaimThroughAXA": "No",
                "ThirdPartyCreditHire": "Yes",
                "CurrentLocation": "Garage",
                "IsVehicleOperable": "No",
                "ThirdPartyFaultRating": "High"
            }
        ],
        "ThirdPartyDriverDetails": [
            {
                "FirstName": "Bob",
                "LastName": "Johnson",
                "Unknown": "Yes",
                "Address": "",
                "Email": "",
                "HomePhoneNumber": "",
                "MobilePhoneNumber": "",
                "Injuries": "No"
            }
        ],
        "ThirdPartyPropertyDetails": {
            "OwnerCompanyName": "Property Owner Company",
            "OwnerFirstName": "John",
            "OwnerLastName": "Doe",
            "PropertyName": "123 Elm Street"
        },
        "EmergencyServiceDetails": [
            {
                "Type": "Ambulance",
                "Name": "City Ambulance Service",
                "ReportNumber": "RS12345"
            },
            {
                "Type": "Police",
                "Name": "City Police Department",
                "ReportNumber": "PR67890"
            }
        ]
    }
    return payload
