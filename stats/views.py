import datetime
from django.http import JsonResponse
from .models import Result

def add_result(request):
    user = request.GET.get("user")
    endgame_type = request.GET.get("endgame_type")
    result = request.GET.get("result")

    Result.objects.create(
        user=user,
        endgame_type=endgame_type,
        result=result,
        created_at=datetime.datetime.now()
    )

    return JsonResponse({"status": "ok"})
