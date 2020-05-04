from django.views.generic.edit import UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from cnf_xplor.api.models import Food, Nutrient, ConversionFactor
from cnf_xplor.item_enter.forms import EnterFood, EnterNutrient, EnterConversionFactor, UpdateFood
from cnf_xplor.item_enter.update_database import add_all_nutrients_to_food
from datetime import datetime
from simple_history.utils import update_change_reason
from django.shortcuts import redirect


class FoodCreate(LoginRequiredMixin, FormView):
    model = Food
    form_class = EnterFood
    template_name = 'item_enter/basicfood_form.html'
    success_url = '/item_enter/entered/' + str(Food.FOOD_C) + "/"

    def form_valid(self, form):
        f, t = Food.objects.get_or_create(
            SOURCE=form.cleaned_data["SOURCE"],
            COUNTRY_C=form.cleaned_data["COUNTRY_C"],
            GROUP=form.cleaned_data["GROUP"],
            FOOD_DESC=form.cleaned_data["FOOD_DESC"],
            FOOD_DESC_F=form.cleaned_data["FOOD_DESC_F"],
            COMMENT_T=form.cleaned_data["COMMENT_T"],
            FN_COMMENT_F=form.cleaned_data["FN_COMMENT_F"],
            DATE_ENTRY=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        )
        add_all_nutrients_to_food(f)
        return redirect('/item_enter/entered/{}/'.format(f.FOOD_C))
        #return super(FoodCreate, self).form_valid(form)


class NutrientCreate(LoginRequiredMixin, FormView):
    model = Nutrient
    form_class = EnterNutrient
    template_name = 'item_enter/basicfood_form.html'
    success_url = '/item_enter/entered/'

    def form_valid(self, form):
        Nutrient.objects.get_or_create(
            NUTR_SYMBOL=form.cleaned_data["NUTR_SYMBOL"],
            NUTR_NAME=form.cleaned_data["NUTR_NAME"],
            NUTR_NAME_F=form.cleaned_data["NUTR_NAME_F"],
            UNIT=form.cleaned_data["UNIT"],
            DATE_ENTRY=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        )

        return super(NutrientCreate, self).form_valid(form)


class ConverserionFactorCreate(LoginRequiredMixin, FormView):
    model = ConversionFactor
    form_class = EnterConversionFactor
    template_name = 'item_enter/basicfood_form.html'
    success_url = '/item_enter/entered/'

    def form_valid(self, form):
        ConversionFactor.objects.get_or_create(
            FOOD_C=form.cleaned_data["FOOD_C"],
            MEASURE_ID=form.cleaned_data["MEASURE_ID"],
            CONV_FACTOR=form.cleaned_data["CONV_FACTOR"],
            COMMENT_T=form.cleaned_data["COMMENT_T"],
            CF_COMMENT_F=form.cleaned_data["CF_COMMENT_F"],
            DATE_ENTRY=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        )
        return super(ConverserionFactorCreate, self).form_valid(form)


class Success(LoginRequiredMixin, generic.detail.DetailView):
    template_name = 'success.html'
    model = Food
    context_object_name = 'food'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Choose(LoginRequiredMixin, generic.TemplateView):
    template_name = 'item_enter/choose.html'


class FoodUpdate(LoginRequiredMixin, UpdateView):
    model = Food
    template_name = 'item_enter/basicfood_form.html'
    success_url = '/item_enter/entered/'
    form_class = UpdateFood
    def form_valid(self, form):
        f = Food(FOOD_C=self.kwargs["pk"])
        f.changeReason = form.cleaned_data["REASON_FOR_CHANGE"]
        f.SOURCE=form.cleaned_data["SOURCE"]
        f.COUNTRY_C=form.cleaned_data["COUNTRY_C"]
        f.GROUP=form.cleaned_data["GROUP"]
        f.FOOD_DESC=form.cleaned_data["FOOD_DESC"]
        f.FOOD_DESC_F=form.cleaned_data["FOOD_DESC_F"]
        f.COMMENT_T=form.cleaned_data["COMMENT_T"]
        f.FN_COMMENT_F=form.cleaned_data["FN_COMMENT_F"]
        f.DATE_CHANGE=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.save()
        return redirect('/item_enter/entered/{}/'.format(f.FOOD_C))


