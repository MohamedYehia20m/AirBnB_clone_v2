#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

import os


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="all, delete", backref="state")

    if os.getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def cities(self):
            return [city for city in self.cities
                    if review.state_id == self.id]
