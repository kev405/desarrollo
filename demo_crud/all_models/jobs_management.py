from django.db import models
from django.utils.translation import gettext_lazy as _

#tareas de obra

class jobManagementManager(models.Manager):
    def create_gestion_tarea(self, nombre, obra , director=None, capataz=None, peones=None, ayudantes=None
                            ,estado=None,reporte=None):
        if not nombre or not obra:
            raise ValueError(_('El nombre y la obra son campos obligatorios para la gestión de obra'))

        gestion_tarea = self.model(
            nombre=nombre,
            obra=obra,
            director=director,
            capataz=capataz,
            estado=estado,
            reporte=reporte
        )

        gestion_tarea.save(using=self._db)
        if peones:
            gestion_tarea.peones.add(*peones)
        if ayudantes:
            gestion_tarea.ayudantes.add(*ayudantes)

        return gestion_tarea

class CustomJobManagement(models.Model):
    # Campos de la obra
    ESTADOS = [
        ('asignada', 'Asignada'),
        ('en_desarrollo', 'En Desarrollo'),
        ('en_revision', 'En Revisión'),
        ('aceptada', 'Aceptada'),

    ]

    nombre = models.CharField(max_length=255, verbose_name=_('Nombre'))
    estado = models.CharField(max_length=255, choices=ESTADOS,verbose_name=_('Estado'))
    reporte = models.CharField(max_length=15000,verbose_name=_('Reporte'))


    # Relaciones con personas que participan en la obra + la obra
    obra = models.ForeignKey('CustomWorkManagement', on_delete=models.SET_NULL, null=True, related_name='tareas_dirigidas')
    director = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, related_name='tareas_dirigidas')
    capataz = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, related_name='tareas_capataz')
    peones = models.ManyToManyField('CustomUser', related_name='tareas_peon', blank=True)
    ayudantes = models.ManyToManyField('CustomUser', related_name='tareas_ayudante', blank=True)
  


    objects = jobManagementManager()

    class Meta:
        verbose_name = 'Gestión de Tareas'
        verbose_name_plural = 'Gestiones de Tarea'

    def __str__(self):
        return self.nombre
