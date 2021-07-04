from django.urls import path
from . import views

urlpatterns = [
    path('excursion/<str:id>/', views.excursion, name="excursion"),
    path('', views.index),
    path('buscar/', views.buscar, name="buscar"),
    path('nueva_excursion/', views.nueva_excursion, name="nueva"),
	path('edit/<str:id>/', views.editar_excursion, name="editar"),
	path('signup/', views.signup, name='signup'),
	path('add_comment/<str:id>/', views.editar_excursion, name="nuevo_comentario"),
	path('like/<str:id>/', views.like, name="like"),
    path('api/excursiones/', views.ExcursionesView.as_view(),name="excursiones_api"),
	path('api/excursion/<str:id>/', views.ExcursionView.as_view(), name = "excursion_api"),
]
