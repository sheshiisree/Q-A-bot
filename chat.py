import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, JSON, Text
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import relationship, backref


class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True)
    question = Column(Text)
    answer = Column(Text)    
    created_date = Column(DateTime, default=func.now(), nullable=False)
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
