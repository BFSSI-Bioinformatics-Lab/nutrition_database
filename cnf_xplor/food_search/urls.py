from django.conf.urls import url
from cnf_xplor.food_search import views

urlpatterns = [
    url(r'^$', views.Search.as_view(), name='food_search'),
    url(r'food/(?P<pk>\d+)/$', views.Food_Detail.as_view(), name='food_detail'),
    url(r'conversionfactor/(?P<pk>\d+)/$', views.ConversionFactor_Detail.as_view(), name='conversionfactor_detail'),
    url(r'nutrient/(?P<pk>\d+)/$', views.Nutrient_Detail.as_view(), name='nutrient_detail'),

]


