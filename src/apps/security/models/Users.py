#!/usr/bin/env python3
from django.contrib.auth.models import AbstractUser
from django.db import models

"""
Modelo User: Extiende el usuario estándar de Django para añadir campos personalizados.
Utiliza email como identificador principal para login en lugar del username.
"""


class User(AbstractUser):
    dni = models.CharField(
        verbose_name="Cédula o RUC", max_length=13, blank=True, null=True
    )
    image = models.ImageField(
        verbose_name="Imagen de perfil",
        upload_to="security/users/",
        max_length=1024,
        blank=True,
        null=True,
    )
    email = models.EmailField("Email", unique=True)
    direction = models.CharField("Dirección", max_length=200, blank=True, null=True)
    phone = models.CharField("Teléfono", max_length=50, blank=True, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        permissions = (
            ("change_userprofile", "Cambiar perfil de Usuario"),
            ("change_userpassword", "Cambiar contraseña de Usuario"),
        )

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def get_groups(self):
        return self.groups.all()

    def get_short_name(self):
        return self.username

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return "/static/img/usuario_anonimo.png"


class AccionChoices(models.TextChoices):
    ADICION = "ADICION", "ADICION"
    MODIFICACION = "MODIFICACION", "MODIFICACION"
    ELIMINACION = "ELIMINACION", "ELIMINACION"


class AuditUser(models.Model):
    usuario = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.PROTECT)
    tabla = models.CharField(max_length=100, verbose_name="Tabla")
    registroid = models.IntegerField(verbose_name="Registro Id")
    accion = models.CharField(
        choices=AccionChoices, max_length=15, verbose_name="Accion"
    )
    fecha = models.DateField(verbose_name="Fecha")
    hora = models.TimeField(verbose_name="Hora")
    estacion = models.CharField(max_length=100, verbose_name="Estacion")

    def __str__(self):
        return "{} - {} [{}]".format(self.usuario.username, self.tabla, self.accion)

    class Meta:
        verbose_name = "Auditoria Usuario "
        verbose_name_plural = "Auditorias Usuarios"
        ordering = ("-fecha", "hora")
