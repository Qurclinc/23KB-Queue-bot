from pydantic import BaseModel

class StudentCreate(BaseModel):
    user_id: int
    usertag: str | None
    username: str
    
class StudentUpdate(BaseModel):
    user_id: int
    usertag: str | None
    username: str | None