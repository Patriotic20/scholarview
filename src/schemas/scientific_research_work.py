from pydantic import BaseModel, ConfigDict, Field
from datetime import date

class ScientificResearchWorkBase(BaseModel):
    scientific_research_form: str 
    date_of_publication: date
    name: str 



class ScientificResearchWorkCreate(ScientificResearchWorkBase):
    pass


class ScientificResearchWorkUpdate(BaseModel):
    scientific_research_form: str | None = None 
    date_of_publication: date | None = None
    name: str | None = None



class ScientificResearchWorkResponse(ScientificResearchWorkBase):
    id: int
    file_path: str 
    model_config = ConfigDict(from_attributes=True)

