#!/usr/bin/env python3
from django.db import models


class Menu(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=150, unique=True)
    icon = models.CharField(
        verbose_name="Icono", max_length=100, default="bi bi-calendar-x-fill"
    )
    order = models.PositiveSmallIntegerField(verbose_name="Orden", default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"
        ordering = ["order", "name"]
