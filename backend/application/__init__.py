from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api
from os import path
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager
db=SQLAlchemy()
DB_NAME="libsys.db"
def create_app():
    app=Flask(__name__)
    CORS(app, origins=['http://localhost:8080'])
    app.config['SECRET_KEY'] = "mysecretkey"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SMTP_HOST']="smtp.gmail.com"
    app.config['SMTP_PORT']=587
    app.config['SENDER_EMAIL']='bookmagnet.bm@gmail.com'
    app.config['SENDDER_PASSWORD']='zciw yhjp mtbg ewzn'
    app.config['CACHE_TYPE'] = 'redis'
    db.init_app(app)
    jwt=JWTManager(app)
    api=Api(app)
    from .myapp import myapplication
    
    from .apis.book_api import BookAPI
    from .apis.section_api import  SectionAPI
    app.register_blueprint(myapplication,url_prefix='/')
    api.add_resource(BookAPI,"/api/books","/api/book/<int:book_id>")
    api.add_resource(SectionAPI,"/api/sections","/api/section/<int:section_id>")
    if not path.exists("instance/"+DB_NAME):
        with app.app_context():
            db.create_all()
            create_initial_data(db)
    return app
def create_initial_data(db):
    from .models import User
    admin = User(
        stored_name="Admin",
        stored_username="admin",
        stored_email="admin@bookmagnet.com",
        stored_password=generate_password_hash("admin"),
        role="admin",
    )
    db.session.add(admin)
    db.session.commit()
