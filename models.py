from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pytz

db = SQLAlchemy()

# Indian Standard Time timezone
IST = pytz.timezone('Asia/Kolkata')

def get_ist_now():
    """Get current time in Indian Standard Time"""
    return datetime.now(IST)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)  # 'admin' or 'user'
    created_at = db.Column(db.DateTime, default=get_ist_now)
    
    # Relationships
    bookings = db.relationship('Booking', backref='user', lazy=True, cascade='all, delete-orphan')
    logs = db.relationship('Log', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.email}>'

class Room(db.Model):
    __tablename__ = 'rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    room_no = db.Column(db.String(50), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    available_beds = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=get_ist_now)
    
    # Relationships
    bookings = db.relationship('Booking', backref='room', lazy=True, cascade='all, delete-orphan')
    
    def get_occupied_beds(self):
        """Calculate number of occupied beds (checked_in bookings)"""
        return Booking.query.filter_by(room_id=self.id).filter(
            Booking.status == 'checked_in'
        ).count()
    
    def get_actual_available_beds(self):
        """Calculate actual available beds based on current bookings"""
        occupied = self.get_occupied_beds()
        return max(0, self.capacity - occupied)
    
    def update_available_beds(self):
        """Update available_beds based on current occupancy"""
        self.available_beds = self.get_actual_available_beds()
    
    def __repr__(self):
        return f'<Room {self.room_no}>'

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)  # 'pending', 'approved', 'rejected', 'checked_in', 'checked_out'
    checkin_time = db.Column(db.DateTime)
    checkout_time = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=get_ist_now)
    updated_at = db.Column(db.DateTime, default=get_ist_now, onupdate=get_ist_now)
    
    def __repr__(self):
        return f'<Booking {self.id} - User {self.user_id} - Room {self.room_id}>'

class Log(db.Model):
    __tablename__ = 'logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)  # e.g., 'check_in', 'check_out', 'booking_request', etc.
    timestamp = db.Column(db.DateTime, default=get_ist_now)
    details = db.Column(db.Text)  # Additional details about the action
    
    def __repr__(self):
        return f'<Log {self.id} - {self.action} at {self.timestamp}>'

