from django.db import models
from django.utils.translation import gettext_lazy as _

#tareas de obra

class progressManagementManager(models.Manager):
    def create_gestion_avances(self, obra, latitud ,longitud , tareas=None, observaciones=None, nota_de_voz=None):
        if not longitud or not latitud:
            raise ValueError(_('La latitud y la Longitud son campos obligatorios para la gestión de obra'))

        gestion_avances = self.model(
            obra=obra,
            latitud=latitud,
            longitud=longitud,
            tareas=tareas,
            observaciones=observaciones,
            nota_de_voz=nota_de_voz
        )

        # gestion_avances.save(using=self._db)
        # if peones:
        #     gestion_avances.peones.add(*peones)
        # if ayudantes:
        #     gestion_avances.ayudantes.add(*ayudantes)

        return gestion_avances

class CustomProgressManagement(models.Model):
    # Campos de la obra


    latitud = models.CharField(max_length=255, verbose_name=_('Latitud'))
    longitud = models.CharField(max_length=255,verbose_name=_('Longitud'))
    observaciones = models.CharField(max_length=15000,verbose_name=_('Observaciones'))
    obra =  models.ForeignKey('CustomWorkManagement', on_delete=models.SET_NULL, null=True, related_name='obras')
    tareas = models.ForeignKey('CustomJobManagement', on_delete=models.SET_NULL, null=True, related_name='tareas_obra')
    nota_de_voz = models.FileField(upload_to='notas_de_voz/', blank=True, null=True)


    objects = progressManagementManager()

    class Meta:
        verbose_name = 'Gestión de Progreso'
        verbose_name_plural = 'Gestiones de Progreso'

    def __str__(self):
        return self.obra






