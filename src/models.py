"""Database models for the parking system"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    """User model for authentication and profile management"""
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default='student')  # admin, faculty, student
    created_at = Column(DateTime, default=datetime.utcnow)
    
    reservations = relationship('Reservation', back_populates='user')
    
    def __repr__(self):
        return f'<User {self.username}>'


class ParkingLot(Base):
    """Parking lot model"""
    __tablename__ = 'parking_lots'
    
    lot_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    location = Column(String(200), nullable=False)
    total_spaces = Column(Integer, nullable=False)
    available_spaces = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    spaces = relationship('ParkingSpace', back_populates='lot', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ParkingLot {self.name}>'
    
    @property
    def occupancy_rate(self):
        """Calculate occupancy rate"""
        if self.total_spaces == 0:
            return 0
        return round((self.total_spaces - self.available_spaces) / self.total_spaces * 100, 2)


class ParkingSpace(Base):
    """Individual parking space model"""
    __tablename__ = 'parking_spaces'
    
    space_id = Column(Integer, primary_key=True)
    lot_id = Column(Integer, ForeignKey('parking_lots.lot_id'), nullable=False)
    space_number = Column(String(20), nullable=False)
    category = Column(String(20), default='regular')  # regular, accessible, reserved
    is_available = Column(Boolean, default=True)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    lot = relationship('ParkingLot', back_populates='spaces')
    reservations = relationship('Reservation', back_populates='space')
    
    def __repr__(self):
        return f'<ParkingSpace {self.space_number}>'


class Reservation(Base):
    """Parking reservation model"""
    __tablename__ = 'reservations'
    
    reservation_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    space_id = Column(Integer, ForeignKey('parking_spaces.space_id'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(String(20), default='active')  # active, completed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', back_populates='reservations')
    space = relationship('ParkingSpace', back_populates='reservations')
    
    def __repr__(self):
        return f'<Reservation {self.reservation_id}>'
    
    @property
    def is_active(self):
        """Check if reservation is still active"""
        return self.status == 'active' and datetime.utcnow() < self.end_time
