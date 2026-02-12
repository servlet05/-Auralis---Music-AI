#!/usr/bin/env python
"""
Auralis - AI Music Platform
Entry point for the application
"""

import os
import sys
from auralis import create_app, db
from auralis.models import Artist, Album, Track, News, Concert, Tag

# Crear la aplicación
app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Contexto para flask shell"""
    return {
        'db': db,
        'Artist': Artist,
        'Album': Album,
        'Track': Track,
        'News': News,
        'Concert': Concert,
        'Tag': Tag
    }

@app.cli.command("init-db")
def init_db_command():
    """Inicializar la base de datos"""
    with app.app_context():
        db.create_all()
    print("✅ Base de datos inicializada correctamente")

@app.cli.command("create-sample-data")
def create_sample_data():
    """Crear datos de ejemplo para pruebas"""
    from datetime import datetime, date
    import random
    
    with app.app_context():
        # Crear artista IA de ejemplo
        artist = Artist(
            name="Neural Collective",
            location="Virtual, Spain",
            bio="Colectivo de músicos IA especializados en ambient y electronica",
            is_ai=True,
            model_used="MusicGen + StableAudio"
        )
        db.session.add(artist)
        db.session.commit()
        
        # Crear álbum
        album = Album(
            title="Latent Space Dreams",
            artist_id=artist.id,
            description="Exploraciones sónicas en el espacio latente de la IA",
            genre="Ambient",
            tags="ai-generated, ambient, experimental, latent-space",
            release_date=date.today(),
            ai_prompt="dreamy ambient textures, evolving pads, gentle rhythms",
            ai_model="MusicGen Large"
        )
        db.session.add(album)
        db.session.commit()
        
        # Crear tracks
        tracks = [
            {"title": "Neural Drift", "duration": 245, "bpm": 80},
            {"title": "Latent Echo", "duration": 312, "bpm": 75},
            {"title": "Synthetic Dawn", "duration": 198, "bpm": 90}
        ]
        
        for i, track_data in enumerate(tracks, 1):
            track = Track(
                title=track_data["title"],
                album_id=album.id,
                duration=track_data["duration"],
                track_number=i,
                bpm=track_data["bpm"]
            )
            db.session.add(track)
        
        # Crear noticia
        news = News(
            title="Auralis lanza soporte para música generada por IA",
            slug="auralis-lanza-soporte-ia",
            content="A partir de ahora, todos los artistas pueden subir música generada con inteligencia artificial. Bienvenidos al futuro del sonido.",
            summary="Plataforma dedicada exclusivamente a música IA",
            featured=True
        )
        db.session.add(news)
        
        # Crear concierto virtual
        concert = Concert(
            artist_name="Neural Collective",
            venue="Auralis Virtual Space",
            location="Metaverso",
            date=datetime(2024, 3, 15, 20, 0),
            is_virtual=True,
            description="Experiencia inmersiva de música generada en tiempo real por IA"
        )
        db.session.add(concert)
        
        # Crear tags
        tags = ["ai", "neural", "ambient", "electronic", "synthetic", "dreamcore", "algorithmic"]
        for tag_name in tags:
            tag = Tag(name=tag_name)
            db.session.add(tag)
        
        db.session.commit()
        print("✅ Datos de ejemplo creados correctamente")

@app.cli.command("create-admin")
def create_admin():
    """Crear usuario administrador"""
    print("🔧 Función de admin próximamente con sistema de usuarios")
    print("Por ahora, puedes gestionar contenido desde /admin/add-*")

if __name__ == "__main__":
    # Determinar si estamos en desarrollo o producción
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    
    # Puerto por defecto o variable de entorno
    port = int(os.environ.get('PORT', 5000))
    
    print("🚀 Auralis - AI Music Platform")
    print("=" * 40)
    print(f"📡 Servidor iniciado en http://localhost:{port}")
    print("📁 Base de datos: SQLite")
    print("🎵 Modo: AI Music Focus")
    print("=" * 40)
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
