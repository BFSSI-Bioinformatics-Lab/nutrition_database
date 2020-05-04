
from django.views import generic
from django.shortcuts import render_to_response
import json
from cnf_xplor.api.models import Food, ConversionFactor
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class Search(LoginRequiredMixin, generic.TemplateView):
    template_name = 'food_search/food_search.html'


class ConversionFactor_Detail(LoginRequiredMixin, generic.detail.DetailView):
    model = Food
    template_name = 'food_search/conversionfactor_detail.html'
    context_object_name = 'food'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Nutrient_Detail(LoginRequiredMixin, generic.detail.DetailView):
    model = Food
    template_name = 'food_search/nutrient_detail.html'
    context_object_name = 'food'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



class Food_Detail(LoginRequiredMixin, generic.detail.DetailView):
    model = Food
    template_name = 'food_search/food_detail.html'
    context_object_name = 'food'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

