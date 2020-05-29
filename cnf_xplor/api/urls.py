
from django.urls import include, path
from django.conf.urls import url
from rest_framework import routers
from cnf_xplor.api import views


router = routers.DefaultRouter()
router.register(r'food', views.FoodDataTables, base_name='food')
router.register(r'nutrient', views.NutrientDataTables, base_name='nutrient')
router.register(r'conversionfactor', views.ConversionFactorDataTables, base_name='conversionfactor')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    url('nutrient_update/(?P<pk>\d+)/$', views.NutrientUpdate.as_view(), name='nutrient_update'),
    url('conversionfactor_update/(?P<pk>\d+)/$', views.ConversionFactorUpdate.as_view(), name='cf_update'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

