from django.db import models


class Item(models.Model):

    title = models.CharField(max_length=250)
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        status = ''
        if self.completed :
            status = '(finished)'

        return f"{self.title} {status}"
    
    class Meta:
        verbose_name_plural  =  "Verbrauchsmaterial"