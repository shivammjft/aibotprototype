from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

##pymysql
##mysql -u root -p users
DB_URL = "mysql+pymysql://root:Jft%40421@localhost:3306/users"

engine = create_engine(
    DB_URL
)

SesssionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()