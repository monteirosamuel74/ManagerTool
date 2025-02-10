from django.contrib import admin
from django.urls import include, path
from . import views

app_name='ferramentas'

urlpatterns = [
    path('', views.ferramenta_list, name='lista_ferramentas'),
    path('registrar/',views.registrar,name='registrar'),
    path('<slug:metodologia_slug>/', views.ferramenta_list, name='lista_ferramentas_por_metodologia'),
    path('editar/<int:id>/', views.editar_ferramenta, name='editar_ferramenta'),
    path('grupos/', views.lista_grupos, name='lista_grupos'),
    path('grupos/criar/', views.criar_grupo, name='criar_grupo'),
    path('pdcas/', views.lista_pdcas, name='lista_pdcas'),
    path('pdcas/criar/', views.criar_pdca, name='criar_pdca'),
    path('pdcas/<int:id>/', views.detalhe_pdca, name='detalhe_pdca'),
    path('pdcas/<int:id>/adicionar-etapa/', views.adicionar_etapa, name='adicionar_etapa'),
    path('login/', views.login_view, name='login'),
]
