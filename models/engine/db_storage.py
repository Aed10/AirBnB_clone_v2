#!/usr/bin/python3
""" MySQL storage engine """
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """Database storage engine"""

    __engine = None
    __session = None

    def __init__(self):
        """db storage engine Constructor"""
        user = os.getenv("HBNB_MYSQL_USER")
        pwd = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        db = os.getenv("HBNB_MYSQL_DB")
        # the engine must be linked to the MySQL database and user
        # created before (hbnb_dev and hbnb_dev_db)
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(user, pwd, host, db),
            pool_pre_ping=True,
        )
        if os.getenv("HBNB_ENV") == "test":
            # reversed(_.sorted_tables)
            for table in Base.metadata.tables:
                table.delete()

    def all(self, cls=None):
        """query on the current session all objects depending of the cls"""
        objects = []
        if cls is None:
            for aCls in [User, State, City, Place, Amenity, Review]:
                objects += self.__session.query(aCls).all()
        else:
            objects = self.__session.query(cls).all()
        dictionary = {}
        for obj in objects:
            dictionary[f"{obj.__class__.__name__}.{obj.id}"] = obj
        return dictionary

    def new(self, obj):
        """adds obj to the current session"""
        self.__session.add(obj)

    def save(self):
        """commits all changes of current session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes obj from current session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """creates all database tables & the current session"""
        Base.metadata.create_all(self.__engine)
        sfactory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sfactory)
        self.__session = Session()

    def close(self):
        """close the session"""
        self.__session.close()
