from pydantic import BaseModel, Field, field_validator


ALLOWED_INTENSITIES = {"Low", "Medium"}
ALLOWED_GOALS = {
    "General wellness",
    "Flexibility and mobility",
    "Healthy activity habit",
}


class UserInput(BaseModel):
    username: str = Field(min_length=2, max_length=100)
    user_id: str = Field(min_length=1, max_length=80)
    age: int = Field(ge=18, le=100)
    weight: float = Field(gt=0, le=500)
    goal: str
    intensity: str

    @field_validator("goal")
    @classmethod
    def validate_goal(cls, value):
        if value not in ALLOWED_GOALS:
            raise ValueError("Choose a supported wellness goal.")
        return value

    @field_validator("intensity")
    @classmethod
    def validate_intensity(cls, value):
        if value not in ALLOWED_INTENSITIES:
            raise ValueError("Choose Low or Medium intensity.")
        return value


class FeedbackRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=80)
    feedback: str = Field(min_length=3, max_length=1000)
