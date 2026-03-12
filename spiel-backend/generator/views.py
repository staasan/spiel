import datetime
import random
from django.http import JsonResponse
from .models import Endgame
from .generate import generate
from .templates import templates

def add_endgame(request):
    template = request.GET.get("template")

    Endgame.objects.create(
        template=template,
        fen=generate(templates[template],template),
        created_at=datetime.datetime.now()
    )

    return JsonResponse({"status": "ok"})

def get_endgame(request):
    template = request.GET.get("template")
    queryset = Endgame.objects.filter(template=template)

    count = queryset.count()
    if count == 0:
        return JsonResponse({"status": "error"})

    random_index = random.randint(0, count - 1)
    endgame = queryset[random_index]

    return JsonResponse({
        "status": "ok",
        "fen": endgame.fen,
        "id": endgame.id
    })
