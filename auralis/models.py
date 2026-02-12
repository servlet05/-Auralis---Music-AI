from auralis import db
from datetime import datetime
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Artist(db.Model):
    __tablename__ = 'artists'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100), nullable=False, index=True)
    location = db.Column(db.String(100))
    bio = db.Column(db.Text)
    profile_image = db.Column(db.String(200))
    website = db.Column(db.String(200))
    email = db.Column(db.String(120))
    is_ai = db.Column(db.Boolean, default=True)
    model_used = db.Column(db.String(100))  # Qué IA/modelo usaron
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    albums = db.relationship('Album', backref='artist', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Artist {self.name}>'

class Album(db.Model):
    __tablename__ = 'albums'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(200), nullable=False, index=True)
    artist_id = db.Column(db.String(36), db.ForeignKey('artists.id'), nullable=False)
    cover_image = db.Column(db.String(200))
    description = db.Column(db.Text)
    genre = db.Column(db.String(100), index=True)
    tags = db.Column(db.String(500))
    release_date = db.Column(db.Date)
    ai_prompt = db.Column(db.Text)  # Prompt usado para generar el álbum
    ai_model = db.Column(db.String(100))  # Modelo específico
    license = db.Column(db.String(50), default='CC BY-NC 4.0')
    plays = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    tracks = db.relationship('Track', backref='album', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Album {self.title}>'

class Track(db.Model):
    __tablename__ = 'tracks'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(200), nullable=False)
    album_id = db.Column(db.String(36), db.ForeignKey('albums.id'), nullable=False)
    audio_file = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.Integer)  # segundos
    track_number = db.Column(db.Integer)
    bpm = db.Column(db.Integer)
    key = db.Column(db.String(10))
    ai_prompt = db.Column(db.Text)
    plays = db.Column(db.Integer, default=0)
    downloads = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Track {self.title}>'

class News(db.Model):
    __tablename__ = 'news'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True)
    content = db.Column(db.Text)
    summary = db.Column(db.String(500))
    image = db.Column(db.String(200))
    published = db.Column(db.Boolean, default=True)
    featured = db.Column(db.Boolean, default=False)
    views = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    read_more_link = db.Column(db.String(500))
    
    def __repr__(self):
        return f'<News {self.title}>'

class Concert(db.Model):
    __tablename__ = 'concerts'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    artist_name = db.Column(db.String(200))
    venue = db.Column(db.String(200))
    location = db.Column(db.String(200))
    date = db.Column(db.DateTime)
    ticket_url = db.Column(db.String(500))
    description = db.Column(db.Text)
    is_virtual = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Concert {self.artist_name} at {self.venue}>'

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    count = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Tag {self.name}>'
