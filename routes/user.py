from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from models import db, User, Room, Booking, Log, get_ist_now
from decorators import login_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    # Get user's bookings
    bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.created_at.desc()).all()
    
    # Get available rooms and update their availability
    all_rooms = Room.query.all()
    for room in all_rooms:
        room.update_available_beds()
    db.session.commit()
    
    available_rooms = [room for room in all_rooms if room.available_beds > 0]
    
    # Check active booking
    active_booking = Booking.query.filter_by(user_id=user_id).filter(
        Booking.status.in_(['approved', 'checked_in'])
    ).first()
    
    return render_template('user/dashboard.html', 
                         user=user, 
                         bookings=bookings,
                         available_rooms=available_rooms,
                         active_booking=active_booking)

@user_bp.route('/profile')
@login_required
def profile():
    user_id = session['user_id']
    user = User.query.get(user_id)
    bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.created_at.desc()).all()
    
    # Calculate statistics
    total_bookings = len(bookings)
    active_bookings = len([b for b in bookings if b.status in ['pending', 'approved', 'checked_in']])
    completed_bookings = len([b for b in bookings if b.status == 'checked_out'])
    
    return render_template('user/profile.html', 
                         user=user, 
                         bookings=bookings,
                         total_bookings=total_bookings,
                         active_bookings=active_bookings,
                         completed_bookings=completed_bookings)

@user_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not name or not phone:
            flash('Name and phone are required.', 'danger')
            return render_template('user/edit_profile.html', user=user)
        
        user.name = name
        user.phone = phone
        
        # Handle password change
        if current_password and new_password and confirm_password:
            if not user.check_password(current_password):
                flash('Current password is incorrect.', 'danger')
                return render_template('user/edit_profile.html', user=user)
            
            if new_password != confirm_password:
                flash('New passwords do not match.', 'danger')
                return render_template('user/edit_profile.html', user=user)
            
            if len(new_password) < 6:
                flash('Password must be at least 6 characters long.', 'danger')
                return render_template('user/edit_profile.html', user=user)
            
            user.set_password(new_password)
        
        try:
            db.session.commit()
            
            # Update session
            session['user_name'] = user.name
            
            # Log action
            log = Log(user_id=user_id, action='profile_updated', 
                     details=f'User updated profile')
            db.session.add(log)
            db.session.commit()
            
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('user.profile'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
    
    return render_template('user/edit_profile.html', user=user)

@user_bp.route('/bookings/request', methods=['POST'])
@login_required
def request_booking():
    user_id = session['user_id']
    room_id = request.form.get('room_id')
    
    if not room_id:
        flash('Please select a room.', 'danger')
        return redirect(url_for('user.dashboard'))
    
    # Check if user already has an active booking
    active_booking = Booking.query.filter_by(user_id=user_id).filter(
        Booking.status.in_(['pending', 'approved', 'checked_in'])
    ).first()
    
    if active_booking:
        flash('You already have an active booking request.', 'warning')
        return redirect(url_for('user.dashboard'))
    
    room = Room.query.get_or_404(room_id)
    
    # Check if room has available beds
    room.update_available_beds()  # Update to get current availability
    active_bookings = Booking.query.filter_by(room_id=room_id).filter(
        Booking.status.in_(['approved', 'checked_in'])
    ).count()
    
    if active_bookings >= room.capacity:
        flash('Room is full. Please select another room.', 'danger')
        return redirect(url_for('user.dashboard'))
    
    # Create booking
    booking = Booking(user_id=user_id, room_id=room_id, status='pending')
    
    try:
        db.session.add(booking)
        db.session.commit()
        
        # Log action
        log = Log(user_id=user_id, action='booking_requested', 
                 details=f'User requested booking for room {room.room_no}')
        db.session.add(log)
        db.session.commit()
        
        flash('Booking request submitted successfully! Waiting for admin approval.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred. Please try again.', 'danger')
    
    return redirect(url_for('user.dashboard'))

@user_bp.route('/bookings/checkin/<int:booking_id>', methods=['POST'])
@login_required
def checkin(booking_id):
    user_id = session['user_id']
    booking = Booking.query.get_or_404(booking_id)
    
    # Verify booking belongs to user
    if booking.user_id != user_id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('user.dashboard'))
    
    if booking.status != 'approved':
        flash('Only approved bookings can be checked in.', 'warning')
        return redirect(url_for('user.dashboard'))
    
    # Check if room still has available beds
    room = booking.room
    if room.get_actual_available_beds() <= 0:
        flash('Room is now full. Cannot check in.', 'danger')
        return redirect(url_for('user.dashboard'))
    
    booking.status = 'checked_in'
    booking.checkin_time = get_ist_now()
    booking.updated_at = get_ist_now()
    
    # Update room available beds
    room.update_available_beds()
    
    try:
        db.session.commit()
        
        # Log action
        log = Log(user_id=user_id, action='check_in', 
                 details=f'User checked in to room {room.room_no}')
        db.session.add(log)
        db.session.commit()
        
        flash('Check-in successful!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred. Please try again.', 'danger')
    
    return redirect(url_for('user.dashboard'))

@user_bp.route('/bookings/checkout/<int:booking_id>', methods=['POST'])
@login_required
def checkout(booking_id):
    user_id = session['user_id']
    booking = Booking.query.get_or_404(booking_id)
    
    # Verify booking belongs to user
    if booking.user_id != user_id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('user.dashboard'))
    
    if booking.status != 'checked_in':
        flash('Only checked-in bookings can be checked out.', 'warning')
        return redirect(url_for('user.dashboard'))
    
    booking.status = 'checked_out'
    booking.checkout_time = get_ist_now()
    booking.updated_at = get_ist_now()
    
    # Update room available beds (increase available beds)
    room = booking.room
    room.update_available_beds()
    
    try:
        db.session.commit()
        
        # Log action
        log = Log(user_id=user_id, action='check_out', 
                 details=f'User checked out from room {room.room_no}')
        db.session.add(log)
        db.session.commit()
        
        flash('Check-out successful!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred. Please try again.', 'danger')
    
    return redirect(url_for('user.dashboard'))

