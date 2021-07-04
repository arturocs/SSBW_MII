from senderos_app.models import Excursion
from rest_framework import serializers

class ExcursionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Excursion
        fields = ['nombre', 'descripcion', 'likes', 'visitas', 'flags', 'comentarios', 'fotos']