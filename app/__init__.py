"""Flask app factory."""

from typing import List

from flask import Flask, jsonify, request

from .extensions import db
from .models import Artist, Metric


def create_app(config_class: object):
    """Create Flask app.

    Args:
        config_class: configuation for Flask app
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    @app.route("/ping", methods=["GET", "POST"])
    def ping() -> str:
        """Return string to show the server is alive."""
        return "Server is here"

    @app.route("/metrics", methods=["GET"])
    def metrics() -> List:
        """IMPLEMENT YOUR SOLUTION HERE."""

    return app
