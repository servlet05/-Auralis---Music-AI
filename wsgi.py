"""
WSGI entry point for production servers (gunicorn, uwsgi)
"""
from auralis import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
