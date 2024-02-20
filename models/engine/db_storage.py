#!/usr/bin/python3
""" DBStorage Module for HBNB project """

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

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
                instances = self.__session.query(eval(table)).all()
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
        Base.metadata.create_all(bind=self.__engine)

        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        self.__session.close()
