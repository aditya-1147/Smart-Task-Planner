# backend/models.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import json

class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    goal_text = Column(String, nullable=False)

    # Relationship to tasks
    tasks = relationship("Task", back_populates="plan")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("plans.id"))
    name = Column(String, nullable=False)
    description = Column(Text, default="")
    dependency_ids = Column(Text, default="[]")  # store as JSON string
    estimated_days = Column(Integer, default=1)

    # Relationship back to plan
    plan = relationship("Plan", back_populates="tasks")

    # Helper to get dependencies as Python list
    @property
    def dependencies(self):
        return json.loads(self.dependency_ids)
