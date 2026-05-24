from django.db import models

# Create your models here.
class link(models.Model):
    id = models.BigAutoField(primary_key=True)
    Short_url = models.CharField(max_length=10,unique=True,db_index=True)
    Long_url = models.URLField(max_length=2000)
    Created_at = models.DateTimeField(auto_now_add=True)
    click = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.Short_url} -> {self.Long_url[:50]}"