#!/usr/bin/env python3
# Import Django
from django.db import models
from django.utils import timezone

# Imports External
from decimal import Decimal


# Choices
class DiaSemanaChoices(models.TextChoices):
    LUNES = "lunes", "Lunes"
    MARTES = "martes", "Martes"
    MIERCOLES = "miércoles", "Miércoles"
    JUEVES = "jueves", "Jueves"
    VIERNES = "viernes", "Viernes"
    SABADO = "sábado", "Sábado"
    DOMINGO = "domingo", "Domingo"


# Models
class HorarioAtencion(models.Model):

    # Día de la semana (ej: lunes, martes...)
    dia_semana = models.CharField(
        max_length=10, choices=DiaSemanaChoices.choices, verbose_name="Día de la Semana"
    )

    # Rango principal de atención (ej. 08:00 a 17:00)
    hora_inicio = models.TimeField(verbose_name="Hora de Inicio")
    hora_fin = models.TimeField(verbose_name="Hora de Fin")

    # Pausa para almuerzo u otro intervalo
    intervalo_desde = models.TimeField(
        verbose_name="Intervalo desde", null=True, blank=True
    )
    intervalo_hasta = models.TimeField(
        verbose_name="Intervalo hasta", null=True, blank=True
    )

    activo = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return f"{self.dia_semana}"


class Atencion(models.Model):
    # Paciente que recibe esta atención médica
    paciente = models.ForeignKey(
        "core.Paciente",
        on_delete=models.PROTECT,
        verbose_name="Paciente",
        related_name="atenciones",
        help_text="Paciente que recibe esta atención médica.",
    )

    # Fecha y hora en que se realizó la atención
    fecha_atencion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Atención",
        help_text="Fecha y hora en que se registró la atención.",
    )
    # Signos vitales
    presion_arterial = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Presión Arterial",
        help_text="Ejemplo: 120/80 mmHg.",
    )
    pulso = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Pulso (ppm)",
        help_text="Pulsaciones por minuto.",
    )
    temperatura = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name="Temperatura (°C)",
        help_text="Temperatura corporal en grados Celsius.",
    )
    frecuencia_respiratoria = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Frecuencia Respiratoria (rpm)",
        help_text="Respiraciones por minuto.",
    )
    saturacion_oxigeno = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Saturación de Oxígeno (%)",
        help_text="Porcentaje de oxígeno en sangre.",
    )
    peso = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Peso (kg)",
        help_text="Peso del paciente en kilogramos.",
    )
    altura = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Altura (m)",
        help_text="Altura del paciente en metros.",
    )

    # Motivo y contenido de la atención
    motivo_consulta = models.TextField(
        verbose_name="Motivo de Consulta",
        help_text="Razón principal por la que el paciente acude a consulta.",
    )
    sintomas = models.TextField(
        verbose_name="Síntomas", help_text="Síntomas que presenta el paciente."
    )
    tratamiento = models.TextField(
        verbose_name="Plan de Tratamiento",
        help_text="Indicaciones o receta entregada al paciente.",
    )
    diagnostico = models.ManyToManyField(
        "core.Diagnostico",
        verbose_name="Diagnósticos",
        related_name="atenciones",
        help_text="Diagnósticos clínicos asociados a esta atención.",
    )
    examen_fisico = models.TextField(
        null=True,
        blank=True,
        verbose_name="Examen Físico",
        help_text="Descripción de hallazgos del examen físico.",
    )
    examenes_enviados = models.TextField(
        null=True,
        blank=True,
        verbose_name="Exámenes Solicitados",
        help_text="Exámenes que se han solicitado al paciente.",
    )
    comentario_adicional = models.TextField(
        null=True,
        blank=True,
        verbose_name="Comentario Adicional",
        help_text="Observaciones adicionales del profesional de salud.",
    )
    es_control = models.BooleanField(
        default=False,
        verbose_name="¿Es consulta de control?",
        help_text="Marca si esta atención es parte de un seguimiento.",
    )

    class Meta:
        ordering = ["-fecha_atencion"]
        verbose_name = "Atención Médica"
        verbose_name_plural = "Atenciones Médicas"

    def __str__(self):
        return f"Atención de {self.paciente} el {self.fecha_atencion.strftime('%Y-%m-%d %H:%M')}"

    @property
    def calcular_imc(self):
        """Calcula el Índice de Masa Corporal (IMC) basado en el peso y la altura."""
        if self.peso and self.altura and self.altura > 0:
            return round(float(self.peso) / (float(self.altura) ** 2), 2)
        return None

    @property
    def get_diagnosticos(self):
        return " - ".join(
            [d.descripcion for d in self.diagnostico.all().order_by("descripcion")]
        )


class DetalleAtencion(models.Model):
    atencion = models.ForeignKey(
        Atencion,
        on_delete=models.CASCADE,
        verbose_name="Atención Médica",
        related_name="detalles",
        help_text="Atención médica asociada a este detalle.",
    )
    medicamento = models.ForeignKey(
        "core.Medicamento",
        on_delete=models.PROTECT,
        verbose_name="Medicamento",
        related_name="prescripciones",
        help_text="Medicamento recetado al paciente.",
    )
    cantidad = models.PositiveIntegerField(
        verbose_name="Cantidad", help_text="Unidades del medicamento recetadas."
    )
    prescripcion = models.TextField(
        verbose_name="Prescripción",
        help_text="Instrucciones para tomar el medicamento.",
    )
    duracion_tratamiento = models.PositiveIntegerField(
        verbose_name="Duración del Tratamiento (días)",
        null=True,
        blank=True,
        help_text="Cantidad de días de tratamiento estimado.",
    )
    frecuencia_diaria = models.PositiveIntegerField(
        verbose_name="Frecuencia Diaria (veces por día)",
        null=True,
        blank=True,
        help_text="Cuántas veces al día debe tomar el medicamento.",
    )

    class Meta:
        ordering = ["atencion"]
        verbose_name = "Detalle de Atención"
        verbose_name_plural = "Detalles de Atención"

    def __str__(self):
        return f"{self.medicamento} para {self.atencion.paciente}"
