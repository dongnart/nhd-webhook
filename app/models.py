from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class WebhookData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

class WebhookConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)