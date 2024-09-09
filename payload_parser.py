# payload_parser.py
# -------------------------------------------v2-----------------------------------
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

# --------------------------------------V1--------------------------------

# import re

# def safe_search(pattern, text):
#     """
#     Safely search for a pattern in the text.
#     """
#     match = re.search(pattern, text)
#     return match.group(1) if match else None

# def parse_text_to_payload(text):
#     """
#     Parse transcribed text into a structured payload.
#     """
#     payload = {
#         "GraphID": "12345",  # Default or extracted value
#         "NotifiedOnBehalfOf": "Reporter Company",
#         "PolicyNumber": safe_search(r'policy number (\S+)', text),
#         "LossDate": safe_search(r'loss date (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)', text),
#         "InsuredVRN": safe_search(r'VRN (\S+)', text),
#         "ReportersCompanyName": "Reporter Company",
#         "ReportersFirstName": "John",
#         "ReportersLastName": safe_search(r'reporters last name (\S+)', text),
#         "ReportersAddress": safe_search(r'address (\d+ \S+)', text),
#         "ReportersWorkPhoneNumber": safe_search(r'work phone number (\S+)', text),
#         "ReportersHomePhoneNumber": safe_search(r'home phone number (\S+)', text),
#         "ReportersMobilePhoneNumber": safe_search(r'mobile phone number (\S+)', text),
#         "ReportersEmail": safe_search(r'email (\S+@\S+)', text),
#         "ReportersReference": safe_search(r'accident number (\S+)', text),
#         "InsuredContactDetails": {
#             "InsuredName": "Insured Name",
#             "InsuredAddress": "456 Elm Street",
#             "InsuredEmail": "insured@example.com",
#             "InsuredWorkPhoneNumber": "456-789-0123",
#             "InsuredHomePhoneNumber": "321-654-0987",
#             "InsuredMobilePhoneNumber": "987-654-3210",
#             "VATStatus": "VAT Registered"
#         },
#         "NoticeDate": safe_search(r'notice date (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)', text),
#         "ClaimInformation": {
#             "WhatHappened": safe_search(r'Accident occurred (.+)', text),
#             "IncidentOnly": safe_search(r'incident only (True|False)', text) == 'True',
#             "Liability": safe_search(r'liability (.+)', text),
#             "LossLocation": safe_search(r'loss location (.+)', text)
#         },
#         "VehicleDetails": {
#             "ClaimPersonalEffects": safe_search(r'personal effects claimed (Yes|No)', text),
#             "IsVehicleDamaged": safe_search(r'vehicle damaged (Yes|No)', text),
#             "IsVehicleOperable": safe_search(r'vehicle operable (Yes|No)', text),
#             "DamageDescription": safe_search(r'damage description (.+)', text),
#             "ClaimVehicleDamage": safe_search(r'vehicle damage claimed (Yes|No)', text)
#         },
#         "DriverDetails": {
#             "FirstName": safe_search(r'driver first name (\S+)', text),
#             "LastName": safe_search(r'driver last name (\S+)', text),
#             "Unknown": safe_search(r'driver unknown (Yes|No)', text),
#             "Address": safe_search(r'driver address (\d+ \S+)', text),
#             "Email": safe_search(r'driver email (\S+@\S+)', text),
#             "WorkPhoneNumber": safe_search(r'driver work phone number (\S+)', text),
#             "HomePhoneNumber": safe_search(r'driver home phone number (\S+)', text),
#             "MobilePhoneNumber": safe_search(r'driver mobile phone number (\S+)', text),
#             "DateOfBirth": safe_search(r'driver date of birth (\d{4}-\d{2}-\d{2})', text),
#             "DateOfBirthKnown": safe_search(r'driver date of birth known (Yes|No)', text),
#             "DrivingLicenseType": safe_search(r'driver license type (\S+)', text),
#             "UKResidency": safe_search(r'driver UK residency (Yes|No)', text),
#             "Occupation": safe_search(r'driver occupation (\S+)', text),
#             "Injuries": safe_search(r'driver injuries (Yes|No)', text)
#         },
#         "ThirdPartyVehicleDetails": [
#             {
#                 "ThirdPartyVRN": safe_search(r'third party VRN (\S+)', text),
#                 "ThirdPartyVRNUnknown": safe_search(r'third party VRN unknown (Yes|No)', text),
#                 "OwnerCompanyName": safe_search(r'third party owner company name (\S+)', text),
#                 "OwnerFirstName": safe_search(r'third party owner first name (\S+)', text),
#                 "OwnerSurname": safe_search(r'third party owner surname (\S+)', text),
#                 "IsVehicleDamaged": safe_search(r'third party vehicle damaged (Yes|No)', text),
#                 "DamageDescription": safe_search(r'third party vehicle damage description (.+)', text),
#                 "ClaimVehicleDamage": safe_search(r'third party vehicle damage claimed (Yes|No)', text),
#                 "ClaimThroughAXA": safe_search(r'third party claim through AXA (Yes|No)', text),
#                 "ThirdPartyCreditHire": safe_search(r'third party credit hire (Yes|No)', text),
#                 "CurrentLocation": safe_search(r'third party current location (.+)', text),
#                 "IsVehicleOperable": safe_search(r'third party vehicle operable (Yes|No)', text),
#                 "ThirdPartyFaultRating": safe_search(r'third party fault rating (.+)', text)
#             }
#         ],
#         "ThirdPartyDriverDetails": [
#             {
#                 "FirstName": safe_search(r'third party driver first name (\S+)', text),
#                 "LastName": safe_search(r'third party driver last name (\S+)', text),
#                 "Unknown": safe_search(r'third party driver unknown (Yes|No)', text),
#                 "Address": safe_search(r'third party driver address (\d+ \S+)', text),
#                 "Email": safe_search(r'third party driver email (\S+@\S+)', text),
#                 "HomePhoneNumber": safe_search(r'third party driver home phone number (\S+)', text),
#                 "MobilePhoneNumber": safe_search(r'third party driver mobile phone number (\S+)', text),
#                 "Injuries": safe_search(r'third party driver injuries (Yes|No)', text)
#             }
#         ],
#         "ThirdPartyPropertyDetails": {
#             "OwnerCompanyName": safe_search(r'third party property owner company name (\S+)', text),
#             "OwnerFirstName": safe_search(r'third party property owner first name (\S+)', text),
#             "OwnerLastName": safe_search(r'third party property owner last name (\S+)', text),
#             "PropertyName": safe_search(r'third party property name (\S+)', text)
#         },
#         "EmergencyServiceDetails": [
#             {
#                 "Type": safe_search(r'emergency service type (\S+)', text),
#                 "Name": safe_search(r'emergency service name (\S+)', text),
#                 "ReportNumber": safe_search(r'emergency service report number (\S+)', text)
#             }
#         ]
#     }
#     return payload

