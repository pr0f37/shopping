import pytest
import os
from planner import create_app, db, Config
from unittest.mock import MagicMock, patch
import json
from pdb import set_trace as bp
from planner.models import Recipe



@pytest.fixture
def app():
    app = create_app()
    app.testing = True
    return app


@pytest.fixture
def client(app):
    client = app.test_client()
    return client


def test_add_new_user(app, client):
    # with app.app_context():
    #     db.session.rollback()
    #     db.session.add(Recipe(title="testAdamNowik", time="1h30m", text="Random", user_id=1))
    #     db.session.commit()
    result = client.get("/test")
    assert "testAdamNowik" in result.json

@patch("planner.main.routes.Recipe")
def test_add_new_user_mock(recipe_mock, app, client):
    recipe_mock.query.all.return_value = [MagicMock(title="Adam"), MagicMock(title="Justyna")]
    result = client.get("/test")
    assert result.json == ["Adam", "Justyna"]