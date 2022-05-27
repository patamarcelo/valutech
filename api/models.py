from django.db import models

from django.conf import settings
User = settings.AUTH_USER_MODEL

class Base(models.Model):
    criados    = models.DateTimeField('Criação', auto_now_add=True)
    modificado = models.DateTimeField('Atualização', auto_now=True)
    ativo      = models.BooleanField('Ativo', default=True)    


    class Meta:
        abstract = True


class ValuRisk(Base):
    data       = models.DateField('Data')
    abertura   = models.DecimalField('Abertura',max_digits=6, decimal_places=3, null=True, blank=True)
    fechamento = models.DecimalField('Fechamento',max_digits=6, decimal_places=3, null=True, blank=True)
    minimo     = models.DecimalField('Mínima',max_digits=6, decimal_places=3, null=True, blank=True)
    maxima     = models.DecimalField('Máxima',max_digits=6, decimal_places=3, null=True, blank=True)
    user       = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['data']
        verbose_name = 'ValuRisk'
        verbose_name_plural = 'ValuRisks'
    
    def __str__(self):
        return f'Data: {self.data} - Fechamento: {self.fechamento}'

