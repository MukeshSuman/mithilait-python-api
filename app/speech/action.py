import azure.cognitiveservices.speech as speechsdk

# Create a speech configuration
speech_key = "YourSubscriptionKey"
service_region = "YourServiceRegion"
speech_config = speechsdk.SpeechConfig(
    subscription=speech_key, region=service_region)

# Create pronunciation assessment config
reference_text = "Hello world"
pronunciation_assessment_config = speechsdk.PronunciationAssessmentConfig(
    reference_text=reference_text,
    grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
    granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme,
    enable_miscue=True
)

# Create a recognizer
audio_config = speechsdk.AudioConfig(use_default_microphone=True)
speech_recognizer = speechsdk.SpeechRecognizer(
    speech_config=speech_config, audio_config=audio_config)

# Apply the pronunciation assessment configuration to the recognizer
pronunciation_assessment_config.apply_to(speech_recognizer)

# Function to process speech


def recognize():
    print(f"Speak the sentence: '{reference_text}'")
    result = speech_recognizer.recognize_once()

    # Check if result is successful
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Recognized: {result.text}")

        # Access the pronunciation assessment result
        pronunciation_result = speechsdk.PronunciationAssessmentResult(result)
        print(
            f"Pronunciation Score: {pronunciation_result.pronunciation_score}")
        print(f"Accuracy Score: {pronunciation_result.accuracy_score}")
        print(f"Fluency Score: {pronunciation_result.fluency_score}")
        print(f"Completeness Score: {pronunciation_result.completeness_score}")

    else:
        print("Speech not recognized or there was an error.")


# Call the function
recognize()
