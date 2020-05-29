from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView

from cnf_xplor.api.serializers import FoodSerializer, NutrientSerializer, ConversionFactorSerializer, NutrientOfFoodSerializer
from cnf_xplor.api.models import Food, NutrientOfFood, Nutrient, ConversionFactor
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import re
import json


# Create your views here.

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


def single_search_term(word, name_search):

    # splitting up into chunks that must be found
    # entirety of a quote block
    # each word for everything outside of a quote block
    # AND logic
    for w in split_with_quotes(word):
        # Either the start or a non-alpha, then the term, then either the end or a non-alpha
        #w = w.lower()
        #regex_use = r'(^|[^A-Za-z]{1})%s($|[^A-Za-z]{1})' % (w)
        #if not bool(re.search(regex_use, name_search)):
        #    return False
        if not w in name_search:
            return False
    return True

# assert single_search_term('beef', 'Mixed dishes, beef pot roast, with browned potatoes, peas and corn')
# assert not single_search_term('apple', 'Mixed dishes, beef pot roast, with browned potatoes, peas and corn')

def advanced_search(x, word = None, group_c = None, language="English"):
    # Don't include any recepies
    if x.FN_RECIPE_FLG:
        return False
    name_search_dict = {"English":"FOOD_DESC", "French": "FOOD_DESC_F"}
    name_search = getattr(x, name_search_dict[language])
    if name_search is None:
        return False
    name_search = name_search.lower()
    word = word.lower()

    # If we are filtering by a word
    if word is not None:
        or_strings, not_strings = find_not_or(word)
        # First do the NOTs
        for substring in not_strings:
            # If you find any NOT, this is not something we want
            if single_search_term(substring, name_search):
                return False

        # Then test the ORs
        # If you find any one of the ORs, keep it
        found = False
        for substring in or_strings:
            #if "Congee" in x.FOOD_DESC:
            #    print(x.FN_RECIPE_FLG)
            #    print(x.FOOD_DESC)
            #    print(or_strings)
            #    print(not_strings)
            #    print(substring, name_search)
            if single_search_term(substring, name_search):
                found = True

        # If you find none of the ORs, this is not something we want
        if not found:
            return False


    # If we are filtering on group code
    if group_c is not None:
        # If a group code has been provided
        if is_int(group_c):
            group_c = int(group_c)
            if x.GROUP.GROUP_C != group_c:
                return False
        # Otherwise, do a search
        else:
            if (language == "English"):
                print(group_c.lower(), x.GROUP.GROUP_DESC.lower())
                if (group_c.lower() not in x.GROUP.GROUP_DESC.lower()):
                    return False
                else:
                    return True
            if (language == "French"):
                if (group_c.lower() not in x.GROUP.GROUP_DESC_F.lower()):
                    return False
                else:
                    return True

    return True


def is_int(x):
    try:
        x = int(x)
        return True
    except:
        return False


def get_within_quotes(s):

    switch = False
    start_quote = -1
    end_quote = -1
    start_nonquote = 0 #We start in a quote block, unless the first character is a non-quote
    end_nonquote = -1
    quote_blocks = []
    nonquote_blocks = []
    # If there are no quotes
    if '"' not in s:
        nonquote_blocks.append((0, len(s)))
        return quote_blocks, nonquote_blocks
    for i in range(len(s)):
        # Change of state
        if (s[i] == '"'):
            if not switch: #Start of a new quote block
                switch = True
                start_quote = i+1
                if i != 0:
                    # Finish off the non-quote block that goes up to this point
                    end_nonquote = i-1
                    assert (start_nonquote != -1) & (end_nonquote != -1)
                    nonquote_blocks.append((start_nonquote, end_nonquote))
                start_nonquote = -1
            else:
                switch = False
                end_quote = i
                # Record the start and end of the quote block
                quote_blocks.append((start_quote, end_quote))

                # Initialize a new nonquote block
                start_nonquote = i+1

    assert not ((start_quote != -1) & (end_quote == -1)), "Odd number of quotes"
    return quote_blocks, nonquote_blocks


def split_with_quotes(s):
    all_chunks = []
    quote_blocks, nonquote_blocks = get_within_quotes(s)
    # Quote blocks need to remain together
    for q in quote_blocks:
        chunk_current = s[q[0]:q[1]]
        chunk_current = chunk_current.lstrip(" ").rstrip(" ")
        all_chunks.append(chunk_current)
    # Non-quote nonquote_blocks need to be split up by " "
    for q in nonquote_blocks:
        chunk_current = s[q[0]:q[1]]
        chunk_current = chunk_current.lstrip(" ").rstrip(" ")
        for w in chunk_current.split(" "):
            all_chunks.append(w)
    return all_chunks

# split_with_quotes('"hello bye" but not "bye bye"') == ['hello bye', 'bye bye', 'but', 'not']


def find_not_or(s):
    #blocks = [m.start() for m in re.finditer('(\[NOT\]|\[OR\])', s)]
    blocks = [m.start() for m in re.finditer('(NOT|OR)', s)]
    # The start and end of s
    blocks.insert(0, 0)
    blocks.append(len(s))
    or_strings = []
    not_strings = []
    for i in range(len(blocks) - 1):
        s_sub = s[blocks[i]:blocks[i+1]]
        s_sub = s_sub.rstrip(" ")
        if i == 0:
            # The first block is an OR string
            or_strings.append(s_sub)
        else:
            assert ("NOT " in s_sub) | ("OR " in s_sub), "Can't find NOT/OR in your s_sub {}".format(s_sub)
            if 'NOT ' in s_sub:
                not_strings.append(s_sub.replace('NOT ',''))
            else:
                or_strings.append(s_sub.replace('OR ',''))
    return or_strings, not_strings

# find_not_or('hello [NOT] bye [OR] hi [NOT] buh-bye') == (['hello', 'hi'], ['bye', 'buh-bye'])


def is_int(x):
    try:
        x = int(x)
        return True
    except:
        return False


class FoodDataTables(ModelViewSet):
    serializer_class = FoodSerializer
    lookup_field = 'FOOD_C'
    def get_queryset(self):
        queryset = Food.objects.select_related('GROUP').all()

        # Here we need to build the advanced search
        word = self.request.query_params.get('name', None)
        group_code = self.request.query_params.get('group_c', None)
        language = self.request.query_params.get('language', None)
        if is_int(word):
            word = int(word)
            queryset = Food.objects.filter(FOOD_C__in=[word])
            return queryset
        # If word appears to be just a food code, then pull that up

        # If we have nothing to search by, we are done
        if (word is None) & (group_code is None):
            return queryset
        # This list comphrehension gives you a list, not a queryset
        # It will work normally, but not for datatables format
        # Instead we are going to use a hacky way to convert it back to a queryset
        queryset_ids = [x.FOOD_C for x in queryset if advanced_search(x, word, group_code, language)]
        queryset = Food.objects.filter(FOOD_C__in=queryset_ids)
        return queryset


class NutrientDataTables(ModelViewSet):
    serializer_class = NutrientOfFoodSerializer
    def get_queryset(self):
        # We need to search with a food code
        food_c = self.request.query_params.get('food_c', None)
        # if we don't have a valid food code, return nada
        if not is_int(food_c):
            food_c = -1
        queryset = NutrientOfFood.objects.select_related('NUTR').all()
        queryset = queryset.filter(FOOD_id__exact=food_c)
        return queryset


class NutrientUpdate(GenericAPIView):
    queryset = NutrientOfFood.objects.all()
    serializer_class = NutrientOfFoodSerializer
    def put(self, request, *args, **kwargs):
        # This more or less just copies the code from UpdateModelMixin
        # But allows us to add a changeReason to the instance
        instance = self.get_object()
        # Need the old value to run some triggers
        old_val = instance.NUTR_VALUE
        data = json.loads(list(request.data.keys())[0])
        #TODO: Where do we get this from
        instance.changeReason=""

        # All of the linked models should not be editable
        # And that currently seems to be the case
        changed = False
        for key in data:
            if key in ['NUTR','NUTR_TAGNAME']: #The default keys that are present when something does not change
                continue
            changed = True
        if not changed:
            return Response({"changed": False})
        # Data that has been removed to an empty string should come in as nothing
        for key in data:
            if data[key] == "":
                data[key] = None

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid()
        # If there is an error, see it here
        serializer.save()
        # Run triggers
        process_change(instance, old_val)
        return Response({"data": [serializer.data], "changed": True}) # Required format for datatables editor


class ConversionFactorUpdate(GenericAPIView):
    queryset = ConversionFactor.objects.all()
    serializer_class = ConversionFactorSerializer
    def put(self, request, *args, **kwargs):
        # This more or less just copies the code from UpdateModelMixin
        # But allows us to add a changeReason to the instance
        instance = self.get_object()
        # instance.changeReason = request.data["REASON"]
        data = json.loads(list(request.data.keys())[0])

        if data == {'FLAG_CFG': 'false'}:
            return Response({"changed": False})

        serializer = self.get_serializer(instance, data=data, partial=False)
        serializer.is_valid(raise_exception=True)
        # If there is an error, see it here
        serializer.save()

        #return Response(serializer.data)
        return Response({"data": [serializer.data], "changed": True}) # Required format for datatables editor



def process_change(n_of_food, old_val):
    """
    does the nutrient change activate any of our triggers
    :param n_of_food:
    :param old_val:
    :return:
    """
    # Kcal <-> KJoul
    amino_acids = ['TRP', 'THR', 'ISO', 'LEU', 'LYS', 'MET', 'CYS', 'PHE', 'TYR', 'VAL', 'ARG', 'HIS', 'ALA',
                   'ASP', 'GLU', 'GLY', 'PRO', 'SER', 'HYP']
    fats = ['CHOL', 'TSAT', 'MUFA', 'PUFA', 'TRFA', 'TRMO', 'TRPO', '4:0', '6:0', '8:0', '10:0', '12:0',
            '14:00', '16:0', '18:0', '15:0', '17:0', '20:0', '22:0', '24:0', '14:1', '15:1', '16:1undiff',
            '16:1c', '16:1t', '17:1', '18:1undiff', '18:1c', '18:1t', '20:1', '22:1undiff', '22:1c', '22:1t',
            '24:1c', '18:2undiff', '18:2ccn-6', '18:2tt', '18:2i', '18:2cla', '18:3undiff', '18:3cccn-3',
            '18:3cccn-6', '18:3i', '18:4', '20:2cc', '20:3undiff', '20:3n-3', '20:3n-6', '20:4undiff',
            '20:4n-6', '20:5n-3EPA', '21:5', '22:2', '22:3', '22:4n-6', '22:5n-3DPA', '22:6n-3DHA', 'TPST',
            'STIG', 'CAMSTR', 'SITSTR']
    sugars = ['TSUG', 'TMOS', 'TDIS', 'GLUC', 'FRUC', 'GAL', 'SUCR', 'LACT', 'MALT', 'RAFF', 'STAC', 'MANN',
              'SORB', 'TDF', 'NDF', 'PEC', 'STAR']

    if n_of_food.NUTR.NUTR_SYMBOL == "KCAL":
        update_database_nutrient(n_of_food, "KJ", int(round(n_of_food.NUTR_VALUE * 4.182,0)))
    if n_of_food.NUTR.NUTR_SYMBOL == "KJ":
        update_database_nutrient(n_of_food, "KCAL", int(round(n_of_food.NUTR_VALUE / 4.182)))
    if n_of_food.NUTR.NUTR_SYMBOL == "PROT":
        if n_of_food.NUTR_VALUE == 0: # If we are setting this to zero.
            f = get_food_from_nutr(n_of_food)
            set_group(f, amino_acids, 0)

        if (old_val == 0) & (n_of_food.NUTR_VALUE != 0): # If we are setting this away from zero
            f = get_food_from_nutr(n_of_food)
            set_group(f, amino_acids, None)
    if n_of_food.NUTR.NUTR_SYMBOL == "FAT":
        if n_of_food.NUTR_VALUE == 0: # If we are setting this to zero.
            f = get_food_from_nutr(n_of_food)
            set_group(f, fats, 0)
        if (old_val == 0) & (n_of_food.NUTR_VALUE != 0): # If we are setting this away from zero
            f = get_food_from_nutr(n_of_food)
            set_group(f, fats, None)

    if n_of_food.NUTR.NUTR_SYMBOL == "CARB":
        if n_of_food.NUTR_VALUE == 0: # If we are setting this to zero.
            f = get_food_from_nutr(n_of_food)
            set_group(f, sugars, 0)

        if (old_val == 0) & (n_of_food.NUTR_VALUE != 0): # If we are setting this away from zero
            f = get_food_from_nutr(n_of_food)
            set_group(f, sugars, None)

    # Niacin update
    if n_of_food.NUTR.NUTR_SYMBOL == "N-MG":
        # get protein factor
        f = get_food_from_nutr(n_of_food)
        trp = get_nof(f, "TRP")
        if trp.NUTR_VALUE is not None:
            if trp.NUTR_VALUE > 0:
                protein_factor = trp.NUTR_VALUE
            else:
                prot = get_nof(f, "PROT")
                protein_factor = prot.NUTR_VALUE * 0.011
        else:
            prot = get_nof(f, "PROT")
            if prot.NUTR_VALUE is not None:
                protein_factor = prot.NUTR_VALUE * 0.011
            else:
                protein_factor = None

        nmg_val = n_of_food.NUTR_VALUE
        # Update N-NE
        ne = get_nof(f, "N-NE")
        if protein_factor is not None:
            ne.NUTR_VALUE = protein_factor * 1000 / 60 + nmg_val
            ne.save(update_fields=["NUTR_VALUE"])


def set_group(f, list_of_nutrients, val):
    """
    Sets all nutrients attached to a given Food to val
    :param f:
    :param list_of_nutrients:
    :param val:
    :return:
    """
    for nutr_symbol in list_of_nutrients:
        n = get_nof(f, nutr_symbol)
        if n is None:
            print("Problem with {}".format(nutr_symbol))
            continue
        n.NUTR_VALUE = val
        n.save(update_fields=["NUTR_VALUE"])


def update_database_nutrient(n_of_food, nutrient_symbol, new_val):
    """
    Updates a given nutrient of food to a new value
    :param n_of_food:
    :param nutrient_symbol:
    :param new_val:
    :return:
    """

    # Get the food of this NutrientOfFood
    f = get_food_from_nutr(n_of_food)

    # Get the other NutrientOfFood Associated with the current food
    n = get_nof(f, nutrient_symbol)

    # Change the value and update it
    n.NUTR_VALUE = new_val
    n.save(update_fields=["NUTR_VALUE"])


def get_food_from_nutr(n_of_food):
    """
    Gets the food from a NutrientOfFood object
    :param n_of_food:
    :return:
    """
    return Food.objects.get(pk=n_of_food.FOOD_id)


def get_nof(f, nutrient_symbol):
    """
    Gets the NutrientOfFood from a given food and a nutrient value
    :param f:
    :param nutrient_symbol:
    :return:
    """

    # Find the master nutrient we want to change
    n_search = Nutrient.objects.filter(NUTR_SYMBOL=nutrient_symbol)
    assert len(n_search) <= 1
    if len(n_search) == 0: #If we don't have this in the database
        return None
    n = n_search[0]

    # Find the nutrient of food we want to change
    nof_search = NutrientOfFood.objects.filter(FOOD=f, NUTR=n)
    assert len(nof_search) <= 1
    if len(nof_search) == 0:
        return None
    return nof_search[0]


class ConversionFactorDataTables(ModelViewSet):
    serializer_class = ConversionFactorSerializer
    def get_queryset(self):
        # We need to search with a food code
        food_c = self.request.query_params.get('food_c', None)
        # if we don't have a valid food code, return nada
        if not is_int(food_c):
            food_c = -1
        queryset = ConversionFactor.objects.filter(FOOD_C__exact=food_c)
        return queryset

