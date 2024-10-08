import streamlit as st
import os
import json
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from voice_recognition.recognize_voice import start_recording, stop_recording, transcribe_audio, transcribe_uploaded_audio
from guidewire_integration import send_to_guidewire
from data_transformer import transform_data
from logging_config import setup_logging, log_action, log_error
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

# Load custom CSS
def load_css():
    with open("styles/styles.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Call the function to load CSS
load_css()

# Function to generate payload using the trained model
def generate_payload(transcribed_text):
    try:
        if not transcribed_text.strip():
            raise ValueError("Transcribed text is empty or contains only whitespace.")
        
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

        # Debugging: Log the raw output and decoded output
        log_action("Raw model output: " + str(outputs))
        log_action("Decoded output: " + decoded_output)

        # Process the decoded output into a payload
        processed_output = parse_text_to_payload(decoded_output)
        log_action("Processed output: " + str(processed_output))

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
def handle_transcription(payload):
    try:
        if payload:
            if validate_payload(payload):
                send_to_guidewire(payload)
                log_action("Payload sent to Guidewire successfully.")
                st.success("Claim submitted successfully.")
            else:
                st.error("Generated payload is invalid.")
                log_error("Payload validation failed.")
        else:
            st.error("No transcribed text available for generating payload.")
            log_error("Empty transcribed text for payload generation.")

    except Exception as e:
        log_error(f"Error in transcription handling: {str(e)}")
        st.error(f"Error in transcription handling: {str(e)}")

# Function to handle audio processing
def handle_audio_processing(transcribed_text, source):
    try:
        if transcribed_text:
            log_action(f"Audio transcribed successfully from {source}")
            st.subheader(f"Transcribed Text from {source}:")
            transcribed_text = st.text_area("Review/Correct Transcribed Text:", transcribed_text, height=200)

            suggested_payload = generate_payload(transcribed_text)
            if suggested_payload is None:
                st.error("Failed to generate payload.")
                log_error("Payload generation failed.")
                return

            st.subheader("LLM Suggested Payload")
            st.json(suggested_payload)

            missing_fields = check_missing_fields(suggested_payload)
            if missing_fields:
                st.warning("The following fields are missing:")
                st.write(missing_fields)
                log_action(f"Missing fields detected: {missing_fields}")

            if not missing_fields:
                if st.button("Confirm and Send to Guidewire"):
                    transformed_payload = transform_data(suggested_payload)
                    handle_transcription(transformed_payload)
                    log_action("Payload confirmed and sent to Guidewire.")
        else:
            st.error(f"Failed to transcribe the {source}. No text returned.")
            log_error(f"Transcription failed for {source}. No text returned.")
    
    except Exception as e:
        log_error(f"Error in audio processing: {str(e)}")
        st.error(f"Error in audio processing: {str(e)}")

# New function to handle manual text input and auto-generate payload
def handle_manual_text_input():
    manual_text = st.text_area("Enter Claim Details Manually", "", height=200)
    if manual_text:
        suggested_payload = generate_payload(manual_text)
        if suggested_payload:
            st.subheader("LLM Suggested Payload from Manual Input")
            st.json(suggested_payload)

            missing_fields = check_missing_fields(suggested_payload)
            if missing_fields:
                st.warning("The following fields are missing:")
                st.write(missing_fields)
                log_action(f"Missing fields detected: {missing_fields}")

            if not missing_fields:
                if st.button("Confirm and Send to Guidewire (Manual Input)"):
                    transformed_payload = transform_data(suggested_payload)
                    handle_transcription(transformed_payload)
                    log_action("Payload confirmed and sent to Guidewire from manual input.")
        else:
            st.error("Failed to generate payload from manual input.")
            log_error("Payload generation failed for manual input.")

# Sidebar navigation
st.sidebar.title("Claim Creation through Voice Recognition")
st.sidebar.write("Navigate through the options below:")

option = st.sidebar.radio("Select an Option", ("Record Voice", "Upload Audio", "Manual Input", "Logs"))

if option == "Record Voice":
    st.header("Record Voice")
    if st.button("Start Recording"):
        start_recording()
        log_action("Started recording.")
    if st.button("Stop Recording"):
        audio_filename = stop_recording()  # Ensure the audio file is saved
        if audio_filename:
            transcribed_text = transcribe_audio(audio_filename)  # Pass the saved file path here
            if transcribed_text:
                handle_audio_processing(transcribed_text, "Recorded Audio")
            else:
                st.error("No transcribed text available after recording.")
                log_error("No transcribed text after recording.")
        else:
            st.error("Failed to save or retrieve the audio file.")
            log_error("Failed to save or retrieve the audio file.")

elif option == "Upload Audio":
    st.header("Upload Audio File")
    uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3"])
    if uploaded_file is not None:
        transcribed_text = transcribe_uploaded_audio(uploaded_file)
        if transcribed_text:
            handle_audio_processing(transcribed_text, "Uploaded File")
        else:
            st.error("No transcribed text available after uploading the file.")
            log_error("No transcribed text after uploading the file.")

elif option == "Manual Input":
    st.header("Enter Claim Details Manually")
    handle_manual_text_input()

elif option == "Logs":
    st.header("Display system logs here...")
    with st.expander("System Logs"):
        try:
            with open("system.log", "r") as log_file:
                st.text(log_file.read())
        except FileNotFoundError:
            st.warning("Log file not found.")


