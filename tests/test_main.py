import pytest
from unittest import mock
import speech_recognition as sr
import json
from main import start_recording, stop_recording, transcribe_audio, transcribe_uploaded_audio
from payload_formatting import format_payload

# Mocking audio recording process
@mock.patch('main.sr.Recognizer.listen')
@mock.patch('main.sr.Microphone')
def test_start_recording(mock_microphone, mock_listen):
    mock_listen.return_value = mock.Mock()  # Mock the returned audio
    start_recording()
    mock_listen.assert_called_once()

# Mocking audio transcription process
@mock.patch('main.sr.AudioFile')
@mock.patch('main.sr.Recognizer.recognize_google')
def test_transcribe_audio_success(mock_recognize_google, mock_audio_file, tmp_path):
    mock_recognize_google.return_value = 'Test transcription'
    
    # Create a temporary audio file for testing
    test_audio_file = tmp_path / 'sample.wav'
    test_audio_file.write_bytes(b'fake_audio_data')
    
    text = transcribe_audio(str(test_audio_file))
    assert text == 'Test transcription'

@mock.patch('main.sr.AudioFile')
@mock.patch('main.sr.Recognizer.recognize_google')
def test_transcribe_audio_unknown_value(mock_recognize_google, mock_audio_file, tmp_path):
    mock_recognize_google.side_effect = sr.UnknownValueError

    test_audio_file = tmp_path / 'sample.wav'
    test_audio_file.write_bytes(b'fake_audio_data')

    text = transcribe_audio(str(test_audio_file))
    assert text is None

@mock.patch('main.sr.AudioFile')
@mock.patch('main.sr.Recognizer.recognize_google')
def test_transcribe_audio_request_error(mock_recognize_google, mock_audio_file, tmp_path):
    mock_recognize_google.side_effect = sr.RequestError("API error")

    test_audio_file = tmp_path / 'sample.wav'
    test_audio_file.write_bytes(b'fake_audio_data')

    text = transcribe_audio(str(test_audio_file))
    assert text is None

@mock.patch('main.sr.Recognizer.recognize_google')
def test_transcribe_uploaded_audio_success(mock_recognize_google, tmp_path):
    mock_recognize_google.return_value = 'Uploaded audio transcription'
    
    # Create a temporary uploaded audio file
    uploaded_file = tmp_path / 'test.mp3'
    uploaded_file.write_bytes(b'fake_audio_data')

    text = transcribe_uploaded_audio(str(uploaded_file))
    assert text == 'Uploaded audio transcription'

@mock.patch('main.sr.Recognizer.recognize_google')
def test_transcribe_uploaded_audio_failure(mock_recognize_google, tmp_path):
    mock_recognize_google.side_effect = sr.UnknownValueError

    uploaded_file = tmp_path / 'test.mp3'
    uploaded_file.write_bytes(b'fake_audio_data')

    text = transcribe_uploaded_audio(str(uploaded_file))
    assert text is None

# Test for format_payload function
def test_format_payload():
    transcribed_text = "Example text for testing."
    json_payload = format_payload(transcribed_text)
    
    # Check if the payload is a valid JSON string
    try:
        json.loads(json_payload)
    except json.JSONDecodeError as e:
        pytest.fail(f"JSON format error: {e}")
