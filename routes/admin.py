from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify, make_response
from models import db, User, Room, Booking, Log, get_ist_now, IST
from decorators import admin_required, login_required
from datetime import datetime, timedelta
import csv
from io import StringIO

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    total_users = User.query.filter_by(role='user').count()
    total_rooms = Room.query.count()
    total_bookings = Booking.query.count()
    pending_bookings = Booking.query.filter_by(status='pending').count()
    checked_in = Booking.query.filter_by(status='checked_in').count()
    
    # Recent bookings
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(10).all()
    
    # Recent logs
    recent_logs = Log.query.order_by(Log.timestamp.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_rooms=total_rooms,
                         total_bookings=total_bookings,
                         pending_bookings=pending_bookings,
                         checked_in=checked_in,
                         recent_bookings=recent_bookings,
                         recent_logs=recent_logs)

@admin_bp.route('/rooms')
@admin_required
def rooms():
    rooms = Room.query.order_by(Room.room_no).all()
    # Update available beds for all rooms
    for room in rooms:
        room.update_available_beds()
    db.session.commit()
    return render_template('admin/rooms.html', rooms=rooms)

@admin_bp.route('/rooms/add', methods=['GET', 'POST'])
@admin_required
def add_room():
    if request.method == 'POST':
        room_no = request.form.get('room_no')
        capacity = request.form.get('capacity')
        available_beds = request.form.get('available_beds')
        description = request.form.get('description')
        
        if not all([room_no, capacity, available_beds]):
            flash('Room number, capacity, and available beds are required.', 'danger')
            return render_template('admin/add_room.html')
        
        try:
            capacity = int(capacity)
            available_beds = int(available_beds)
            
            if available_beds > capacity:
                flash('Available beds cannot exceed room capacity.', 'danger')
                return render_template('admin/add_room.html')
            
            if Room.query.filter_by(room_no=room_no).first():
                flash('Room number already exists.', 'danger')
                return render_template('admin/add_room.html')
            
            room = Room(room_no=room_no, capacity=capacity, 
                       available_beds=available_beds, description=description)
            db.session.add(room)
            db.session.commit()
            
            # Log action
            log = Log(user_id=session['user_id'], action='room_added', 
                     details=f'Admin added room: {room_no}')
            db.session.add(log)
            db.session.commit()
            
            flash('Room added successfully!', 'success')
            return redirect(url_for('admin.rooms'))
        except ValueError:
            flash('Capacity and available beds must be valid numbers.', 'danger')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
    
    return render_template('admin/add_room.html')

@admin_bp.route('/rooms/edit/<int:room_id>', methods=['GET', 'POST'])
@admin_required
def edit_room(room_id):
    room = Room.query.get_or_404(room_id)
    
    if request.method == 'POST':
        room_no = request.form.get('room_no')
        capacity = request.form.get('capacity')
        available_beds = request.form.get('available_beds')
        description = request.form.get('description')
        
        if not all([room_no, capacity, available_beds]):
            flash('Room number, capacity, and available beds are required.', 'danger')
            return render_template('admin/edit_room.html', room=room)
        
        try:
            capacity = int(capacity)
            available_beds = int(available_beds)
            
            if available_beds > capacity:
                flash('Available beds cannot exceed room capacity.', 'danger')
                return render_template('admin/edit_room.html', room=room)
            
            # Check if room number already exists (excluding current room)
            existing_room = Room.query.filter_by(room_no=room_no).first()
            if existing_room and existing_room.id != room_id:
                flash('Room number already exists.', 'danger')
                return render_template('admin/edit_room.html', room=room)
            
            old_room_no = room.room_no
            room.room_no = room_no
            room.capacity = capacity
            room.available_beds = available_beds
            room.description = description
            
            db.session.commit()
            
            # Log action
            log = Log(user_id=session['user_id'], action='room_edited', 
                     details=f'Admin edited room: {old_room_no} -> {room_no}')
            db.session.add(log)
            db.session.commit()
            
            flash('Room updated successfully!', 'success')
            return redirect(url_for('admin.rooms'))
        except ValueError:
            flash('Capacity and available beds must be valid numbers.', 'danger')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
    
    return render_template('admin/edit_room.html', room=room)

@admin_bp.route('/rooms/delete/<int:room_id>', methods=['POST'])
@admin_required
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    
    # Check if room has active bookings
    active_bookings = Booking.query.filter_by(room_id=room_id).filter(
        Booking.status.in_(['pending', 'approved', 'checked_in'])
    ).count()
    
    if active_bookings > 0:
        flash('Cannot delete room with active bookings.', 'danger')
        return redirect(url_for('admin.rooms'))
    
    room_no = room.room_no
    db.session.delete(room)
    db.session.commit()
    
    # Log action
    log = Log(user_id=session['user_id'], action='room_deleted', 
             details=f'Admin deleted room: {room_no}')
    db.session.add(log)
    db.session.commit()
    
    flash('Room deleted successfully!', 'success')
    return redirect(url_for('admin.rooms'))

@admin_bp.route('/users')
@admin_required
def users():
    users = User.query.filter_by(role='user').order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/bookings')
@admin_required
def bookings():
    status_filter = request.args.get('status', 'all')
    
    query = Booking.query
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    bookings = query.order_by(Booking.created_at.desc()).all()
    return render_template('admin/bookings.html', bookings=bookings, status_filter=status_filter)

@admin_bp.route('/bookings/approve/<int:booking_id>', methods=['POST'])
@admin_required
def approve_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.status != 'pending':
        flash('Only pending bookings can be approved.', 'warning')
        return redirect(url_for('admin.bookings'))
    
    # Check if room has available beds
    room = booking.room
    room.update_available_beds()  # Update to get current availability
    active_bookings = Booking.query.filter_by(room_id=room.id).filter(
        Booking.status.in_(['approved', 'checked_in'])
    ).count()
    
    if active_bookings >= room.capacity:
        flash('Room is full. Cannot approve more bookings.', 'danger')
        return redirect(url_for('admin.bookings'))
    
    booking.status = 'approved'
    booking.updated_at = get_ist_now()
    
    # Update room available beds (in case it was manually changed)
    room.update_available_beds()
    
    db.session.commit()
    
    # Log action
    log = Log(user_id=session['user_id'], action='booking_approved', 
             details=f'Admin approved booking #{booking_id} for user {booking.user.name}')
    db.session.add(log)
    db.session.commit()
    
    # Send approval email to user
    try:
        from email_service import send_booking_approval_email
        email_sent = send_booking_approval_email(
            user_email=booking.user.email,
            user_name=booking.user.name,
            room_no=room.room_no,
            room_description=room.description
        )
        if email_sent:
            flash('Booking approved successfully! Email notification sent.', 'success')
        else:
            flash('Booking approved successfully! (Email notification failed - check email configuration)', 'warning')
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        flash('Booking approved successfully! (Email notification failed - check email configuration)', 'warning')
    
    return redirect(url_for('admin.bookings'))

@admin_bp.route('/bookings/reject/<int:booking_id>', methods=['POST'])
@admin_required
def reject_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.status != 'pending':
        flash('Only pending bookings can be rejected.', 'warning')
        return redirect(url_for('admin.bookings'))
    
    booking.status = 'rejected'
    booking.updated_at = get_ist_now()
    
    # Update room available beds
    room = booking.room
    room.update_available_beds()
    
    db.session.commit()
    
    # Log action
    log = Log(user_id=session['user_id'], action='booking_rejected', 
             details=f'Admin rejected booking #{booking_id} for user {booking.user.name}')
    db.session.add(log)
    db.session.commit()
    
    flash('Booking rejected successfully!', 'success')
    return redirect(url_for('admin.bookings'))

@admin_bp.route('/logs')
@admin_required
def logs():
    query = Log.query
    
    # Filter by action
    action_filter = request.args.get('action')
    if action_filter:
        query = query.filter(Log.action == action_filter)
    
    # Filter by user email
    user_email = request.args.get('user_email')
    if user_email:
        query = query.join(User).filter(User.email.ilike(f'%{user_email}%'))
    
    # Filter by date range
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    if date_from:
        date_from_dt = IST.localize(datetime.strptime(date_from, '%Y-%m-%d'))
        query = query.filter(Log.timestamp >= date_from_dt)
    if date_to:
        date_to_dt = IST.localize(datetime.strptime(date_to, '%Y-%m-%d'))
        # Add one day to include the entire end date
        date_to_dt = date_to_dt + timedelta(days=1)
        query = query.filter(Log.timestamp < date_to_dt)
    
    logs = query.order_by(Log.timestamp.desc()).all()
    
    # Calculate statistics
    from models import get_ist_now
    today = get_ist_now().date()
    
    # Count today's logs
    today_logs = [log for log in logs if log.timestamp.date() == today]
    
    # Get unique user IDs
    unique_users = len(set(log.user_id for log in logs))
    
    # Get unique action types
    unique_actions = len(set(log.action for log in logs))
    
    return render_template('admin/logs.html', 
                         logs=logs, 
                         today=today,
                         today_logs_count=len(today_logs),
                         unique_users=unique_users,
                         unique_actions=unique_actions)

@admin_bp.route('/logs/export')
@admin_required
def export_logs():
    logs = Log.query.order_by(Log.timestamp.desc()).all()
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['ID', 'User', 'Email', 'Action', 'Details', 'Timestamp'])
    
    # Write data
    for log in logs:
        writer.writerow([
            log.id,
            log.user.name,
            log.user.email,
            log.action,
            log.details or '',
            log.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    output.seek(0)
    
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=accommodation_logs.csv'
    
    return response

@admin_bp.route('/logs/clear', methods=['POST'])
@admin_required
def clear_logs():
    try:
        # Get count before deletion for flash message
        log_count = Log.query.count()
        
        # Delete all logs
        Log.query.delete()
        db.session.commit()
        
        # Log the action (this will be the first log after clearing)
        log = Log(
            user_id=session['user_id'],
            action='logs_cleared',
            details=f'Admin {User.query.get(session["user_id"]).name} cleared all {log_count} logs'
        )
        db.session.add(log)
        db.session.commit()
        
        flash(f'Successfully cleared {log_count} log entries.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while clearing logs. Please try again.', 'danger')
    
    return redirect(url_for('admin.logs'))

