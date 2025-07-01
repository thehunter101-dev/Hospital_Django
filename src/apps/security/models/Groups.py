#!/usr/bin/env python3
from django.db import models
from django.contrib.auth.models import Group, Permission

"""
Modelo para el manejo de los permisos para los modulos
"""


class GroupModulePermissionManager(models.Manager):
    """Obtiene los módulos con su respectivo menú del grupo requerido que estén activos"""

    def get_group_module_permission_active_list(self, group_id):
        return self.select_related("module", "module__menu").filter(
            group_id=group_id, module__is_active=True
        )


"""
Modelo para asociar los grupos con modulos, ademas dedefinir los permisos que tiene cada grupo sobre cada modulo asignado
"""


class GroupModulePermission(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.PROTECT,
        verbose_name="Grupo",
        related_name="module_permissions",
    )
    module = models.ForeignKey(
        "security.Module",
        on_delete=models.PROTECT,
        verbose_name="Módulo",
        related_name="group_permissions",
    )
    permissions = models.ManyToManyField(Permission, verbose_name="Permisos")
    # Manager personalizado (conserva toda la funcionalidad del manager por defecto)
    objects = GroupModulePermissionManager()

    def __str__(self):
        return f"{self.module.name} - {self.group.name}"

    class Meta:
        verbose_name = "Grupo módulo permiso"
        verbose_name_plural = "Grupos módulos permisos"
        ordering = ["group", "module"]
        constraints = [
            models.UniqueConstraint(
                fields=["group", "module"], name="unique_group_module"
            )
        ]
