from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    scoped_session,
    sessionmaker,
    relationship
)
from sqlalchemy import Integer, String, DateTime, create_engine, ForeignKey
from datetime import datetime
from typing import List
import os


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    surname: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    birth_year: Mapped[int] = mapped_column(Integer, nullable=False)
    date_created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now
    )
    jobs: Mapped[List["Job"]] = relationship(back_populates="user")

    def __str__(self):
        return f"User: {self.name} {self.surname} ({self.email})"
    
    
    
class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="jobs")

# Define path for SQLite file
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
print(BASE_DIR)
connection_string = "sqlite:///" + os.path.join(BASE_DIR, "db.sqlite3")
print(connection_string)


# Create Engine
engine = create_engine(connection_string, echo=True)

#Create Session Factory
Session = scoped_session(sessionmaker())

# Drop all tables
Base.metadata.drop_all(engine)

# Create All Tables
Base.metadata.create_all(engine)

# Get an active session
local_session = Session(bind=engine)


print(Base.metadata.tables)

user1 = User(name="John", surname="Doe", email="john@hua.gr", birth_year=1990)
user2 = User(name="Jane", surname="Doe", email="jane@hua.gr", birth_year=1997)
user3 = User(name="Jack", surname="Doe", email="jack@hua.gr", birth_year=2000)


job1 = Job(name="Developer", user=user1)
job2 = Job(name="UI/UX Designer", user=user2)
job3 = Job(name="Data Scientist", user=user3)
job4 = Job(name="Software Engineer", user=user3)

# add users to session
local_session.add(user1)
local_session.add(user2)
local_session.add(user3)

# apply changes to db
# Query: 'insert into users (name, surname, email, birth_year) values ("John", "Doe", "john@hua", 1990)'
local_session.commit()

# remove a user from session
# find user
# user_to_delete = local_session.query(User).filter(User.id == 1).first()
# local_session.delete(user_to_delete)
# apply changes to db
# Query: 'delete from users where id=1'
# local_session.commit()


# read from db
# query: 'select * from users'
users = local_session.query(User).all()

# Where example
# Qurey: 'select * from users where name="John"'
u1 = local_session.query(User).filter(User.name == "John").all()
print(u1)

# print jobs of a user
# Query: 'select * from jobs where user_id=3'
jobs = local_session.query(Job).filter(Job.user_id == 3).all()
for j in jobs:
    print(j.name)
