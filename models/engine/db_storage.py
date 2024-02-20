#!/usr/bin/python3
""" DBStorage Module for HBNB project """

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.base_model import Base


class DBStorage:
    """Database storage class"""
    __engine = None
    __session = None

    def __init__(self):
        self.engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                .format(os.getenv('HBNB_MYSQL_USER'),
                    os.getenv('HBNB_MYSQL_PWD'),
                    os.getenv('HBNB_MYSQL_HOST'),
                    os.getenv('HBNB_MYSQL_DB')),
                pool_pre_ping=True)
        if os.getenv('HBNB_MYSQL_DB') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        tables = ['User', 'State', 'City', 'Amenity', 'Place', 'Review']
        ret_dict = {}
        if cls is None:
            for table in tables:
                instances = self.__session.query(eval(table)).all
                for instance in instances:
                    key = instance.__class__.__name__ + '.' + instance.id
                    ret_dict.update({key: instance})
        else:
            if type(cls) == str:
                cls = eval(cls)
            instances = self.__session.query(cls).all()
            for instance in instances:
                key = instance.__class__.__name__ + '.' + instance.id
                ret_dict.update({key: instance})
        return ret_dict

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        # TODO: create all tables in the database (feature of SQLAlchemy) (WARNING: all classes who inherit from Base must be imported before calling Base.metadata.create_all(engine))
        # TODO: create the current database session (self.__session) from the engine (self.__engine) by using a sessionmaker - the option expire_on_commit must be set to False ; and scoped_session - to make sure your Session is thread-safe
