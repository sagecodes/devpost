from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Profile(Base):

    __tablename__ = 'profile'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    github = Column(String(250))
    twitter = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


class Project(Base):

    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    picture = Column(String(250))
    description = Column(String(250))
    sourcecode = Column(String(250))
    livedemo = Column(String(250))
    profile_id = Column(Integer, ForeignKey('profile.id'))
    profile = relationship(Profile)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


engine = create_engine('sqlite:///devpostusers.db')

Base.metadata.create_all(engine)
