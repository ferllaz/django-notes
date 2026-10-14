
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Note


@api_view(["GET", "POST"])
def notes_list(request):
    if request.method == "GET":
        notes = Note.objects.all()
        data = [
            {"id": note.id, "title": note.title, "text": note.text}
            for note in notes
        ]
        return Response(data)

    title = request.data.get("title")
    text = request.data.get("text")

    if not isinstance(title, str) or not title.strip():
        return Response(
            {"error": "title is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not isinstance(text, str) or not text.strip():
        return Response(
            {"error": "text is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    note = Note.objects.create(title=title, text=text)

    return Response(
        {"id": note.id, "title": note.title, "text": note.text},
        status=status.HTTP_201_CREATED,
    )
