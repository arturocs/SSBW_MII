from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import EmbeddedDocumentField, StringField, ListField, IntField, DateTimeField
from datetime import datetime
excursiones
class Comentarios(EmbeddedDocument):
    contenido = StringField(required=True)
    autor = StringField(max_length=120, required=True)
    fecha = DateTimeField(default=datetime.now())

class Excursion(Document):
    nombre = StringField(max_length=120, required=True)
    descripcion = StringField(required=True)
    likes = IntField(default=0)
    visitas = IntField(default=0)
    tags = ListField(StringField(max_length=20))
    duracion = StringField(max_length=20)
    comentarios = ListField(EmbeddedDocumentField(Comentarios))
    fotos = ListField(StringField())
