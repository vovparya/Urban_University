from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from ..backend.db import Base


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    priority = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True, index=True)
    slug = Column(String, unique=True, index=True)

    # Связь с моделью User
    user = relationship('User', back_populates='tasks')
