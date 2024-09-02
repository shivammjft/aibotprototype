from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

##pymysql
##mysql -u root -p users
DB_URL = "mysql+pymysql://root:12345678@mysql:3306/chatbotserver"

engine = create_engine(
    DB_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
