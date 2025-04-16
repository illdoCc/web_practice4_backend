from sqlalchemy import insert
from myUser import User
from sqlalchemy import create_engine
from hashlib import sha256

engine = create_engine("postgresql://postgres:123@localhost:8080/test")  # 也可以換成你的資料庫 URI

pwd = sha256('Anne'.encode('utf-8')).hexdigest()
with engine.connect() as conn:
    stmt = insert(User).values(username="Anne", password=pwd, birthday='2003-11-11')
    conn.execute(stmt)
    conn.commit()