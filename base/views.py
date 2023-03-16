from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Presenca, Aluno
from reportlab.pdfgen import canvas
from datetime import datetime, timedelta, timezone
import pytz


def formulario_presenca(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        codigo = request.POST.get('codigo')
        presenca = Presenca.objects.filter(codigo_adm=codigo).first()
        if presenca:
            Aluno.objects.create(codigo_aluno=codigo, nome=nome)
            return redirect('success')
        else:
            return redirect('erro')
    return render(request, 'base/formulario_presenca.html')


@login_required
def gerar_codigo_presenca(request):
    if request.method == 'POST':
        Presenca.objects.all().delete()
        codigo = request.POST.get('codigo')
        data = request.POST.get('data')
        Presenca.objects.create(codigo_adm=codigo, data_adm=data)
        Aluno.objects.all().delete()
        return redirect('formulario_presenca')
    return render(request, 'base/gerar_codigo_presenca.html')


def success(request):
    return render(request, 'base/success.html')


def login(request):
    return render(request, 'base/login.html')


def erro(request):
    return render(request, 'base/erro.html')


def gerar_pdf(request):
    local_tz = pytz.timezone('Brazil/East')  # substitua pelo seu fuso horário local
    um_dia = datetime.now() - timedelta(minutes=10)

    # Obtém todos os alunos presentes na aula
    alunos = Aluno.objects.filter(data_aluno__gt=um_dia)

    # Cria um objeto PDF com o tamanho da página A4
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="lista_presenca.pdf"'
    p = canvas.Canvas(response, pagesize=(595.27, 841.89))

    # Define o título do documento
    p.setTitle("Lista de Presença")

    # Define o tamanho da fonte e escreve o título
    p.setFontSize(16)
    p.drawString(220, 800, "Lista de Presença")

    # Define o tamanho da fonte e escreve o cabeçalho da tabela
    p.setFontSize(12)
    p.drawString(30, 750, "Nome do Aluno")
    p.drawString(250, 750, "Presente")
    p.drawString(500, 750, "Data")

    # Itera sobre todos os alunos e escreve seus nomes na tabela
    y = 700
    for aluno in alunos:
        data_aluno_local = aluno.data_aluno.astimezone(local_tz)
        data_formatada = data_aluno_local.strftime("%d/%m/%Y")
        p.drawString(30, y, aluno.nome)
        p.drawString(280, y, "Sim")
        p.drawString(480, y, data_formatada)
        y -= 20

    # Salva o documento PDF e retorna a resposta
    p.showPage()
    p.save()
    return response
