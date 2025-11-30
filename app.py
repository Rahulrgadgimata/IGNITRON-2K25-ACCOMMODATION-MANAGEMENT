from flask import Flask, render_template, redirect, url_for, flash, session, request
from models import db, User, Room, Booking, Log, get_ist_now
from config import Config
from email_service import init_email
import os
import pytz

# Try to load dotenv if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, skip

app = Flask(__name__)
app.config.from_object(Config)

# Initialize email service
init_email(app)

# Add template filter for IST timezone
IST = pytz.timezone('Asia/Kolkata')
@app.template_filter('ist')
def ist_filter(dt):
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    return dt.astimezone(IST).strftime('%Y-%m-%d %H:%M IST')

# Initialize database
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()
    
    # Create default admin user if it doesn't exist
    admin = User.query.filter_by(email='admin@ignitron.com').first()
    if not admin:
        admin = User(
            name='Admin',
            email='admin@ignitron.com',
            phone='0000000000',
            role='admin'
        )
        admin.set_password('admin123')
        admin.created_at = get_ist_now()
        db.session.add(admin)
        db.session.commit()

# Import routes (must be after app and db initialization)
from routes.admin import admin_bp
from routes.user import user_bp

app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(user_bp, url_prefix='/user')

@app.route('/')
def index():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user.is_admin():
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('user.dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user.is_admin():
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('user.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Please provide both email and password.', 'danger')
            return render_template('login.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_role'] = user.role
            session.permanent = True
            
            # Log login action
            log = Log(user_id=user.id, action='login', details=f'User logged in')
            db.session.add(log)
            db.session.commit()
            
            flash(f'Welcome back, {user.name}!', 'success')
            if user.is_admin():
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('user.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not all([name, email, phone, password, confirm_password]):
            flash('All fields are required.', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please login.', 'danger')
            return redirect(url_for('login'))
        
        # Create new user
        user = User(name=name, email=email, phone=phone, role='user')
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            
            # Log registration
            log = Log(user_id=user.id, action='registration', details=f'New user registered: {user.name}')
            db.session.add(log)
            db.session.commit()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    if 'user_id' in session:
        user_id = session['user_id']
        # Log logout action
        log = Log(user_id=user_id, action='logout', details='User logged out')
        db.session.add(log)
        db.session.commit()
    
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

