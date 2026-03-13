from django.contrib import admin
from django.urls import path
from stats.views import add_result
from generator.views import add_endgame, get_endgame

urlpatterns = [
    path("api/add_result/", add_result),
    path("api/add_endgame/", add_endgame),
    path("api/get_endgame", get_endgame),
    path('admin/', admin.site.urls),
]
