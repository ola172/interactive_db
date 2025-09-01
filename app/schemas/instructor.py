from pydantic import BaseModel


class InstructorBase(BaseModel):
    profile_image: str | None = None
    name: str
    title: str | None = None
    bio: str | None = None
    linkedin: str | None = None
    education: str | None = None
    is_top_rated: bool = False
    is_new: bool = False
