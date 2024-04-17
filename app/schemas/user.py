from pydantic import BaseModel, ConfigDict


class UserRecord(BaseModel):
    first_name: str
    last_name: str = None
    age: int

    class Config(ConfigDict):
        orm_mode = True
