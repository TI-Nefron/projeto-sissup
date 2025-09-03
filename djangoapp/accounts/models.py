from django.contrib.auth.models import AbstractUser
from django.db import models
from organization.models import Clinic

class CustomUser(AbstractUser):
    """
    Extends the default Django User model to include clinic associations,
    enabling a multi-tenancy access control system.
    """
    clinics = models.ManyToManyField(
        Clinic,
        verbose_name="Clínicas",
        blank=True,
        related_name="users",
        help_text="As clínicas às quais este usuário tem acesso. Um superusuário tem acesso a todas as clínicas implicitamente."
    )

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.get_full_name() or self.username