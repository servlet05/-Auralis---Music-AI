from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Ensure upload directories exist
    upload_dirs = ['audio', 'covers', 'profiles']
    for dir_name in upload_dirs:
        dir_path = os.path.join(app.config['UPLOAD_FOLDER'], dir_name)
        os.makedirs(dir_path, exist_ok=True)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from auralis.routes.main import main_bp
    from auralis.routes.artists import artists_bp
    from auralis.routes.albums import albums_bp
    from auralis.routes.tracks import tracks_bp
    from auralis.routes.admin import admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(artists_bp, url_prefix='/artists')
    app.register_blueprint(albums_bp, url_prefix='/albums')
    app.register_blueprint(tracks_bp, url_prefix='/tracks')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
