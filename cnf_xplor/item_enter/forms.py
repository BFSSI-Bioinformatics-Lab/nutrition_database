import django.forms as forms
from cnf_xplor.api.models import Food, FoodGroup, FoodSource, Nutrient, ConversionFactor, Measure


class EnterFood(forms.ModelForm):
    class Meta:
        model = Food
        fields = ["GROUP","SOURCE", "COUNTRY_C", "FOOD_DESC", "FOOD_DESC_F", "COMMENT_T", "FN_COMMENT_F"]

    GROUP = forms.ModelChoiceField(queryset=FoodGroup.objects.order_by('GROUP_C'), widget=forms.Select(attrs={'class':'enter-item'}), required=False)
    SOURCE = forms.ModelChoiceField(queryset=FoodSource.objects.order_by('SOURCE_C'), widget=forms.Select(attrs={'class':'enter-item'}), required=False)
    COUNTRY_C = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'enter-item'}), required=False)
    FOOD_DESC = forms.CharField(widget=forms.TextInput(attrs={'class':'enter-item'}), required=False)
    FOOD_DESC_F = forms.CharField(widget=forms.TextInput(attrs={'class':'enter-item'}), required=False)
    COMMENT_T = forms.CharField(widget=forms.TextInput(attrs={'class':'enter-item'}), required=False)
    FN_COMMENT_F = forms.CharField(widget=forms.TextInput(attrs={'class':'enter-item'}), required=False)
    #REASON_FOR_CHANGE = forms.CharField(widget=forms.TextInput(attrs={'class':'enter-item'}), required=False)


class UpdateFood(forms.ModelForm):
    class Meta:
        model = Food
        fields = ["GROUP","SOURCE", "COUNTRY_C", "FOOD_DESC", "FOOD_DESC_F", "COMMENT_T", "FN_COMMENT_F"]

    GROUP = forms.ModelChoiceField(queryset=FoodGroup.objects.order_by('GROUP_C'), widget=forms.Select(attrs={'class':'enter-item'}), required=False)
    SOURCE = forms.ModelChoiceField(queryset=FoodSource.objects.order_by('SOURCE_C'), widget=forms.Select(attrs={'class':'enter-item'}), required=False)
    COUNTRY_C = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'enter-item'}), required=False)
    FOOD_DESC = forms.CharField(widget=forms.TextInput(attrs={'class':'enter-item'}), required=False)
    FOOD_DESC_F = forms.CharField(widget=forms.TextInput(attrs={'class':'enter-item'}), required=False)
    COMMENT_T = forms.CharField(widget=forms.TextInput(attrs={'class':'enter-item'}), required=False)
    FN_COMMENT_F = forms.CharField(widget=forms.TextInput(attrs={'class':'enter-item'}), required=False)
    REASON_FOR_CHANGE = forms.CharField(widget=forms.TextInput(attrs={'class':'enter-item'}), required=False)


class EnterNutrient(forms.ModelForm):
    class Meta:
        model = Nutrient
        fields = ["NUTR_SYMBOL","NUTR_NAME", "NUTR_NAME_F", "UNIT"]

    NUTR_SYMBOL = forms.CharField(widget=forms.TextInput(attrs={'class': 'enter-item'}), required=False)
    NUTR_NAME = forms.CharField(widget=forms.TextInput(attrs={'class':'enter-item'}), required=False)
    NUTR_NAME_F = forms.CharField(widget=forms.TextInput(attrs={'class':'enter-item'}), required=False)
    UNIT = forms.CharField(widget=forms.TextInput(attrs={'class':'enter-item'}), required=False)


class EnterConversionFactor(forms.ModelForm):
    class Meta:
        model = ConversionFactor
        fields = ["FOOD_C","MEASURE_ID", "CONV_FACTOR", "COMMENT_T", "CF_COMMENT_F"]

    FOOD_C = forms.ModelChoiceField(queryset=Food.objects.order_by('FOOD_C'), widget=forms.Select(attrs={'class':'enter-item'}), required=False)
    MEASURE_ID = forms.ModelChoiceField(queryset=Measure.objects.order_by('MEASURE_ID'), widget=forms.Select(attrs={'class':'enter-item'}), required=False)
    CONV_FACTOR = forms.CharField(widget=forms.TextInput(attrs={'class':'enter-item'}), required=False)
    COMMENT_T = forms.CharField(widget=forms.TextInput(attrs={'class':'enter-item'}), required=False)
    CF_COMMENT_F = forms.CharField(widget=forms.TextInput(attrs={'class':'enter-item'}), required=False)
