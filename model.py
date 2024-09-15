# Step 1: Import necessary modules
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import datetime

# Step 2: Define the base class and data models
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    preferences = Column(Text)  # JSON string or serialized preferences
    
    sessions = relationship('Session', back_populates='user')
    tasks = relationship('Task', back_populates='user')

class Session(Base):
    __tablename__ = 'sessions'
    
    session_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime)
    
    user = relationship('User', back_populates='sessions')
    interactions = relationship('Interaction', back_populates='session')

class Interaction(Base):
    __tablename__ = 'interactions'
    
    interaction_id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('sessions.session_id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    user_input = Column(Text)
    assistant_response = Column(Text)
    
    session = relationship('Session', back_populates='interactions')
    emotion = relationship('Emotion', uselist=False, back_populates='interaction')

class Emotion(Base):
    __tablename__ = 'emotions'
    
    emotion_id = Column(Integer, primary_key=True)
    interaction_id = Column(Integer, ForeignKey('interactions.interaction_id'), nullable=False)
    emotion_type = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    
    interaction = relationship('Interaction', back_populates='emotion')

class Task(Base):
    __tablename__ = 'tasks'
    
    task_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    description = Column(Text, nullable=False)
    due_date = Column(DateTime)
    status = Column(String, default='pending')
    
    user = relationship('User', back_populates='tasks')

# Step 3: Create SQLite database engine
engine = create_engine('sqlite:///mydatabase.db', echo=True)

# Step 4: Create all tables in the database
Base.metadata.create_all(engine)

# Step 5: Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = SessionLocal()

# Step 6: Add a new user and commit to the database
new_user = User(username="John Doe", email="john@example.com", preferences="{'theme': 'dark'}")
db_session.add(new_user)
db_session.commit()

# Step 7: Query the user back
user = db_session.query(User).filter_by(username="John Doe").first()
print(f"Retrieved User: {user.username}, Email: {user.email}")