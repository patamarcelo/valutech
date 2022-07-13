from django.db import models

from django.conf import settings
User = settings.AUTH_USER_MODEL

class Base(models.Model):
    criados    = models.DateTimeField('Criação', auto_now_add=True)
    modificado = models.DateTimeField('Atualização', auto_now=True)
    ativo      = models.BooleanField('Ativo', default=True)    


    class Meta:
        abstract = True

class NpData(Base):
    nome    = models.CharField('Nome do arquivo', max_length=100 )
    arquivo = models.FileField('Arquivo gerado', upload_to='np_files/')
    user    = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['criados']
        verbose_name = 'NpData'
        verbose_name_plural = 'NpDatas'

    def __str__(self):
        return f'Arquivo: {self.nome} {self.arquivo}'