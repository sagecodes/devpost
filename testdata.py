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

#project for sage elliott:
project1 = Project(name="devpost",
                    picture="",
                    description="dev post stuff",
                    sourcecode="https://github.com/sageio/devpost",
                    livedemo="https://github.com/sageio/devpost",
                    profile=profile1)

session.add(project1)
session.commit()


# Profile for Sage Elliott2
profile2 = Profile(name="Sage Elliott 2",
                    email="hello@sageelliott.com",
                    picture="http://sageelliott.com/tmp/img/sage.jpg",
                    github="https://github.com/sageio",
                    twitter="https://twitter.com/sagecoder")

session.add(profile2)
session.commit()

#project for sage elliott2:
project2 = Project(name="devpost2",
                    picture="",
                    description="dev post2 stuff",
                    sourcecode="https://github.com/sageio/devpost",
                    livedemo="https://github.com/sageio/devpost",
                    profile=profile2)

session.add(project2)
session.commit()
