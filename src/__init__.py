from flask import Flask

def create_app():
    app = Flask(__name__)
    from src.routers import main, api
    app.register_blueprint(main.bp)
    app.register_blueprint(api.bp)
    return app
