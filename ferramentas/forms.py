from django import forms
from .models import Grupo, Ferramenta, PDCA, EtapaPDCA

class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['nome', 'membros']
        
        
class FerramentaForm(forms.ModelForm):
    class Meta:
        model = Ferramenta
        fields = ['metodologia', 'nome', 'slug', 'imagem', 'descricao', 'preco', 'disponivel', 'grupo']
        
        
class PDCAForm(forms.ModelForm):
    class Meta:
        model=PDCA
        fields=['nome','descricao','grupo']
        
        
class EtapaPDCAForm(forms.ModelForm):
    class Meta:
        model=EtapaPDCA
        fields=['tipo','descricao','concluido']