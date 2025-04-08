from pydantic import BaseModel , ConfigDict

class User(BaseModel):
    username: str 


class UserCreate(User):
    password: str


class UserResponse(UserCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


    