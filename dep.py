import cv2
import json
import numpy as np
import pyaudio
import vosk

# Set up Vosk speech recognizer
def init_vosk():
    vosk.SetLogLevel(-1)
    model = vosk.Model("C:/Users/HP/Downloads/vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15")
    return vosk.KaldiRecognizer(model, 16000)

# Set up PyAudio for microphone input
def init_audio():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=2048)
    return audio, stream

# Initialize OpenCV camera
def init_camera():
    return cv2.VideoCapture(0)

# Placeholder function for sign language recognition
def recognize_sign_language(frame):
    # This is a placeholder function for sign language recognition
    # You would replace this function with your actual sign language recognition code
    # For simplicity, this function returns a fixed gesture ("A" for example)
    return "A"

# Main loop
def main():
    recognizer = init_vosk()
    audio, audio_stream = init_audio()
    camera = init_camera()

    while True:
        # Capture video frame from camera
        ret, frame = camera.read()
        if not ret:
            print("Error: Failed to capture frame")
            break

        # Perform sign language recognition using OpenCV
        sign_language_text = recognize_sign_language(frame)

        # Perform speech-to-text transcription using Vosk
        audio_data = audio_stream.read(2048)
        recognizer.AcceptWaveform(audio_data)
        result = recognizer.Result()
        if result:
            result_json = json.loads(result)
            speech_text = result_json.get("text", "")

        # Display the recognized text (both sign language and speech)
        display_text = f"Sign language: {sign_language_text}\nSpeech: {speech_text}"
        print(display_text)

        # Display the video frame with text overlay (implementation dependent)
        # For now, we'll just print the recognized text to the console
        print(display_text)

        # Check for exit key press
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    # Release resources
    camera.release()
    cv2.destroyAllWindows()
    audio_stream.stop_stream()
    audio_stream.close()
    audio.terminate()

if __name__ == "__main__":
    main()
