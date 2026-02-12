from flask import Blueprint, render_template, current_app
from auralis.models import Album, News, Concert, Tag
from sqlalchemy import func
from datetime import datetime
import random

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    page = 1
    per_page = current_app.config['ITEMS_PER_PAGE']
    
    # Últimos álbumes
    latest_albums = Album.query.order_by(Album.created_at.desc()).limit(6).all()
    
    # Noticias recientes
    news = News.query.filter_by(published=True).order_by(News.date.desc()).limit(3).all()
    
    # Próximos conciertos
    upcoming_concerts = Concert.query.filter(
        Concert.date >= datetime.now()
    ).order_by(Concert.date.asc()).limit(5).all()
    
    # Tags aleatorios
    all_tags = Tag.query.order_by(func.random()).limit(12).all()
    
    # Álbumes destacados
    featured_albums = Album.query.filter_by().order_by(func.random()).limit(4).all()
    
    # Estadísticas
    total_albums = Album.query.count()
    total_artists = Artist.query.count()
    total_tracks = Track.query.count()
    
    return render_template('index.html',
                         latest_albums=latest_albums,
                         news=news,
                         concerts=upcoming_concerts,
                         tags=all_tags,
                         featured_albums=featured_albums,
                         total_albums=total_albums,
                         total_artists=total_artists,
                         total_tracks=total_tracks,
                         now=datetime.now())

@main_bp.route('/explore')
def explore():
    # Página de exploración con filtros
    genres = db.session.query(Album.genre, func.count(Album.genre)).group_by(Album.genre).all()
    return render_template('explore.html', genres=genres)

@main_bp.route('/about')
def about():
    return render_template('about.html')
