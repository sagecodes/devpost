from database_setup import Base, Profile, Project
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# create Session and connect to database
engine = create_engine('sqlite:///devpost.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Profile for Sage Elliott
profile1 = Profile(name="Sage Elliott",
                    email="hello@sageelliott.com",
                    picture="http://sageelliott.com/tmp/img/sage.jpg",
                    github="https://github.com/sageio",
                    twitter="https://twitter.com/sagecoder")

session.add(profile1)
session.commit()

# Profile for Sage Elliott
profile2 = Profile(name="Sage Elliott 2",
                    email="hello@sageelliott.com",
                    picture="http://sageelliott.com/tmp/img/sage.jpg",
                    github="https://github.com/sageio",
                    twitter="https://twitter.com/sagecoder")

session.add(profile2)
session.commit()
