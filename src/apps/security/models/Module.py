#!/usr/bin/env python3

# Import Django imports
from django.db import models
from django.contrib.auth.models import Permission

# Imports models
from .Menu import Menu


class Module(models.Model):
    url = models.CharField(verbose_name="Url", max_length=100, unique=True)
    name = models.CharField(verbose_name="Nombre", max_length=100)
    menu = models.ForeignKey(
        Menu, on_delete=models.PROTECT, verbose_name="Menu", related_name="modules"
    )
    description = models.CharField(
        verbose_name="Descripción", max_length=200, null=True, blank=True
    )
    icon = models.CharField(
        verbose_name="Icono", max_length=100, default="bi bi-x-octagon"
    )
    is_active = models.BooleanField(verbose_name="Es activo", default=True)
    order = models.PositiveSmallIntegerField(verbose_name="Orden", default=0)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return f"{self.name} [{self.url}]"

    class Meta:
        verbose_name = "Módulo"
        verbose_name_plural = "Módulos"
        ordering = ["menu", "order", "name"]
