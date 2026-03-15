from pydantic import BaseModel

class DisciplineCreate(BaseModel):
    name: str
    
class DisciplineUpdate(BaseModel):
    id: int
    name: str | None