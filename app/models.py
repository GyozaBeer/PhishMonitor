from app import db
from datetime import datetime

# 中間テーブルの定義
user_nrd = db.Table('user_nrd',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('nrd_id', db.Integer, db.ForeignKey('nrd.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    # その他のユーザー関連フィールド

    # 多対多リレーションシップ
    nrds = db.relationship('NRD', secondary=user_nrd, lazy='subquery',
                           backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f"<User '{self.username}'>"

class NRD(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain_name = db.Column(db.String(255), unique=True, nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    # その他のNRD関連フィールド

    def __repr__(self):
        return f"<NRD '{self.domain_name}'>"
