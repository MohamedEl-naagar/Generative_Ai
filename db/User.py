from sqlalchemy import Column, String , Integer , create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


Base = declarative_base()
engine = create_engine("sqlite:///mydb.db")

# design table 
class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False)
    age = Column(Integer,nullable=False)

    def __represent__(self):
        return f"User: {self.id} , name: {self.name}, age: {self.age}"

Base.metadata.create_all(engine)