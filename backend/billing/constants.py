from django.db import models
from django.utils.translation import gettext_lazy as _

class GuideNature(models.TextChoices):
    CHRONIC = 'CHRONIC', _('Crônico')
    ACUTE = 'ACUTE', _('Agudo')