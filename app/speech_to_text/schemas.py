from pydantic import BaseModel


class PronunciationAssessmentResult(BaseModel):
    recognizedText: str
    pronunciationScore: float
    accuracyScore: float
    fluencyScore: float
    completenessScore: float
    prosodyScore: float

    class Config:
        from_attributes = True
