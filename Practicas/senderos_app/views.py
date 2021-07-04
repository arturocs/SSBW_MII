from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from senderos_app import models
from .forms import ComentarioForm, ExcursionForm
import os
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
import logging
from mongoengine.queryset.visitor import Q
from rest_framework.permissions import BasePermission, IsAdminUser, SAFE_METHODS
from rest_framework.views import APIView
from rest_framework.response import Response
from senderos_app.serializers import ExcursionSerializer
from rest_framework import status
from django.http import Http404
from bson.json_util import dumps
logger = logging.getLogger(__name__)

def excursion(request, id):
	excursion = models.Excursion.objects.get(id = id)
	if request.method == "GET":
		excursion.visitas +=1
		excursion.save()
		context = {
			'formulario': ExcursionForm({
				"nombre": excursion.nombre, 
				"descripcion": excursion.descripcion,
				"tags": ' '.join(list(excursion.tags)),
			}),
			'excursion': excursion,
			'comentario': ComentarioForm(),
		}
		return render(request, "senderos_app/excursion.html", context)
	elif request.method == "POST":
		if(request.POST.get("method", "") == "delete"):
			excursion.delete()
			return HttpResponseRedirect("/")

		elif(request.POST.get("method", "") == "like"):
			excursion.likes = excursion.likes + 1
			excursion.save()
			return HttpResponseRedirect("/excursion/" + id)

		elif(request.POST.get("method", "") == "comentario"):
			form = ComentarioForm(request.POST)
			comentario = models.Comentarios(contenido = form['contenido'].value(), autor = form['autor'].value())
			excursion.comentarios.append(comentario)
			excursion.save()
			return HttpResponseRedirect("/excursion/" + id)
	return HttpResponseNotFound()

def _handle_uploaded_file(file):
    """Deal with file upload   
    """

    # Write the file to media folder
    destination = open(os.path.join(settings.BASE_DIR, f'static/img/{file.name}'), 'wb+')
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()


def nueva_excursion(request):
	if request.method == "POST":
		form = ExcursionForm(request.POST, request.FILES)
		fotos = []
		for file in request.FILES.getlist('fotos'):
			fotos.append("img/"+file.name)
			_handle_uploaded_file(file)

		excursion = models.Excursion(nombre = form['nombre'].value(), descripcion = form['descripcion'].value(),
				tags = form['tags'].value().split(" "), fotos = fotos)
		excursion.save()
		logger.info("Añadida nueva excursion")
		return HttpResponseRedirect("/")


def editar_excursion(request, id):
	excursion = models.Excursion.objects.get(id = id)
	if request.method == "POST":
		form = ExcursionForm(request.POST, request.FILES)

		form = ExcursionForm(request.POST, request.FILES)
		fotos = []
		for file in request.FILES.getlist('fotos'):
			fotos.append("img/"+file.name)
			_handle_uploaded_file(file)

		excursion.nombre = form['nombre'].value()
		excursion.descripción = form['descripcion'].value()
		excursion.tags = form['tags'].value().split(" ")
		excursion.fotos = fotos
		excursion.save()
		logger.info(f"Modificada excursion {id}")
		return HttpResponseRedirect("/excursion/" + id)


def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=password)
			login(request, user)

			logger.info(f"Usuario {username} creado")

			return HttpResponseRedirect('/')

		else:
			logger.error("No se pudo crear el usuario")
			return render(request, 'registration/signup.html', {'form': form})
	else:
		form = UserCreationForm()
		return render(request, 'registration/signup.html', {'form': form})


def buscar(request):
	busqueda = request.POST.get('busqueda', '')
	context = {
		'excursiones' : models.Excursion.objects(Q(nombre__icontains=busqueda) | Q(descripcion__icontains=busqueda)),
	}

	return render(request, "senderos_app/index.html", context)

def nuevo_comentario(request, id):
	if request.method == "POST":
		excursion = models.Excursion.objects.get(id = id)
		form = ComentarioForm(request.POST)

		if form.is_valid():
			comentario = models.Comentarios(contenido = form['contenido'].value(), 
					autor = form['autor'].value())

			excursion.comentarios.append(comentario)
			excursion.save()

			logger.info(f"Añadido nuevo comentario en excursion {id}")
		
			return HttpResponseRedirect("/excursion/" + id)

		else:
			logger.error(f"No se ha podido crear comentario en excursion {id}")

def like(request, id):
	excursion = models.Excursion.objects.get(id = id)
	like = request.GET.get("like")

	if like == "true":
		excursion.likes += 1
	else:
		excursion.likes -= 1
	
	excursion.save()

	logger.info(f"Modificado likes de excursion {id}")

	return HttpResponse(excursion.likes)

def index(request):
	context = {
		'excursiones': models.Excursion.objects.all(),
		'formulario': ExcursionForm()
	}
	return render(request, "senderos_app/index.html", context)

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class ExcursionView(APIView):

	permission_classes = [IsAdminUser|ReadOnly]
    
	def get_object(self, id):
		try:
			return models.Excursion.objects.get(id=id)
		except models.Excursion.DoesNotExist:
			raise Http404

	def get(self, request, id, format=None):
		excursion = self.get_object(id)
		serializer = ExcursionSerializer(excursion)
		return Response(serializer.data)

	def put(self, request, id, format=None):
		excursion = self.get_object(id)
		serializer = ExcursionSerializer(excursion, data=request.data)
		serializer.save()
		return Response(serializer.data)
		

	def delete(self, request, id, format=None):
		excursion = self.get_object(id)
		excursion.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class ExcursionesView(APIView):

	permission_classes = [IsAdminUser|ReadOnly]

	def get(self, request):
		print(dumps(models.Excursion.objects.all()))
		return Response({"excursiones": dumps(i) for i in models.Excursion.objects.all()})

	def post(self, request):
		serializer = ExcursionSerializer(data=request.data)
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)


