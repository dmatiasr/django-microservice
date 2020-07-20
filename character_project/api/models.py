from django.db import models
from django.db.models import (
    Avg,
    Max
)

class Character(models.Model):
    """
        Character model,
        This class represents one character
    """
    slug_item = models.IntegerField(db_index=True, unique=True, null=False, default=0)

class Score(models.Model):
    """
        Score model,
        This class represents all scores belong to a Character
    """
    # Se toma como pre-condicion que son todos Integers los elementos nuevos.
    score_field = models.IntegerField(null=False,
                                      blank=False,
                                      default=0
                                      )
    related_character = models.ForeignKey('Character',
                                          related_name='related_character_score',
                                          null=False,
                                          on_delete=models.CASCADE
                                          )

    def get_average_rating(self):
        return self.objects.all().aggregate(Avg('score_field'))

    def get_max_rating(self):
        return self.objects.aggregate(Max('score_field'))
