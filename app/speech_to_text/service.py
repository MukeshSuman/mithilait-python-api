import azure.cognitiveservices.speech as speechsdk
from typing import Tuple

from app.speech_to_text.schemas import PronunciationAssessmentResult


class AzureSpeechService:
    def __init__(self, subscription_key: str, region: str):
        self.subscription_key = subscription_key
        self.region = region
        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.subscription_key, region=self.region)

    def transcribe_audio_file(self, audio_file_path: str) -> str:
        audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config, audio_config=audio_config)

        result = speech_recognizer.recognize_once()
        print(result)
        return result.text if result.reason == speechsdk.ResultReason.RecognizedSpeech else "No speech recognized"

    def recognize_speech_from_file(self, audio_file_path) -> str:
        # audio_config = speechsdk.audio.AudioConfig(
        #     stream=speechsdk.AudioDataStream(audio_stream))

        audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)

        pronunciation_assessment_config = speechsdk.PronunciationAssessmentConfig(
            # reference_text=reference_text,
            grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
            granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme,
            enable_miscue=False
        )
        pronunciation_assessment_config.enable_prosody_assessment()

        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config, audio_config=audio_config)

        pronunciation_assessment_config.apply_to(speech_recognizer)

        result = speech_recognizer.recognize_once()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(f"result: {result}")
            pronunciation_result = speechsdk.PronunciationAssessmentResult(
                result)
            print(pronunciation_result)
            print(
                f"Pronunciation Score: {pronunciation_result.pronunciation_score}")
            print(f"Accuracy Score: {pronunciation_result.accuracy_score}")
            print(f"Fluency Score: {pronunciation_result.fluency_score}")
            print(
                f"Completeness Score: {pronunciation_result.completeness_score}")
            # return pronunciation_result
            data = {
                "recognizedText": result.text,
                "pronunciationScore": pronunciation_result.pronunciation_score,
                "accuracyScore": pronunciation_result.accuracy_score,
                "fluencyScore": pronunciation_result.fluency_score,
                "completenessScore": pronunciation_result.completeness_score,
                "prosodyScore": pronunciation_result.prosody_score,
                # "content_assessment_result": pronunciation_result.content_assessment_result,
                # "pronunciation_assessment_result": pronunciation_result,
            }
            finalData = PronunciationAssessmentResult(**data)
            return finalData
        else:
            print("Speech not recognized or there was an error.")
            return "No speech recognized"

        return result.text if result.reason == speechsdk.ResultReason.RecognizedSpeech else "No speech recognized"
