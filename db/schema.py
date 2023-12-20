from sqlalchemy import Column, String, DateTime, Integer,ForeignKey,Text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
from datetime import datetime
import sys
sys.path.append('.')
from config_data.config import db_string

db = create_engine(db_string, pool_pre_ping=True)
base = declarative_base()

class User(base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(200), nullable=False)

class Post(base):
    __tablename__ ='post'
    id = Column(String(100), primary_key=True ,nullable=False,)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref='posts')
    like_count = Column(Integer, default=0)

class Like(base):
    __tablename__ ='like'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(String(100), ForeignKey('post.id'), nullable=False)

class Comment(base):
    __tablename__ ='comment'
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(String(100), ForeignKey('post.id'), nullable=False)
    user = relationship('User', backref='comments')

    # def __init__(self, id, text, timestamp, user_id, post_id, user):
    #     self.id = id
    #     self.text = text
    #     self.timestamp = timestamp
    #     self.user_id = user_id
    #     self.post_id = post_id
    #     self.user = user

    # def as_dict(self):
    #     return {c.name: getattr(self, c.name) for c in self._table_.columns}


Session = sessionmaker(db)

#to create the tables if already not created
base.metadata.create_all(db)

