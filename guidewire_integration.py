import requests

def send_to_guidewire(payload):
    url = "http://localhost:8088/cc/ClaimCenter.do"  # Update with actual endpoint
    # http://localhost:8088/cc/ClaimCenter.do
    # https://guidewire_claim_center_endpoint/api/claims
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer <your_access_token>'  # Use actual authorization
    }
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print("Claim successfully created in Guidewire.")
        return True
    else:
        print(f"Failed to create claim: {response.status_code} - {response.text}")
        return False
