from django.conf.urls import url
from cnf_xplor.history import views

urlpatterns = [
    url(r'^$', views.History.as_view(), name='history'),
    url(r'nutrient_history/(?P<nutr_amount_c>\d+)/$', views.NutrientHistory.as_view(), name='nutrienthistory'),
    url(r'nutrient_revert/(?P<nutr_amount_c>\d+)/(?P<history_pk>\d+)/$', views.NutrientRevert.as_view(), name='nutrienthistory'),
    url(r'food_history/(?P<food_c>\d+)/$', views.FoodHistory.as_view(), name='nutrienthistory'),
]

