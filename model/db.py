# coding: utf-8

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool
import redis

engine = create_engine(
        'mysql+pymysql://root:330625@127.0.0.1:3306/design?charset=utf8mb4',
        convert_unicode=True,
        poolclass=NullPool
)

db_session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=True,
    bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()
redis_connect = redis.StrictRedis()


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db_session.add(self)
        if commit:
            db_session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db_session.delete(self)
        return commit and db_session.commit()


class Model(CRUDMixin, Base):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True


