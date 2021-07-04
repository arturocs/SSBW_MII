# populate.py
from mongoengine import connect, Document, EmbeddedDocument
from mongoengine.fields import EmbeddedDocumentField, StringField, ListField, IntField, DateTimeField
from datetime import datetime

connect('senderos', host='mongo')


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
    fotos = ListField(StringField(required=True))


comentarios = [
    {
        "contenido": 'Primer comentario',
        "autor": 'Yo'
    },
    {
        "contenido": 'Otro comentario',
        "autor": 'Pepito'
    }
]


excursion = Excursion(nombre="Alhama, la ciudad de los tajos", descripcion="Famosa por sus baños árabes explotados desde tiempos romanos,\
 la ciudad de Al-hamman (Alhama), importante plaza del reino nazarí, es un símbolo de la reconquista cristiana del Reino de Granada. \
 Su historia, marcada por la presencia musulmana, se encuentra indefectiblemente enmarcada en el paraje natural de los Tajos, apareciendo,\
  tal como escribiese el poeta Teóphile Gautier, “colgada sobre una enorme roca o pico, como un nido de águila”.", duracion="2,5h",
                      comentarios=comentarios, fotos=["img/alhama1.jpg", "img/alhama2.jpg"])
excursion.save()

excursion = Excursion(nombre="Barranco de La Fonfría y pino de La Señora", descripcion="El Parque Natural de la Sierra de Baza ofrece un \
refrescante recorrido por el arroyo de Baúl que permite contemplar uno de los mayores ejemplares de pino laricio de la provincia de Granada. \
La ruta circular comienza en el Centro de Visitantes de Narváez, ascendiendo en parte por el GR-7 y tomando un desvío en la cabecera del arroyo del Baúl.",
                      comentarios=comentarios, fotos=["img/fonfria1.jpg", "img/fonfria2.jpg", "img/fonfria3.jpg", "img/fonfria4.jpg", "img/fonfria5.jpg"], duracion="7,5h")
excursion.save()

excursion = Excursion(nombre="Acequia del Toril y dólmenes de Alicún", descripcion="Este corta y sencilla ruta permite contemplar los dólmenes \
situados junto al Balneario de Alicún de las Torres y la espectacular y extraña pared mineral que ha formado una acequia de aguas termales a través\
 de los siglos. La presencia de aguas termales a una temperatura de 35 grados, así como su posición estratégica entre dos valles, ha favorecido la\
     creación de asentamientos humanos desde la Prehistoria en este lugar. Prueba de ello es  la presencia de restos del Paleolítico Superior,\
          Neolítico, Edad del Cobre y Cultura del Argar.", comentarios=comentarios,
                      fotos=["img/acequia-alicun1.jpg", "img/acequia-alicun2.jpg", "img/acequia-alicun3.jpg", "img/acequia-alicun4.jpg", "img/acequia-alicun5.jpg", ], duracion="1h")
excursion.save()

excursion = Excursion(nombre="Prueba", descripcion="ruta 1", likes=1,
                      tags=['fácil'], comentarios=comentarios, fotos=["img/foto1.png"])
excursion.save()  # Para escribir en la BD


for excursion in Excursion.objects():
    print(excursion)
