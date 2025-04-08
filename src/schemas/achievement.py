from pydantic import BaseModel, ConfigDict , Field
from datetime import date


class AchievementBase(BaseModel):
    name: str
    type_of_achievement: str
    date_of_award_of_achievement: date

class AchievementCreate(AchievementBase):
    pass 


class AchievementResponse(AchievementBase):
    id: int
    file_path: str


    model_config = ConfigDict(from_attributes=True)



class AchievementUpdate(BaseModel):
    name: str | None = Field(default=None)
    type_of_achievement: str | None = Field(default=None)
    date_of_award_of_achievement: date | None = Field(default=None)