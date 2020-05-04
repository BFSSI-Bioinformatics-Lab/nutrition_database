from cnf_xplor.api.models import Food, Nutrient, NutrientOfFood, ConversionFactor, FoodGroup, Measure, NutrientReference, NutrientSource
from rest_framework import serializers


class GroupSerializer(serializers.ModelSerializer):
    lookup_field = 'GROUP_C'
    class Meta:
        model = FoodGroup
        fields = '__all__'

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'

    #GROUP = GroupSerializer()
    GROUP_DESC = serializers.SerializerMethodField('get_group_desc')
    GROUP_DESC_F = serializers.SerializerMethodField('get_group_desc_F')
    def get_group_desc(self, obj):
        return obj.GROUP.GROUP_DESC
    def get_group_desc_F(self, obj):
        return obj.GROUP.GROUP_DESC_F


class NutrientSerializer(serializers.ModelSerializer):
    lookup_field = 'NUTR_C'
    class Meta:
        model = Nutrient
        fields = '__all__'


class NutrientReferenceSerializer(serializers.ModelSerializer):
    lookup_field = 'REF_C'
    class Meta:
        model = NutrientReference
        fields = '__all__'


class NutrientSourceSerializer(serializers.ModelSerializer):
    lookup_field = 'NUTR_SOURCE_C'
    class Meta:
        model = NutrientSource
        fields = '__all__'



class NutrientOfFoodSerializer(serializers.ModelSerializer):
    lookup_field = 'NUTR_AMOUNT_C'
    class Meta:
        model = NutrientOfFood
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': False},
            'slug': {'validators': []},
        }

    NUTR = NutrientSerializer(read_only=True)
    SOURCE = NutrientSourceSerializer(read_only=True)
    REF = NutrientReferenceSerializer(read_only=True)

    NUTR_C = serializers.SerializerMethodField('get_nutrc')
    def get_nutrc(self, obj):
        if obj.NUTR is None:
            return None
        return obj.NUTR.NUTR_C
    REF_C = serializers.SerializerMethodField('get_refc')
    def get_refc(self, obj):
        if obj.REF is None:
            return None
        return obj.REF.REF_C

    #NUTR_SYMBOL = serializers.SerializerMethodField('get_symbol')
    #def get_symbol(self, obj):
    #    return obj.NUTR.NUTR_SYMBOL
    #NUTR_UNIT = serializers.SerializerMethodField('get_unit')
    #def get_unit(self, obj):
    #    return obj.NUTR.UNIT


class MeasureSerializer(serializers.ModelSerializer):
    lookup_field = "MEASURE_ID"
    class Meta:
        model = Measure
        fields = '__all__'


class ConversionFactorSerializer(serializers.ModelSerializer):
    lookup_field = 'CF_FACTOR_C'
    class Meta:
        model = ConversionFactor
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': False},
            'slug': {'validators': []},
        }

    MEASURE_ID = MeasureSerializer(read_only=True)
