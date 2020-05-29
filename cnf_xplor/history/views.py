from django.views import generic
from cnf_xplor.api.models import Nutrient, Food, NutrientOfFood
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class History(LoginRequiredMixin, generic.TemplateView):
    template_name = 'history/history.html'


class NutrientHistory(LoginRequiredMixin, generic.ListView):
    model = NutrientOfFood
    template_name = 'history/nutrient_history.html'
    context_object_name = 'nutrient_h'
    def get_queryset(self):
        n = NutrientOfFood.objects.get(pk=self.kwargs['nutr_amount_c'])
        return list(n.history.all())


class FoodHistory(LoginRequiredMixin, generic.ListView):
    model = Nutrient
    template_name = 'history/food_history.html'
    context_object_name = 'food_h'
    def get_queryset(self):
        n = Food.objects.get(pk=self.kwargs['food_c'])
        return n.history.all()


class NutrientRevert(LoginRequiredMixin, generic.TemplateView):
    template_name = 'success.html'
    def post(self, request, nutr_amount_c, history_pk):
        h_all = NutrientOfFood.objects.get(pk=nutr_amount_c).history.all()
        h = [x for x in h_all if x.pk==int(history_pk)]
        assert len(h) == 1 # Or return an error
        h = h[0].instance
        h.changeReason = "history reversion"
        h.save()
        return redirect('/history/nutrient_history/%s/' %(nutr_amount_c) ) #Does not seem to work, and I"m just reloading the page in javascript

