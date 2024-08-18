from pydantic import BaseModel


class ChatBase(BaseModel):
    prompt: str


class Chat(ChatBase):
    id: int
    response: str

    class Config:
        from_attributes = True
