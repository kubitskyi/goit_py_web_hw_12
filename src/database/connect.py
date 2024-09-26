from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# "postgresql+psycopg2://<username>:<password>@<host>:<port>/<database_name>"
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://root:secretps@localhost:5432/hw12"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__=="__main__":
    try:
        with engine.connect() as connection:
            print("Connection successful!")
    except Exception as e:
        print(f"Connection failed: {e}")