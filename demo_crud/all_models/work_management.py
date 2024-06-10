from django.db import models
from django.utils.translation import gettext_lazy as _

#Obras
class workManagementManager(models.Manager):
    def create_gestion_obra(self, nombre, direccion, director=None, capataz=None, peones=None, ayudantes=None
                            ,estado="nueva",reporte=None):
        if not nombre or not direccion:
            raise ValueError(_('El nombre y la dirección son campos obligatorios para la gestión de obra'))

        gestion_obra = self.model(
            nombre=nombre,
            direccion=direccion,
            director=director,
            capataz=capataz,
            estado=estado,
            reporte=reporte
        )

        gestion_obra.save(using=self._db)
        if peones:
            gestion_obra.peones.add(*peones)
        if ayudantes:
            gestion_obra.ayudantes.add(*ayudantes)

        return gestion_obra

class CustomWorkManagement(models.Model):
    # Campos de la obra
    ESTADOS = [
        ('nueva', 'Nueva'),
        ('en_desarrollo', 'En Desarrollo'),
        ('finalizada', 'Finalizada'),
    ]

    nombre = models.CharField(max_length=255, verbose_name=_('Nombre'))
    direccion = models.CharField(max_length=255, verbose_name=_('Dirección'))
    estado = models.CharField(max_length=255, choices=ESTADOS,verbose_name=_('Estado'))
    reporte = models.CharField(max_length=1500,verbose_name=_('Reporte'))


    

    # Relaciones con personas que participan en la obra
    director = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, related_name='obras_dirigidas')
    capataz = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, related_name='obras_capataz')
    peones = models.ManyToManyField('CustomUser', related_name='obras_peon', blank=True)
    ayudantes = models.ManyToManyField('CustomUser', related_name='obras_ayudante', blank=True)
  


    objects = workManagementManager()

    class Meta:
        verbose_name = 'Gestión de Obra'
        verbose_name_plural = 'Gestiones de Obra'

    def __str__(self):
        return self.nombre
