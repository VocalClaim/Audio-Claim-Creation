import streamlit as st
from voice_recognition.recognize_voice import start_recording, stop_recording, transcribe_audio, transcribe_uploaded_audio
from guidewire_integration import send_to_guidewire
from data_transformer import transform_data
from logging_config import setup_logging, log_action, log_error
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import os
import json
from payload_formatting import format_payload, validate_payload
from payload_parser import parse_text_to_payload

# Setup logging configuration
setup_logging()

# Directory to save extracted texts
EXTRACTED_TEXTS_DIR = os.path.join('claim_form_automation', 'extracted_texts')
os.makedirs(EXTRACTED_TEXTS_DIR, exist_ok=True)

# Load the trained model and tokenizer
model = AutoModelForSeq2SeqLM.from_pretrained("./llm_model")
tokenizer = AutoTokenizer.from_pretrained("./llm_model")

# Define the function to generate payload using the trained model
# Function to generate payload using the trained model

def generate_payload(transcribed_text):
    try:
        # Tokenize the input text
        inputs = tokenizer.encode(transcribed_text, return_tensors="pt")

        # Generate output using the model
        outputs = model.generate(
            inputs,
            max_length=512,  # Adjust max_length if needed
            num_beams=4,     # Adjust num_beams if needed
            early_stopping=True
        )

        # Decode the output
        decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Debugging: Print the raw output and decoded output
        print("Raw model output:", outputs)
        print("Decoded output:", decoded_output)

        # Process the decoded output into payload
        processed_output = parse_text_to_payload(decoded_output)

        # Optional: Print processed output for debugging
        print("Processed output:", processed_output)

        return processed_output

    except Exception as e:
        st.error(f"Error generating payload: {str(e)}")
        log_error(f"Payload generation failed: {str(e)}")
        return None

# Define the function to check missing fields in the payload
def check_missing_fields(payload):
    required_fields = [
        "GraphID", "NotifiedOnBehalfOf", "PolicyNumber", "LossDate", "InsuredVRN",
        "ReportersCompanyName", "ReportersFirstName", "ReportersLastName", 
        "ReportersAddress", "ReportersWorkPhoneNumber", "ReportersHomePhoneNumber", 
        "ReportersMobilePhoneNumber", "ReportersEmail", "ReportersReference",
        "InsuredContactDetails", "NoticeDate", "ClaimInformation", "VehicleDetails", 
        "DriverDetails", "ThirdPartyVehicleDetails", "ThirdPartyDriverDetails", 
        "ThirdPartyPropertyDetails", "EmergencyServiceDetails"
    ]
    
    missing_fields = [field for field in required_fields if field not in payload]
    
    return missing_fields

# Function to handle transcription and payload generation
def handle_transcription(transcribed_text):
    if transcribed_text:
        json_payload = format_payload(transcribed_text)
        if not validate_payload(json_payload):
            st.error("Generated payload is invalid.")
            return

        send_to_guidewire(json_payload)
    else:
        st.error("No transcribed text available for generating payload.")

# Function to handle audio processing
def handle_audio_processing(transcribed_text, source):
    if transcribed_text:
        st.subheader(f"Transcribed Text from {source}:")
        st.write(transcribed_text)

        transcribed_text = st.text_area("Review/Correct Transcribed Text:", transcribed_text)

        suggested_payload = generate_payload(transcribed_text)
        if suggested_payload is None:
            st.error("Failed to generate payload.")
            return

        # Convert the payload to a JSON string if it's a dictionary
        if isinstance(suggested_payload, dict):
            suggested_payload_str = json.dumps(suggested_payload, indent=4)
        else:
            suggested_payload_str = suggested_payload

        st.subheader("LLM Suggested Payload")
        st.json(suggested_payload_str)

        missing_fields = check_missing_fields(suggested_payload)
        if missing_fields:
            st.warning("The following fields are missing:")
            st.write(missing_fields)
        else:
            if st.button("Review and Confirm Payload"):
                try:
                    st.json(suggested_payload_str)
                    if st.button("Confirm and Send to Guidewire"):
                        transformed_payload = transform_data(suggested_payload)
                        handle_transcription(transformed_payload)
                except Exception as e:
                    st.error(f"Error in processing payload: {str(e)}")
                    log_error(f"Payload processing failed: {str(e)}")
    else:
        st.error(f"Failed to transcribe the {source}.")

# Upload Audio for Transcription
st.subheader("Upload Audio File")
uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3"])
if uploaded_file is not None:
    transcribed_text = transcribe_uploaded_audio(uploaded_file)
    handle_audio_processing(transcribed_text, "Uploaded File")
