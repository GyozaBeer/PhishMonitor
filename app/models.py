#app/models.py
from app.database import db
from datetime import datetime
from flask_login import UserMixin

# 中間テーブルの定義
user_nrd = db.Table('user_nrd',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('nrd_id', db.Integer, db.ForeignKey('nrd.id'), primary_key=True)
)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    # その他のユーザー関連フィールド

    # 多対多リレーションシップ
    nrds = db.relationship('NRD', secondary=user_nrd, lazy='subquery',
                           backref=db.backref('users', lazy=True))

    def add_nrd_to_watchlist(self, nrd):
        if nrd not in self.nrds:
            self.nrds.append(nrd)
            db.session.commit()

    def remove_nrd_from_watchlist(self, nrd):
        if nrd in self.nrds:
            self.nrds.remove(nrd)
            db.session.commit()

    def __repr__(self):
        return f"<User '{self.username}'>"

class NRD(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain_name = db.Column(db.String(255), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)  # 死活状況
    is_active = db.Column(db.Boolean, default=True)  # 死活状況
    last_checked = db.Column(db.DateTime)  # 最後にチェックした日時
    ping_status = db.Column(db.Boolean)  # pingの起動状態
    curl_status = db.Column(db.Boolean)  # curlの起動状態

    def __repr__(self):
        return f"<NRD '{self.domain_name}'>"
