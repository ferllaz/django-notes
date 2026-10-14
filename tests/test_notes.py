
import pytest
from rest_framework.test import APIClient
from notes.models import Note


pytestmark = pytest.mark.django_db


@pytest.fixture
def client():
    return APIClient()


def test_list_notes(client):
    response = client.get("/api/notes/")

    assert response.status_code == 200
    assert response.data == []


def test_create_note(client):
    response = client.post(
        "/api/notes/",
        {"title": "First note", "text": "Hello Django"},
        format="json",
    )

    assert response.status_code == 201
    assert Note.objects.count() == 1


def test_note_title(client):
    response = client.post(
        "/api/notes/",
        {"title": "My title", "text": "Some text"},
        format="json",
    )

    assert response.data["title"] == "My title"


def test_note_text(client):
    response = client.post(
        "/api/notes/",
        {"title": "My note", "text": "Important information"},
        format="json",
    )

    assert response.data["text"] == "Important information"


def test_create_multiple_notes(client):
    for i in range(3):
        response = client.post(
            "/api/notes/",
            {"title": f"Note {i}", "text": f"Text {i}"},
            format="json",
        )
        assert response.status_code == 201

    assert Note.objects.count() == 3
    response = client.get("/api/notes/")
    assert len(response.data) == 3
