from django.urls import path
from django.conf.urls import url
import cnf_xplor.item_enter.views as views

urlpatterns = [
    url(r'^$', views.Choose.as_view(), name='item_enter'),
    path('create_food/', views.FoodCreate.as_view()),
    path('create_nutrient/', views.NutrientCreate.as_view()),
    path('create_conversionfactor/', views.ConverserionFactorCreate.as_view()),
    path('entered/<int:pk>/', views.Success.as_view()),
    path('update/<int:pk>/', views.FoodUpdate.as_view()),
]

