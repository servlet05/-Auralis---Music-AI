from flask import Blueprint, render_template, request, redirect, url_for, current_app
from auralis.models import Artist, db
from werkzeug.utils import secure_filename
import os
import uuid
from PIL import Image

artists_bp = Blueprint('artists', __name__)

def save_profile_image(file):
    """Guarda y optimiza la imagen de perfil"""
    if file and file.filename:
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower()
        if ext in current_app.config['ALLOWED_IMAGES']:
            new_filename = f"{uuid.uuid4()}.{ext}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'profiles', new_filename)
            
            # Optimizar imagen
            img = Image.open(file)
            img.thumbnail((400, 400))  # Redimensionar
            img.save(filepath, optimize=True, quality=85)
            
            return f"/static/uploads/profiles/{new_filename}"
    return None

@artists_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        artist = Artist(
            name=request.form['name'],
            location=request.form.get('location', ''),
            bio=request.form.get('bio', ''),
            website=request.form.get('website', ''),
            email=request.form.get('email', ''),
            is_ai=request.form.get('is_ai') == 'on',
            model_used=request.form.get('model_used', '')
        )
        
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file.filename:
                artist.profile_image = save_profile_image(file)
        
        db.session.add(artist)
        db.session.commit()
        
        return redirect(url_for('artists.detail', artist_id=artist.id))
    
    return render_template('artist/upload.html')

@artists_bp.route('/<artist_id>')
def detail(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    albums = artist.albums.order_by(Album.created_at.desc()).all()
    return render_template('artist/detail.html', artist=artist, albums=albums)

@artists_bp.route('/')
def list_all():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ITEMS_PER_PAGE']
    
    artists = Artist.query.order_by(Artist.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('artist/list.html', artists=artists)
