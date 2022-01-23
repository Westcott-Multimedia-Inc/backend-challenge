"""Flask app factory."""

from typing import List, Union, Tuple

from flask import Flask, jsonify, request
from sqlalchemy import func

from app.models import db, Metric, Artist


def create_app(config_class: object):
    """Create Flask app.

    Args:
        config_class: configuration for Flask app
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    @app.route("/ping", methods=["GET", "POST"])
    def ping() -> str:
        """Return string to show the server is alive."""
        return "Server is here"

    @app.route("/metrics", methods=["GET"])
    def metrics() -> Union[List, Tuple]:
        """Return array of artist_ids and list of days when metrics have
        crossed metrics_value from request args."""

        metric_value_param = request.args.get("metric_value", type=int)
        if not metric_value_param:
            return "metric_value argument is required", 400

        # Fetch all metrics from DB
        metric_values_from_db = db.session.query(
            Artist.id,
            func.group_concat(Metric.value.concat("|").concat(Metric.date)),
        ).join(
            Metric,
            Metric.artist_id == Artist.id,
            isouter=True,
        ).group_by(Artist.id)

        # Calculate days when metrics crossed the passed value
        result = list()
        for (artist_id, dates_values) in metric_values_from_db:
            crossings = list()

            if dates_values is None:
                # filter out artists without metrics
                result.append({"artist_id": artist_id, "crossings": crossings})
                continue

            is_consequent_day = False
            for pair in dates_values.split(","):
                value, date = pair.split("|")
                if float(value) >= metric_value_param:
                    if not is_consequent_day:
                        crossings.append(date)
                        is_consequent_day = True
                else:
                    is_consequent_day = False

            result.append({"artist_id": artist_id, "crossings": crossings})

        return jsonify(result)

    return app
