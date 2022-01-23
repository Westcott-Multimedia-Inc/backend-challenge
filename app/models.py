"""Define app models."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Artist(db.Model):
    """Representation of an artist."""

    id = db.Column(db.Integer, primary_key=True)
    metrics = db.relationship("Metric", backref="artist", lazy=True)


class Metric(db.Model):
    """Representation of a metric."""

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    value = db.Column(db.Integer)
    __table_args__ = (db.UniqueConstraint("artist_id", "date", name="_artist_date_uc"),)
