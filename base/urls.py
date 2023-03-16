from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import formulario_presenca, gerar_codigo_presenca, success, erro, gerar_pdf
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', formulario_presenca, name='formulario_presenca'),
    path('adminlq/', login_required(gerar_codigo_presenca), name='gerar_codigo_presenca'),
    path('success/', success, name='success'),
    path('erro/', erro, name='erro'),
    path('accounts/login/', LoginView.as_view(template_name='base/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('gerar_pdf/', gerar_pdf, name='gerar_pdf'),
]
