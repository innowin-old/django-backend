from django.db import models
from django.utils.timezone import now


class Base(models.Model):
    class Meta:
        ordering = ["-pk"]
        verbose_name_plural = "Basics"
        abstract = True

    created_time = models.DateTimeField(db_index=True, default=now, editable=False, blank=True)
    updated_time = models.DateTimeField(db_index=True, default=now, blank=True)
