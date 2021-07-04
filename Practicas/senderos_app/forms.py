from django import forms

class ComentarioForm(forms.Form):
    autor = forms.CharField(label='Autor', max_length=50)
    contenido = forms.CharField(label='Comentario', max_length=1000)

class ExcursionForm(forms.Form):
    nombre = forms.CharField(label='Título', max_length=100, required=True)
    descripcion = forms.CharField(label='Descripción de la ruta', max_length = 1000, required=True)
    tags = forms.CharField(label= 'Etiquetas', max_length=200, required=True)
    fotos = forms.ImageField(widget=forms.ClearableFileInput())
