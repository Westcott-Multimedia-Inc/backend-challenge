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
        """Return list of artists that crossing the metric value."""

        # Get metric_value params or set default to 0
        metric_value = request.args.get('metric_value', 0) or 0

        # Fetch all metrics
        metrics = Metric.query.order_by(Metric.artist_id.asc(), Metric.date.asc()).all()

        # Find the days when any artist crossed the passed value
        artist_metrics = {}
        yesterday_metrics = {}

        for metric in metrics:
            if not artist_metrics.get(metric.artist_id):
                artist_metrics[metric.artist_id] = []

            if metric.value >= int(metric_value) and (not artist_metrics[metric.artist_id] or yesterday_metrics[metric.artist_id] < int(metric_value)):
                artist_metrics[metric.artist_id].append(metric.date.strftime('%Y-%m-%d'))
            
            yesterday_metrics[metric.artist_id] = metric.value

        # Return a list of all artists as dictionaries with the artist id and all "crossings"
        artist_crossings = [
            {
                'artist_id': artist_id,
                'crossings': crossings
            }
            for artist_id, crossings in artist_metrics.items()
        ]

        return jsonify(artist_crossings)

    return app
