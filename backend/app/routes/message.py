from flask import Blueprint, render_template, request, redirect, url_for, flash
from backend.app.models import Conversation, Message, Booking
from backend.app.extensions import db

message_bp = Blueprint("message", __name__, url_prefix="/messages")

@message_bp.route("/")
def index():
    host_id = 1 # Hardcoded for demo
    conversations = Conversation.query.filter_by(host_id=host_id).order_by(Conversation.updated_at.desc()).all()
    
    active_conversation = None
    bookings = []
    
    conversation_id = request.args.get('conversation_id', type=int)
    
    if not conversation_id and conversations:
        # Default to first conversation
        conversation_id = conversations[0].id

    if conversation_id:
        active_conversation = Conversation.query.get(conversation_id)
        if active_conversation:
            # Mark messages as read
            unread_msgs = active_conversation.messages.filter_by(sender_type='guest', is_read=False).all()
            for msg in unread_msgs:
                msg.is_read = True
            db.session.commit()
            
            # Fetch bookings for this guest
            bookings = Booking.query.filter_by(guest_email=active_conversation.guest_email).order_by(Booking.created_at.desc()).all()

    return render_template(
        "message/index.html",
        active_nav="messages",
        conversations=conversations,
        active_conversation=active_conversation,
        bookings=bookings
    )

@message_bp.route("/<int:conversation_id>/send", methods=["POST"])
def send_message(conversation_id):
    content = request.form.get("content")
    if content and content.strip():
        msg = Message(
            conversation_id=conversation_id,
            sender_type="host",
            content=content.strip()
        )
        db.session.add(msg)
        
        # Update conversation updated_at
        conversation = Conversation.query.get(conversation_id)
        if conversation:
            # SQLAlchemy updates updated_at automatically on update, but we need to trigger an update.
            # Just touch a field or let it be. For now, db.session.add is enough.
            conversation.updated_at = db.func.now()
            
        db.session.commit()
        
    return redirect(url_for('message.index', conversation_id=conversation_id))

@message_bp.route("/report", methods=["POST"])
def report():
    # Giả lập xử lý report / liên hệ admin
    report_type = request.form.get("type", "Báo cáo") # 'report' or 'admin'
    title = request.form.get("title")
    content = request.form.get("content")
    
    if title and content:
        flash(f"Đã gửi {report_type} thành công! Quản trị viên sẽ sớm xem xét.", "success")
    else:
        flash("Vui lòng điền đầy đủ thông tin.", "danger")
        
    conversation_id = request.form.get("conversation_id")
    if conversation_id:
        return redirect(url_for('message.index', conversation_id=conversation_id))
    return redirect(url_for('message.index'))
