import speech_recognition as sr
import os
import datetime
from pydub import AudioSegment
import logging

# Configure logging
logging.basicConfig(filename='voice_recognition.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Directory to save recordings
RECORDINGS_DIR = os.path.join(os.path.dirname(__file__), 'recordings')
os.makedirs(RECORDINGS_DIR, exist_ok=True)

# Initialize recognizer
recognizer = sr.Recognizer()
audio = None

# Start recording audio with ambient noise adjustment
def start_recording():
    global audio
    with sr.Microphone() as source:
        try:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Recording started...")
            print("Recording started... Speak clearly.")
            audio = recognizer.listen(source, timeout=10)  # 10-second timeout
        except sr.WaitTimeoutError:
            logging.error("Timeout occurred while listening.")
            print("Recording timed out.")
        except Exception as e:
            logging.error(f"Error during recording: {e}")
            print("An error occurred during recording.")

# Stop recording and save the file
def stop_recording():
    global audio
    if audio:
        # Generate filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_filename = os.path.join(RECORDINGS_DIR, f"audio_{timestamp}.wav")

        try:
            # Save audio file
            with open(audio_filename, "wb") as f:
                f.write(audio.get_wav_data())
            logging.info(f"Recording stopped and saved as {audio_filename}")
            print(f"Recording stopped and saved as {audio_filename}")
            return audio_filename
        except Exception as e:
            logging.error(f"Error saving audio file: {e}")
            print("An error occurred while saving the audio file.")
            return None
    else:
        print("No audio recorded.")
        return None

# Transcribe audio file to text
def transcribe_audio(audio_filename):
    try:
        with sr.AudioFile(audio_filename) as source:
            # Record audio from file
            recorded_audio = recognizer.record(source)
            # Recognize speech using Google API
            text = recognizer.recognize_google(recorded_audio)
            logging.info(f"Transcribed text: {text}")
            print("Transcribed text: ", text)
            return text
    except sr.UnknownValueError:
        logging.error("Could not understand the audio.")
        print("Could not understand the audio.")
        return None
    except sr.RequestError as e:
        logging.error(f"Could not request results from Google API; {e}")
        print(f"Could not request results from Google API; {e}")
        return None
    except Exception as e:
        logging.error(f"Error during transcription: {e}")
        print("An error occurred during transcription.")
        return None

# Transcribe uploaded audio file (e.g., mp3, wav)
def transcribe_uploaded_audio(uploaded_file):
    try:
        # Convert file to wav format using pydub
        audio = AudioSegment.from_file(uploaded_file)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_filename = os.path.join(RECORDINGS_DIR, f"uploaded_audio_{timestamp}.wav")
        
        # Export audio as wav
        audio.export(audio_filename, format="wav")
        
        # Transcribe the wav file
        return transcribe_audio(audio_filename)
    except Exception as e:
        logging.error(f"Error converting or transcribing uploaded audio file: {e}")
        print("An error occurred during audio conversion or transcription.")
        return None
