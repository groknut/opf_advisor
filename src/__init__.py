from flask import Flask


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )
    app.config["SECRET_KEY"] = "opf-advisor-dev-key"

    from src.routers.main import bp as main_bp
    from src.routers.api import bp as api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    return app