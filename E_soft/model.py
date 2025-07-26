from pydantic import BaseModel
from typing import Optional

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text

Base = declarative_base()

class Note:
    id : int
    name : str
    command: str

class DataFile(Base):
    __tablename__ = 'data_files'
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False)
    num_rows = Column(Integer)
    num_cols = Column(Integer)








