"""Unit tests."""

import datetime
import unittest

from app import create_app, db
from app.config import TestingConfig
from app.helpers import timer
from app.models import Artist, Metric


class TestSetup(unittest.TestCase):
    """Unit testing setup."""

    def setUp(self):
        """Create new app and database for each test."""
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Remove databse and app context after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class TestBasic(TestSetup):
    """Basic default tests."""

    def test_ping(self):
        """Test that app can be pinged wth GET and POST."""
        response = self.app.test_client().get("/ping")
        self.assertEqual(response.status_code, 200)
        response = self.app.test_client().post("/ping")
        self.assertEqual(response.status_code, 200)


class TestMetrics(TestSetup):
    """Test metrics route."""

    def test_route(self):
        """Test that metrics route returns expected artist crossings."""
        @timer(1)
        def create_data():
            for i in range(100):
                db.session.add(Artist())
                for j in range(1000):
                    date = datetime.date.today() - datetime.timedelta(j)
                    value = (1000 - j) / (i + 1)
                    db.session.add(Metric(artist_id=i+1, date=date, value=value))
            db.session.commit()

        @timer(10)
        def call_endpoint(self):
            return self.app.test_client().get("/metrics?metric_value=50")

        create_data()
        response = call_endpoint(self)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 100)
        self.assertEqual(response.json[0]["artist_id"], 1)
        self.assertEqual(
            response.json[0]["crossings"][0],
            (datetime.date.today() - datetime.timedelta(950)).strftime("%Y-%m-%d")
        )

    def test_returns_validation_error_with_invalid_metric_value(self):
        """Test that metrics route returns validation error for passed invalid
        query param."""

        @timer(10)
        def call_endpoint_with_invalid_param(self):
            return self.app.test_client().get("/metrics?metric_value=-1")

        response = call_endpoint_with_invalid_param(self)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], "Invalid 'metric_value'")
