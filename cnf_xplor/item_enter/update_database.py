
from cnf_xplor.api.models import Food, Nutrient, NutrientOfFood
import tqdm


def add_all_nutrients():
    for n in Nutrient.objects.all():
        add_nutrient_to_all_foods(n)


def add_nutrient_to_all_foods(n):
    # Loop through all foods
    for f in tqdm.tqdm(Food.objects.all(), desc="adding food for {}".format(n.NUTR_NAME)):
        add_nutrient_to_food(f, n)


def add_all_nutrients_to_food(f):
    for n in Nutrient.objects.all():
        add_nutrient_to_food(f, n)


def add_nutrient_to_food(f, n):
    qs = NutrientOfFood.objects.select_related('FOOD').select_related('NUTR').all()
    qs = qs.filter(NUTR=n, FOOD=f)
    # If this food does not have this nutrient
    if qs.count() == 0:
        # Add it
        NutrientOfFood.objects.create(
            FOOD=f,
            NUTR=n,
            NUTR_VALUE=None,
            STD_ERROR=None,
            NUM_OBSER=None,
        )
