from pydantic import BaseModel

class SkillObjectiveSchema(BaseModel):
    name: str
    description: str