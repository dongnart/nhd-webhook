from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from app.models import db, WebhookConfig, Admin, WebhookData
from app.auth import authenticate, login_required
from rq import Queue
from redis import Redis
from app.tasks import process_data

bp = Blueprint('webhook', __name__)
admin_bp = Blueprint('admin', __name__)
redis_conn = Redis()
queue = Queue(connection=redis_conn)

@bp.route('/webhook/<type>', methods=['POST'])
def webhook_by_type(type):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    queue.enqueue(process_data, data, type)
    return jsonify({"message": "Data received"}), 200

@admin_bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate(username, password):
            return redirect(url_for('admin.dashboard'))
        return "Invalid credentials", 401
    return render_template('admin.html')

@admin_bp.route('/admin/dashboard')
@login_required
def dashboard():
    webhooks = WebhookConfig.query.all()
    return jsonify([{"url": w.url, "type": w.type} for w in webhooks])

@admin_bp.route('/admin/add-webhook', methods=['POST'])
@login_required
def add_webhook():
    url = request.form['url']
    type = request.form['type']
    new_webhook = WebhookConfig(url=url, type=type)
    db.session.add(new_webhook)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))