from django.db import models
from .templates import templates
class Endgame(models.Model):
    db_table = "Endgame"
    TEMPLATES = [
        (template.lower().replace(" ","_"),template.lower().replace(" ","_")) for template in templates.keys()
    ]
    template = models.CharField(max_length=100,choices=TEMPLATES)
    fen = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.template} - {self.fen} - {self.created_at}"

class Template(models.Model):
    db_table = "Template"
    template = models.CharField(max_length=100)
    queens = models.IntegerField()
    rooks = models.IntegerField()
    bishops = models.IntegerField()
    knights = models.IntegerField()
    wdl = models.IntegerField()    
