import uuid

from pydantic import BaseModel, Field

from app.domain.auth.entities.user import User


class Viewer(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user: User
