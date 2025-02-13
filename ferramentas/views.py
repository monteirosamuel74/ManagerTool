from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .models import Grupo, Ferramenta, PDCA, EtapaPDCA
from .forms import GrupoForm, FerramentaForm, PDCAForm, EtapaPDCAForm
from django.contrib.auth.decorators import login_required

from .models import Metodologia, Ferramenta
# Create your views here.

def ferramenta_list(request,metodologia_slug=None):
    print("01")
    if request.user.is_authenticated:
        print("02")
        return redirect('login')
    metodologia=None
    metodologias=Metodologia.objects.all()
    ferramentas=Ferramenta.objects.filter(disponivel=True)
    if metodologia_slug:
        metodologia=get_object_or_404(Metodologia,slug=metodologia_slug)
        ferramentas=ferramentas.filter(metodologia=metodologia)
        
    return render(
        request,
        'ferramentas/ferramenta/lista_ferramentas.html',
        {
            'metodologia':metodologia,
            'metodologias':metodologias,
            'ferramentas':ferramentas
        }
    )
    
    
    
def registrar(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Faz login automaticamente após o registro
            return redirect('ferramentas:lista_ferramentas')
    else:
        form = UserCreationForm()
    return render(request, 'ferramentas/registrar.html', {'form': form})



@login_required
def criar_grupo(request):
    if request.method == 'POST':
        form = GrupoForm(request.POST)
        if form.is_valid():
            grupo = form.save(commit=False)
            grupo.save()
            grupo.membros.add(request.user)  # Adiciona o usuário atual ao grupo
            return redirect('ferramentas:lista_grupos')
    else:
        form = GrupoForm()
    return render(request, 'ferramentas/criar_grupo.html', {'form': form})



@login_required
def lista_grupos(request):
    grupos = Grupo.objects.filter(membros=request.user)
    return render(request, 'ferramentas/lista_grupos.html', {'grupos': grupos})



@login_required
def criar_ferramenta(request):
    if request.method == 'POST':
        form = FerramentaForm(request.POST, request.FILES)
        if form.is_valid():
            ferramenta = form.save(commit=False)
            ferramenta.dono = request.user
            ferramenta.save()
            return redirect('ferramentas:lista_ferramentas')
    else:
        form = FerramentaForm()
    return render(request, 'ferramentas/criar_ferramenta.html', {'form': form})



@login_required
def editar_ferramenta(request, id):
    ferramenta = get_object_or_404(Ferramenta, id=id)
    if ferramenta.dono != request.user:
        return redirect('ferramentas:lista_ferramentas')
    if request.method == 'POST':
        form = FerramentaForm(request.POST, request.FILES, instance=ferramenta)
        if form.is_valid():
            form.save()
            return redirect('ferramentas:lista_ferramentas')
    else:
        form = FerramentaForm(instance=ferramenta)
    return render(request, 'ferramentas/editar_ferramenta.html', {'form': form})



@login_required
def lista_pdcas(request):
    pdcas = PDCA.objects.filter(criado_por=request.user)  # Mostra apenas PDCA do usuário
    return render(request, 'ferramentas/lista_pdcas.html', {'pdcas': pdcas})



@login_required
def criar_pdca(request):
    if request.method == 'POST':
        form = PDCAForm(request.POST)
        if form.is_valid():
            pdca = form.save(commit=False)
            pdca.criado_por = request.user  # Associa o PDCA ao usuário atual
            pdca.save()
            return redirect('ferramentas:lista_pdcas')
    else:
        form = PDCAForm()
    return render(request, 'ferramentas/criar_pdca.html', {'form': form})



@login_required
def detalhe_pdca(request, id):
    pdca = get_object_or_404(PDCA, id=id)
    etapas = pdca.etapas.all()
    return render(request, 'ferramentas/detalhe_pdca.html', {'pdca': pdca, 'etapas': etapas})



@login_required
def adicionar_etapa(request, id):
    pdca = get_object_or_404(PDCA, id=id)
    if request.method == 'POST':
        form = EtapaPDCAForm(request.POST)
        if form.is_valid():
            etapa = form.save(commit=False)
            etapa.pdca = pdca
            etapa.save()
            return redirect('ferramentas:detalhe_pdca', id=pdca.id)
    else:
        form = EtapaPDCAForm()
    return render(request, 'ferramentas/adicionar_etapa.html', {'form': form, 'pdca': pdca})



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('registration/login.html')  # Altere 'nome_da_view_principal' para a view principal do seu app
        else:
            # Erro de autenticação
            return render(request, 'login.html', {'error': 'Credenciais inválidas'})
    return render(request, 'registration/login.html')