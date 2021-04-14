"""Flask app factory."""

from typing import List

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from app.exceptions import ValidationError
from app.helpers import get_crossed_dates_per_artist

db = SQLAlchemy()


def create_app(config_class: object):
    """Create Flask app.

    Args:
        config_class: configuation for Flask app
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    @app.errorhandler(ValidationError)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.route("/ping", methods=["GET", "POST"])
    def ping() -> str:
        """Return string to show the server is alive."""
        return "Server is here"

    @app.route("/metrics", methods=["GET"])
    def metrics() -> List:
        """Return a list of all artists as dictionaries with the artist id and
         all "crossings" = day(s) the metric crossed the specified
         "metric_value" parameter.
        """
        requested_value = request.args.get('metric_value',
                                           default=None,
                                           type=int)
        if not requested_value or requested_value < 0:
            raise ValidationError("Invalid 'metric_value'")

        results = get_crossed_dates_per_artist(
            requested_value=requested_value)
        return jsonify(results)

    return app
