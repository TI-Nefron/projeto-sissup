from django.contrib.auth.models import AbstractUser
from django.db import models
from organization.models import Clinic

class Permission(models.Model):
    codename = models.CharField("Código", max_length=100, unique=True)
    name = models.CharField("Nome", max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Permissão"
        verbose_name_plural = "Permissões"

class Role(models.Model):
    name = models.CharField("Nome do Cargo", max_length=100, unique=True)
    permissions = models.ManyToManyField(Permission, verbose_name="Permissões", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"

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
    roles = models.ManyToManyField(Role, verbose_name="Cargos", blank=True, related_name="users")

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.get_full_name() or self.username