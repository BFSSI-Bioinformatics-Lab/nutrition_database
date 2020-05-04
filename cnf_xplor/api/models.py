from django.db import models
from simple_history.models import HistoricalRecords


class FoodGroup(models.Model):
    GROUP_C = models.AutoField(null=False, blank=False, primary_key=True)
    GROUP_DESC = models.CharField(max_length=500,null=True,blank=True)
    GROUP_DESC_F = models.CharField(max_length=500,null=True,blank=True)

    GROUP_CODE = models.IntegerField(null=True,blank=True)
    FG_GROUP_ABBRV = models.CharField(max_length=10,null=True,blank=True)
    GROUP_COMPOSITE_FLG = models.BooleanField(null=True,blank=True)
    GROUP_RECIPE_FLG = models.BooleanField(null=True,blank=True)
    FG_DB_SOURCE_C = models.BooleanField(null=True,blank=True)
    FG_BBCA_INDEX = models.IntegerField(null=True,blank=True)
    GROUP_OWNER = models.IntegerField(null=True,blank=True)
    SHARED_GROUP = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.GROUP_DESC + " (%i)" %(self.GROUP_C)

    history = HistoricalRecords()


class FoodSource(models.Model):
    SOURCE_C = models.AutoField(null=False, blank=False, primary_key=True)
    SOURCE_DESC = models.CharField(max_length=500, null=True, blank=True)
    SOURCE_DESC_F = models.CharField(max_length=500, null=True, blank=True)
    NRD_REF = models.IntegerField(null=True,blank=True)
    SHARED_SOURCE = models.BooleanField(null=True,blank=True)
    SOURCE_OWNER = models.IntegerField(null=True,blank=True)
    SOURCE_CNF_OWNER = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.SOURCE_DESC + " (%i)" %(self.SOURCE_C)

    history = HistoricalRecords()


class Food(models.Model):
    # Codes
    FOOD_C = models.AutoField(null=False, blank=False, primary_key=True)
    ENG_NAME = models.CharField(max_length=500,null=True,blank=True)
    FR_NAME = models.CharField(max_length=500,null=True,blank=True)
    FOOD_DESC = models.CharField(max_length=500,null=True,blank=True)
    FOOD_DESC_F = models.CharField(max_length=500,null=True,blank=True)
    NUT_CAN_C = models.IntegerField(null=True,blank=True) # Should this be a ForeignKey??
    CNF_FLAG = models.BooleanField(null=True,blank=True)

    SOURCE = models.ForeignKey(FoodSource, on_delete=models.SET_NULL, null=True)
    COUNTRY_C = models.IntegerField(null=True,blank=True)
    GROUP = models.ForeignKey(FoodGroup, on_delete=models.SET_NULL, null=True)
    COMMENT_T = models.CharField(max_length=500,null=True,blank=True)
    FN_COMMENT_F = models.CharField(max_length=500,null=True,blank=True)

    FOOD_REFERENCE = models.CharField(max_length=500,null=True,blank=True)
    SCIENTIFIC_NAME = models.CharField(max_length=500,null=True,blank=True)
    PUBLICATION_FLAG = models.BooleanField(null=True,blank=True)
    PUBLICATION_CODE = models.CharField(max_length=10,null=True,blank=True)
    ITEM_C = models.IntegerField(null=True,blank=True) # Should this be a ForeignKey??
    SEQUENCE_C = models.IntegerField(null=True,blank=True) # Should this be a ForeignKey??
    LEGACY_GROUP_C = models.IntegerField(null=True,blank=True) # Should this be included # Should this be a ForeignKey??

    COMMON_NM_E = models.CharField(max_length=500,null=True,blank=True)
    COMMON_NM_F = models.CharField(max_length=500,null=True,blank=True)

    FN_DB_SOURCE_C = models.IntegerField(null=True,blank=True)
    FN_RECIPE_FLG = models.BooleanField(null=True,blank=True)
    FN_SYSTEM_VIEW_C = models.IntegerField(null=True,blank=True)
    FN_FAT_CHANGE = models.IntegerField(null=True,blank=True)
    FN_MOISTURE_CHANGE = models.IntegerField(null=True,blank=True)
    FN_SYS_USER_CREATE_C = models.IntegerField(null=True,blank=True)
    FN_SYS_USER_EDIT_C = models.IntegerField(null=True,blank=True)
    FN_TEMPLATE_C = models.IntegerField(null=True,blank=True)
    FN_TEMP = models.IntegerField(null=True,blank=True)
    FN_ARCHIVED = models.IntegerField(null=True,blank=True)
    FN_LEGACY_C = models.CharField(max_length=15, null=True,blank=True)
    US_RECIPE_C = models.IntegerField(null=True,blank=True)
    USDA_MODIFIED = models.BooleanField(null=True,blank=True)
    USDA_TEMP = models.CharField(max_length=35, null=True, blank=True)
    CANADA_FOOD_SUBGROUP_ID = models.IntegerField(null=True,blank=True)
    CFGHE_FLAG = models.IntegerField(null=True,blank=True)
    ORIG_CANADA_FOOD_SUBGROUP_ID = models.IntegerField(null=True,blank=True)
    FOOD_OWNER = models.IntegerField(null=True,blank=True)
    SHARED_FOOD = models.BooleanField(null=True,blank=True)
    CANDI_REC_NUM = models.IntegerField(null=True,blank=True)
    INHERITANCE_FLAG = models.IntegerField(null=True,blank=True)
    FOOD_CODE = models.IntegerField(null=True,blank=True)

    # Dates
    DATE_ENTRY = models.DateTimeField(null=True, blank=True)
    DATE_CHANGE = models.DateTimeField(null=True, blank=True)
    DATE_END = models.DateTimeField(null=True, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.FOOD_C}: {self.ENG_NAME}'


class Nutrient(models.Model):
    NUTR_C = models.AutoField(null=False, blank=False, primary_key=True)
    NUTR_SYMBOL = models.CharField(max_length=500,null=True,blank=True)
    NUTR_NAME = models.CharField(max_length=500,null=True,blank=True)
    NUTR_NAME_F = models.CharField(max_length=500,null=True,blank=True)
    UNIT = models.CharField(max_length=100,null=True,blank=True)
    SEQUENCE_C = models.IntegerField(null=True, blank=True)

    NUTR_CODE = models.IntegerField(null=True, blank=True)
    NUTR_WEB = models.BooleanField(null=True, blank=True)
    NUTR_ACTIVE_FLAG = models.BooleanField(null=True, blank=True)
    NUTR_DECIMAL_PLACE = models.IntegerField(null=True, blank=True)
    NUTR_WEB_ORDER = models.IntegerField(null=True, blank=True)
    NUTRIENT_GROUP_ID = models.IntegerField(null=True, blank=True)

    TAGNAME = models.CharField(max_length=100,null=True,blank=True)
    NUTR_WEB_NAME_E = models.CharField(max_length=100,null=True,blank=True)
    NUTR_WEB_NAME_F = models.CharField(max_length=100,null=True,blank=True)
    PUBLICATION_CODE = models.CharField(max_length=100,null=True,blank=True)

    history = HistoricalRecords()


class NutrientSource(models.Model):
    NUTR_SOURCE_C = models.AutoField(null=False, blank=False, primary_key=True)
    SOURCE_DESC = models.CharField(max_length=500,null=True,blank=True)
    SOURCE_DESC_F = models.CharField(max_length=500,null=True,blank=True)
    NRD_REF = models.IntegerField(null=True, blank=True)
    PUBLICATION_CODE = models.CharField(max_length=500,null=True,blank=True)


class NutrientReference(models.Model):
    REF_C = models.AutoField(null=False, blank=False, primary_key=True)
    REF_DESC = models.CharField(max_length=500,null=True,blank=True)
    REF_DESC_F = models.CharField(max_length=500,null=True,blank=True)


class NutrientOfFood(models.Model):
    NUTR_AMOUNT_C = models.AutoField(null=False, blank=False, primary_key=True)
    FOOD = models.ForeignKey(Food, on_delete=models.CASCADE, null=True, blank=True)
    NUTR = models.ForeignKey(Nutrient, on_delete=models.CASCADE, null=True, blank=True)
    SOURCE = models.ForeignKey(NutrientSource, on_delete=models.CASCADE, null=True, blank=True)
    REF = models.ForeignKey(NutrientReference, on_delete=models.CASCADE, null=True, blank=True)

    NUTR_VALUE = models.FloatField(null=True, blank=True)
    STD_ERROR = models.FloatField(null=True, blank=True)
    NUM_OBSER = models.IntegerField(null=True, blank=True)

    METHOD_C = models.IntegerField(null=True, blank=True) #Should this be a foreign key?

    COMMENT_T = models.CharField(max_length=500,null=True,blank=True)
    FLAG_TRACE = models.BooleanField(null=True,blank=True)
    PUBLICATION_CODE = models.CharField(max_length=500,null=True,blank=True)
    USDA_SOURCE = models.IntegerField(null=True, blank=True)
    USDA_DERIV = models.IntegerField(null=True, blank=True)
    FN_SYS_USER_CREATE_C = models.IntegerField(null=True, blank=True)
    FN_SYS_USER_EDIT_C = models.IntegerField(null=True, blank=True)

    # Dates
    DATE_ENTRY = models.DateTimeField(null=True, blank=True)
    DATE_CHANGE = models.DateTimeField(null=True, blank=True)
    DATE_END = models.DateTimeField(null=True, blank=True)
    PENTAHO_CREATE_DATE = models.DateTimeField(null=True, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.NUTR_AMOUNT_C}: {self.NUTR.NUTR_NAME}'


class MeasureType(models.Model):
    M_TYPE_ID = models.AutoField(null=False, blank=False, primary_key=True)
    M_TYPE_DESC = models.CharField(max_length=500,null=True,blank=True)
    M_TYPE_ABBRV = models.CharField(max_length=500,null=True,blank=True)
    M_TYPE_USER_SELECTABLE = models.BooleanField(null=True, blank=True)
    M_TYPE_DESC_F = models.CharField(max_length=500,null=True,blank=True)


class Measure(models.Model):
    MEASURE_ID = models.AutoField(null=False, blank=False, primary_key=True)
    MEASURE_DESC = models.CharField(max_length=500,null=True,blank=True)
    MEASURE_DESC_F = models.CharField(max_length=500,null=True,blank=True)
    MEASURE_ABBRV = models.CharField(max_length=500,null=True,blank=True)
    MEASURE_ABBRV_F = models.CharField(max_length=500,null=True,blank=True)
    M_TYPE = models.ForeignKey(MeasureType, on_delete=models.CASCADE, null=True, blank=True)
    MEASURE_OWNER = models.IntegerField(null=True, blank=True)
    SHARED_MEASURE = models.BooleanField(null=True, blank=True)
    PUBLICATION_CODE = models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return f'{self.MEASURE_DESC}'

class ConversionFactor(models.Model):
    CF_FACTOR_C = models.AutoField(null=False, blank=False, primary_key=True)
    FOOD_C = models.ForeignKey(Food, on_delete=models.CASCADE, null=True, blank=True)
    MEASURE_ID = models.ForeignKey(Measure, on_delete=models.CASCADE, null=True, blank=True)

    CONV_FACTOR = models.FloatField(null=True,blank=True)

    COMMENT_T = models.CharField(max_length=500,null=True,blank=True)
    CF_COMMENT_F = models.CharField(max_length=500,null=True,blank=True)

    FLAG_CFG = models.BooleanField(null=True, blank=True)
    NO_SERVING = models.IntegerField(null=True, blank=True)
    VALID_NULL_CF = models.IntegerField(null=True, blank=True)

    CF_REF_ID  = models.IntegerField(null=True, blank=True)
    PUBLICATION_CODE = models.CharField(max_length=25,null=True,blank=True)
    SEQ_WEB  = models.IntegerField(null=True, blank=True)
    FLAG_REFERENCE_AMOUNT  = models.BooleanField(null=True, blank=True)
    SHOW_SERVING_SIZE  = models.BooleanField(null=True, blank=True)
    CF_OWNER  = models.IntegerField(null=True, blank=True)
    SHARED_CF  = models.BooleanField(null=True, blank=True)
    FLAG_REPORT = models.BooleanField(null=True, blank=True)
    FN_SYS_USER_CREATE_C  = models.IntegerField(null=True, blank=True)
    FN_SYS_USER_EDIT_C  = models.IntegerField(null=True, blank=True)
    PUBLICATION_FLAG = models.BooleanField(null=True, blank=True)

    DATE_ENTRY = models.DateTimeField(null=True, blank=True)
    DATE_END = models.DateTimeField(null=True, blank=True)


    history = HistoricalRecords()

    def __str__(self):
        return f'{self.CF_FACTOR_C}: {self.MEASURE_DESC}'

