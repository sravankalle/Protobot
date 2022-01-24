from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import update
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///test.db', echo=True)

Session = sessionmaker(bind=engine)

session = Session()
Base = declarative_base()
class User(Base):
    __tablename__= "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    coins = Column(Integer)
    
    @classmethod
    def createUser(cls, user_id, user_username, user_coins):
        user = cls(id=user_id, username=user_username, coins=user_coins)
        session.add(user)
        session.commit()
    
    @classmethod
    def getUserBalance(cls, user_id):
        query = select(User.coins).where(User.id == user_id)
        result = session.execute(query)
        return result.fetchone()

    @classmethod
    def updateUserBalance(cls, user_id, money):
        user = session.query(cls).filter(cls.id == user_id).one()
        user.coins += money
        session.commit()

Base.metadata.create_all(engine)
    
    

