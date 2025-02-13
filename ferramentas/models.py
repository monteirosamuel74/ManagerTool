from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.
class Metodologia(models.Model):
    nome=models.CharField(max_length=200)
    slug=models.SlugField(max_length=200,unique=True)
    
    class Meta:
        ordering=['nome']
        indexes=[
            models.Index(fields=['nome']),
        ]
        verbose_name='metodologia'
        verbose_name_plural='metodologias'
    
    def get_absolute_url(self):
        return reverse(
            'ferramentas:lista_ferramentas_por_metodologia', 
            args=[self.slug]
            )
    
    def __str__(self):
        return self.nome

  

class Grupo(models.Model):
    nome = models.CharField(max_length=200)
    membros = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='grupos')

    def __str__(self):
        return self.nome
    

    
class Ferramenta(models.Model):
    metodologia=models.ForeignKey(
        Metodologia,
        related_name='ferramentas',
        on_delete=models.CASCADE
    )
    
    nome=models.CharField(max_length=200)
    slug=models.SlugField(max_length=200)
    imagem=models.ImageField(
        upload_to='ferramentas/%Y/%m/%d',
        blank=True
    )
    
    descricao=models.TextField(blank=True)
    preco=models.DecimalField(max_digits=10,decimal_places=2)
    disponivel=models.BooleanField(default=True)
    criado=models.DateTimeField(auto_now_add=True)
    atualizado=models.DateTimeField(auto_now=True)
    grupo = models.ForeignKey('Grupo', related_name='ferramentas', on_delete=models.SET_NULL, null=True, blank=True)
    dono = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ferramentas', on_delete=models.CASCADE)
    
    class Meta:
        ordering=['nome']
        indexes=[
            models.Index(fields=['id','slug']),
            models.Index(fields=['nome']),
            models.Index(fields=['criado']),
        ]
        
    def __str__(self):
        return self.nome
  
  
  
class PDCA(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='pdcas', on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, related_name='pdcas', on_delete=models.SET_NULL, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome



class EtapaPDCA(models.Model):
    PDCA_CHOICES = [
        ('PLAN', 'Planejar'),
        ('DO', 'Fazer'),
        ('CHECK', 'Verificar'),
        ('ACT', 'Agir'),
    ]
    pdca = models.ForeignKey(PDCA, related_name='etapas', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=5, choices=PDCA_CHOICES)
    descricao = models.TextField()
    concluido = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.pdca.nome}"
    
    
    
