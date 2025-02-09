from django.contrib import admin

# Register your models here.
from .models import Metodologia,Ferramenta

@admin.register(Metodologia)
class MetodologiaAdmin(admin.ModelAdmin):
    list_display=['nome','slug']
    prepopulated_fields={'slug':('nome',)}
    
@admin.register(Ferramenta)
class FerramentaAdmin(admin.ModelAdmin):
    list_display=[
        'nome',
        'slug',
        'preco',
        'disponivel',
        'criado',
        'atualizado'
    ]
    list_filter=[
        'disponivel',
        'criado',
        'atualizado'
        
    ]
    
    list_editable=[
        'preco',
        'disponivel'
    ]
    
    prepopulated_fields={
        'slug':('nome',)
    }