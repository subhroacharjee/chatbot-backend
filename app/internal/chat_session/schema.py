from pydantic import BaseModel


class ChatSessionBase(BaseModel):
    pass


class ChatSession(ChatSessionBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
