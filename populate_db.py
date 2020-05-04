

def enter_foodgroup():
    import tqdm
    import psycopg2
    import pandas as pd
    from cnf_xplor.api.models import FoodGroup

    def fix_french_accents(df, key):
        df[key] = [x.encode('utf-8').decode('utf-8') if x is not None else x for x in df[key].values]
        return df
    def reformat_bool(s):
        if s is None:
            return None
        if (s == 1) | (s == "1"):
            return True
        if (s == 0) | (s == "0"):
            return False
        if s == "Y":
            return True
        if s == "N":
            return False
        assert False, "problem with boolean {}".format(s)

    df_foodgroup = pd.read_csv('UpdatedCNFData/CNFADM_FOOD_GROUP.csv', sep='\t', encoding='utf-16')
    df_foodgroup = df_foodgroup.where((pd.notnull(df_foodgroup)), None)

    df_foodgroup = fix_french_accents(df_foodgroup,"GROUP_DESC_F")
    # 2 and 1 instead of 1 and 0. Needs to be changed
    df_foodgroup["FG_DB_SOURCE_C"] = df_foodgroup["FG_DB_SOURCE_C"].values-1

    for (i, dat) in tqdm.tqdm(df_foodgroup.iterrows(), total=df_foodgroup.shape[0], desc="foodgroup"):
        if dat["GROUP_C"] is None:
            continue
        FoodGroup.objects.get_or_create(
            GROUP_C = dat["GROUP_C"],
            GROUP_DESC = dat["GROUP_DESC"],
            GROUP_DESC_F = dat["GROUP_DESC_F"],
            GROUP_CODE=dat["GROUP_CODE"],
            FG_GROUP_ABBRV=dat["FG_GROUP_ABBRV"],
            GROUP_COMPOSITE_FLG=reformat_bool(dat["GROUP_COMPOSITE_FLG"]),
            GROUP_RECIPE_FLG=reformat_bool(dat["GROUP_RECIPE_FLG"]),
            FG_DB_SOURCE_C=reformat_bool(dat["FG_DB_SOURCE_C"]),
            FG_BBCA_INDEX=dat["FG_BBCA_INDEX"],
            GROUP_OWNER=dat["GROUP_OWNER"],
            SHARED_GROUP=dat["SHARED_GROUP"],
        )

    conn = psycopg2.connect(user = "averster",
                                  password = "Boat1234",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "cnf_xplor")
    cur = conn.cursor()
    cur.execute(" SELECT setval('\"api_foodgroup_GROUP_C_seq\"',(SELECT max(\"GROUP_C\") + 1 FROM api_foodgroup));")


def enter_source():
    import psycopg2
    import tqdm
    import pandas as pd
    from cnf_xplor.api.models import FoodSource

    def fix_french_accents(df, key):
        df[key] = [x.encode('utf-8').decode('utf-8') if x is not None else x for x in df[key].values]
        return df
    def reformat_bool(s):
        if s is None:
            return None
        if (s == 1) | (s == "1"):
            return True
        if (s == 0) | (s == "0"):
            return False
        if s == "Y":
            return True
        if s == "N":
            return False
        assert False, "problem with boolean {}".format(s)

    df_foodsource = pd.read_csv('UpdatedCNFData/CNFADM_FOOD_SOURCE.csv', sep = '\t', encoding='utf-16')
    df_foodsource = df_foodsource.where((pd.notnull(df_foodsource)), None)

    df_foodsource = fix_french_accents(df_foodsource,"SOURCE_DESC_F")

    for (i, dat) in tqdm.tqdm(df_foodsource.iterrows(), total=df_foodsource.shape[0], desc="foodsource"):
        if dat["SOURCE_C"] is None:
            continue
        FoodSource.objects.get_or_create(
            SOURCE_C = dat["SOURCE_C"],
            SOURCE_DESC = dat["SOURCE_DESC"],
            SOURCE_DESC_F = dat["SOURCE_DESC_F"],
            NRD_REF = dat["NRD_REF"],
            SHARED_SOURCE = reformat_bool(dat["SHARED_SOURCE"]),
            SOURCE_OWNER = dat["SOURCE_OWNER"],
            SOURCE_CNF_OWNER = dat["SOURCE_CNF_OWNER"]
        )
    conn = psycopg2.connect(user = "averster",
                                  password = "Boat1234",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "cnf_xplor")
    cur = conn.cursor()
    cur.execute(" SELECT setval('\"api_foodsource_SOURCE_C_seq\"',(SELECT max(\"SOURCE_C\") + 1 FROM api_foodsource));")



def enter_food():
    import psycopg2
    import pandas as pd
    import tqdm
    from cnf_xplor.api.models import Food, FoodSource, FoodGroup

    def fix_french_accents(df, key):
        df[key] = [x.encode('utf-8').decode('utf-8') if x is not None else x for x in df[key].values]
        return df
    def is_number(s):
        try:
            int(s)
            return True
        except (ValueError,TypeError) as e:
            return False

    def reformat_datetime(s):
        from datetime import datetime
        if s is None:
            return None
        try:
            #d = datetime.strptime(s, '%d/%m/%Y %H:%M:%S')
            d = datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
            return d.strftime('%Y-%m-%d %H:%M:%S')
        except:
            #d = datetime.strptime(s, '%d/%m/%Y')
            d = datetime.strptime(s, '%Y-%m-%d')
            return d.strftime('%Y-%m-%d')
    def reformat_bool(s):
        if s is None:
            return None
        if (s == 1) | (s == "1"):
            return True
        if (s == 0) | (s == "0"):
            return False
        if s == "Y":
            return True
        if s == "N":
            return False
        assert False, "problem with boolean {}".format(s)


    # Load data
    df_food = pd.read_csv('UpdatedCNFData/CNFADM_FOOD_NAME.csv', sep='\t', encoding='utf-16')

    # Merge, then populate the database
    df_food = df_food.where((pd.notnull(df_food)), None)

    # Fix the french accents
    df_food = fix_french_accents(df_food,"FR_NAME")
    df_food = fix_french_accents(df_food,"FOOD_DESC_F")

    # Loop through, make a database entry for each row
    for (i,dat) in tqdm.tqdm(df_food.iterrows(), total=df_food.shape[0], desc = "food"):
        if pd.isnull(dat["GROUP_C"]):
            dat["GROUP_C"] = None
        if dat["FOOD_C"] is None:
            print(dat)
            continue
        if not is_number(dat["FOOD_C"]):
            print(dat)
            continue

        try:
            g = FoodGroup.objects.get(pk=int(dat["GROUP_C"]))
        except:
            g = None

        try:
            s = FoodSource.objects.get(pk=int(dat["SOURCE_C"]))
        except:
            s = None

        #try:
        # This will work if there is no item, or if we have done no database migrations
        #print(dat)
        Food.objects.get_or_create(
            FOOD_C = dat["FOOD_C"],
            ENG_NAME=dat["ENG_NAME"],
            FR_NAME=dat["FR_NAME"],
            FOOD_DESC=dat["FOOD_DESC"],
            FOOD_DESC_F=dat["FOOD_DESC_F"],
            NUT_CAN_C=dat["NUT_CAN_C"],
            CNF_FLAG=reformat_bool(dat["CNF_FLAG"]),

            SOURCE = s,
            COUNTRY_C = dat["COUNTRY_C"],
            GROUP = g,
            COMMENT_T = dat["COMMENT_T"],
            FN_COMMENT_F = dat["FN_COMMENT_F"],

            FOOD_REFERENCE=dat["FOOD_REFERENCE"],
            SCIENTIFIC_NAME=dat["SCIENTIFIC_NAME"],
            PUBLICATION_FLAG=reformat_bool(dat["PUBLICATION_FLAG"]),
            PUBLICATION_CODE=dat["PUBLICATION_CODE"],
            ITEM_C=dat["ITEM_C"],
            SEQUENCE_C=dat["SEQUENCE_C"],
            LEGACY_GROUP_C=dat["LEGACY_GROUP_C"],

            COMMON_NM_E=dat["COMMON_NM_E"],
            COMMON_NM_F=dat["COMMON_NM_F"],
            FN_DB_SOURCE_C=dat["FN_DB_SOURCE_C"],
            FN_RECIPE_FLG=reformat_bool(dat["FN_RECIPE_FLG"]),
            FN_SYSTEM_VIEW_C=dat["FN_SYSTEM_VIEW_C"],
            FN_FAT_CHANGE=dat["FN_FAT_CHANGE"],
            FN_MOISTURE_CHANGE=dat["FN_MOISTURE_CHANGE"],
            FN_SYS_USER_CREATE_C=dat["FN_SYS_USER_CREATE_C"],
            FN_SYS_USER_EDIT_C=dat["FN_SYS_USER_EDIT_C"],
            FN_TEMPLATE_C=dat["FN_TEMPLATE_C"],
            FN_TEMP=dat["FN_TEMP"],
            FN_ARCHIVED=dat["FN_ARCHIVED"],
            FN_LEGACY_C=dat["FN_LEGACY_C"],
            US_RECIPE_C=dat["US_RECIPE_C"],
            USDA_MODIFIED=reformat_bool(dat["USDA_MODIFIED"]),
            USDA_TEMP=dat["USDA_TEMP"],
            CANADA_FOOD_SUBGROUP_ID=dat["CANADA_FOOD_SUBGROUP_ID"],
            CFGHE_FLAG=dat["CFGHE_FLAG"],
            ORIG_CANADA_FOOD_SUBGROUP_ID=dat["ORIG_CANADA_FOOD_SUBGROUP_ID"],
            FOOD_OWNER=dat["FOOD_OWNER"],
            SHARED_FOOD=reformat_bool(dat["SHARED_FOOD"]),
            CANDI_REC_NUM=dat["CANDI_REC_NUM"],
            INHERITANCE_FLAG=reformat_bool(dat["INHERITANCE_FLAG"]),
            FOOD_CODE=dat["FOOD_CODE"],

            DATE_ENTRY = reformat_datetime(dat["DATE_ENTRY"]),
            DATE_CHANGE = reformat_datetime(dat["DATE_CHANGE"]),
            DATE_END = reformat_datetime(dat["DATE_END"])
        )
        #except:
        #    f = Food.objects.get(dat["FOOD_C"])
        #    f.SOURCE_C = dat["SOURCE_C"],
        #    f.COUNTRY_C = dat["COUNTRY_C"],
        #    f.GROUP = g,
#
#            f.ENG_NAME = dat["ENG_NAME"],
#            f.FR_NAME = dat["FR_NAME"],
#            f.FOOD_DESC = dat["FOOD_DESC"],
#            f.FOOD_DESC_F = dat["FOOD_DESC_F"],
#            f.COMMENT_T = dat["COMMENT_T"],
#            f.FN_COMMENT_F = dat["FN_COMMENT_F"],
#
#            f.DATE_ENTRY = reformat_datetime(dat["DATE_ENTRY"]),
#            f.DATE_CHANGE = reformat_datetime(dat["DATE_CHANGE"]),
#            r.DATE_END = reformat_datetime(dat["DATE_END"])
#            f.save()

    #Finally, deal with the sequence
    #SELECT setval('"viewfood_food_FOOD_C_seq"',(SELECT max("FOOD_C") + 1 FROM viewfood_food));

    conn = psycopg2.connect(user = "averster",
                                  password = "Boat1234",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "cnf_xplor")
    cur = conn.cursor()
    cur.execute(" SELECT setval('\"api_food_FOOD_C_seq\"',(SELECT max(\"FOOD_C\") + 1 FROM api_food));")


def enter_conversion_factors():
    import pandas as pd
    import tqdm
    from cnf_xplor.api.models import ConversionFactor, Measure, Food, MeasureType
    import psycopg2

    def fix_french_accents(df, key):
        df[key] = [x.encode('utf-8').decode('utf-8') if x is not None else x for x in df[key].values]
        return df
    def reformat_datetime(s):
        from datetime import datetime
        if s is None:
            return None
        try:
            d = datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
            return d.strftime('%Y-%m-%d %H:%M:%S')
        except:
            try:
                d = datetime.strptime(s, '%Y-%m-%d %H:%M')
                return d.strftime('%Y-%m-%d %H:%M')
            except:
                d = datetime.strptime(s, '%Y-%m-%d')
                return d.strftime('%Y-%m-%d')

    def reformat_bool(s):
        if s is None:
            return None
        if (s == 1) | (s == "1"):
            return True
        if (s == 0) | (s == "0"):
            return False
        if s == "Y":
            return True
        if s == "N":
            return False
        assert False, "problem with boolean {}".format(s)

    def convert_to_int(s):
        if s is None:
            return s
        return int(s)

    infile = "UpdatedCNFData/CNFADM_CONV_FACTOR.csv"
    df_convfactor = pd.read_csv(infile, sep = "\t", encoding="utf-16")
    df_convfactor = df_convfactor.where((pd.notnull(df_convfactor)), None)

    infile = "UpdatedCNFData/CNFADM_MEASURE.csv"
    df_measure = pd.read_csv(infile, sep = "\t", encoding="utf-16")
    df_measure = df_measure.where((pd.notnull(df_measure)), None)

    infile = "UpdatedCNFData/CNFADM_MEASURE_TYPE.csv"
    df_measuretype = pd.read_csv(infile, sep = "\t", encoding="utf-16")
    df_measuretype = df_measuretype.where((pd.notnull(df_measuretype)), None)

    # Merge, then add to the database
    #df_full = df_convfactor.merge(df_measure, on = "MEASURE_ID", how = "left")
    #df_full = df_full.where((pd.notnull(df_full)), None)

    # fix encoding on this one
    #df_full = fix_french_accents(df_full,"MEASURE_DESC")
    #df_full = fix_french_accents(df_full,"MEASURE_DESC_F")
    #df_full = fix_french_accents(df_full,"MEASURE_ABBRV")
    #df_full = fix_french_accents(df_full,"MEASURE_ABBRV_F")
    for (i,dat) in tqdm.tqdm(df_measuretype.iterrows(), total=df_measuretype.shape[0], desc="measuretype"):
        MeasureType.objects.get_or_create(
            M_TYPE_ID=dat["M_TYPE_ID"],
            M_TYPE_DESC=dat["M_TYPE_DESC"],
            M_TYPE_ABBRV=dat["M_TYPE_ABBRV"],
            M_TYPE_USER_SELECTABLE=reformat_bool(dat["M_TYPE_USER_SELECTABLE"]),
            M_TYPE_DESC_F=dat["M_TYPE_DESC_F"]
        )

    for (i,dat) in tqdm.tqdm(df_measure.iterrows(), total=df_measure.shape[0], desc="measure"):
        try:
            t = MeasureType.objects.get(pk=int(dat["M_TYPE_ID"]))
        except:
            print("Can't find a measure type for {}".format(dat["M_TYPE_ID"]))
            t = None


        Measure.objects.get_or_create(
            MEASURE_ID=dat["MEASURE_ID"],
            MEASURE_DESC=dat["MEASURE_DESC"],
            MEASURE_DESC_F=dat["MEASURE_DESC_F"],
            MEASURE_ABBRV=dat["MEASURE_ABBRV"],
            MEASURE_ABBRV_F=dat["MEASURE_ABBRV_F"],
            M_TYPE=t,
            MEASURE_OWNER=dat["MEASURE_OWNER"],
            SHARED_MEASURE=reformat_bool(dat["SHARED_MEASURE"]),
            PUBLICATION_CODE=dat["PUBLICATION_CODE"]

        )


    for (i,dat) in tqdm.tqdm(df_convfactor.iterrows(), total=df_convfactor.shape[0], desc="convertionfactor"):
        try:
            f = Food.objects.get(pk=int(dat["FOOD_C"]))
        except:
            print("Can't find a food for {}".format(dat["FOOD_C"]))
            f = None
        try:
            m = Measure.objects.get(pk=int(dat["MEASURE_ID"]))
        except:
            print("Can't find a measure for {}".format(dat["MEASURE_ID"]))
            m = None
        ConversionFactor.objects.get_or_create(
            CF_FACTOR_C = dat["CF_FACTOR_C"],
            FOOD_C = f,
            MEASURE_ID = m,

            CONV_FACTOR = dat["CONV_FACTOR"],
            COMMENT_T=dat["COMMENT_T"],
            CF_COMMENT_F=dat["CF_COMMENT_F"],

            FLAG_CFG=reformat_bool(dat["FLAG_CFG"]),
            NO_SERVING=dat["NO_SERVING"],
            VALID_NULL_CF=dat["VALID_NULL_CF"],

            CF_REF_ID=dat["CF_REF_ID"],
            PUBLICATION_CODE=dat["PUBLICATION_CODE"],
            SEQ_WEB=dat["SEQ_WEB"],
            FLAG_REFERENCE_AMOUNT=reformat_bool(dat["FLAG_REFERENCE_AMOUNT"]),
            SHOW_SERVING_SIZE=reformat_bool(dat["SHOW_SERVING_SIZE"]),
            CF_OWNER=dat["CF_OWNER"],
            SHARED_CF=reformat_bool(dat["SHARED_CF"]),
            FLAG_REPORT=reformat_bool(dat["FLAG_REPORT"]),
            FN_SYS_USER_CREATE_C=dat["FN_SYS_USER_CREATE_C"],
            FN_SYS_USER_EDIT_C=dat["FN_SYS_USER_EDIT_C"],
            PUBLICATION_FLAG=reformat_bool(dat["PUBLICATION_FLAG"]),

            DATE_ENTRY = reformat_datetime(dat["DATE_ENTRY"]),
            DATE_END = reformat_datetime(dat["DATE_END"]),

        )

    conn = psycopg2.connect(user = "averster",
                                  password = "Boat1234",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "cnf_xplor")
    cur = conn.cursor()
    cur.execute(" SELECT setval('\"api_conversionfactor_CF_FACTOR_C_seq\"',(SELECT max(\"CF_FACTOR_C\") + 1 FROM api_conversionfactor));")


def add_nutrients():
    import pandas as pd
    import tqdm
    from cnf_xplor.api.models import Nutrient, Food, NutrientOfFood, NutrientSource, NutrientReference
    import psycopg2

    def fix_french_accents(df, key):
        df[key] = [x.encode('utf-8').decode('utf-8') if x is not None else x for x in df[key].values]
        return df
    def convert_to_int(s):
        if s is None:
            return s
        return int(s)
    def reformat_bool(s):
        if s is None:
            return None
        if (s == 1) | (s == "1"):
            return True
        if (s == 0) | (s == "0"):
            return False
        if s == "Y":
            return True
        if s == "N":
            return False
        assert False, "problem with boolean {}".format(s)

    df_nutramount = pd.read_csv('UpdatedCNFData/CNFADM_NUTR_AMOUNT.csv', delimiter = "\t", encoding='utf-16')
    df_nutrname = pd.read_csv('UpdatedCNFData/CNFADM_NUTR_NAME.csv', delimiter = "\t", encoding='utf-16')
    df_nutrsource = pd.read_csv('UpdatedCNFData/CNFADM_NUTR_SOURCE.csv', delimiter = "\t", encoding='utf-16')
    df_nutrreference = pd.read_csv("UpdatedCNFData/CNFADM_REFERENCE.csv", delimiter = "\t", encoding='utf-16')
    df_nutramount = df_nutramount.where((pd.notnull(df_nutramount)), None)
    df_nutrname = df_nutrname.where((pd.notnull(df_nutrname)), None)
    df_nutrsource = df_nutrsource.where((pd.notnull(df_nutrsource)), None)
    df_nutrreference = df_nutrreference.where((pd.notnull(df_nutrreference)), None)

    # the NA in sodium comes out as None
    df_nutrname.loc[df_nutrname['NUTR_NAME'] == "SODIUM","NUTR_SYMBOL"] = "NA"
    #df_full = df_nutramount.merge(df_nutrname, on = "NUTR_C", how = "left")[["NUTR_AMOUNT_C", "FOOD_C", "NUTR_C", "NUTR_VALUE", "UNIT", "STD_ERROR", "NUM_OBSER", "NUTR_SYMBOL", "NUTR_NAME", "NUTR_NAME_F"]]
    #df_full = df_full.where((pd.notnull(df_full)), None)
    df_nutrname = fix_french_accents(df_nutrname,"NUTR_SYMBOL")
    df_nutrname = fix_french_accents(df_nutrname,"NUTR_NAME")
    df_nutrname = fix_french_accents(df_nutrname,"NUTR_NAME_F")

    for (i,dat) in tqdm.tqdm(df_nutrname.iterrows(), total=df_nutrname.shape[0], desc="nutrients"):
        Nutrient.objects.get_or_create(
            NUTR_C = convert_to_int(dat["NUTR_C"]),
            NUTR_SYMBOL = dat["NUTR_SYMBOL"].replace(" ","",-1),
            NUTR_NAME = dat["NUTR_NAME"],
            NUTR_NAME_F = dat["NUTR_NAME_F"],
            UNIT = dat["UNIT"],
            SEQUENCE_C = convert_to_int(dat["SEQUENCE_C"]),
            NUTR_CODE=dat["NUTR_CODE"],
            NUTR_WEB=reformat_bool(dat["NUTR_WEB"]),
            NUTR_ACTIVE_FLAG=reformat_bool(dat["NUTR_ACTIVE_FLAG"]),
            NUTR_DECIMAL_PLACE=dat["NUTR_DECIMAL_PLACE"],
            NUTR_WEB_ORDER=dat["NUTR_WEB_ORDER"],
            NUTRIENT_GROUP_ID=dat["NUTRIENT_GROUP_ID"],

            TAGNAME=dat["TAGNAME"],
            NUTR_WEB_NAME_E=dat["NUTR_WEB_NAME_E"],
            NUTR_WEB_NAME_F=dat["NUTR_WEB_NAME_F"],
            PUBLICATION_CODE=dat["PUBLICATION_CODE"]
        )

    for (i,dat) in tqdm.tqdm(df_nutrsource.iterrows(), total=df_nutrsource.shape[0], desc="nutrientsource"):
        NutrientSource.objects.get_or_create(
            NUTR_SOURCE_C = convert_to_int(dat["NUTR_SOURCE_C"]),
            SOURCE_DESC=dat["SOURCE_DESC"],
            SOURCE_DESC_F=dat["SOURCE_DESC_F"],
            NRD_REF=dat["NRD_REF"],
            PUBLICATION_CODE=dat["PUBLICATION_CODE"]
        )

    for (i,dat) in tqdm.tqdm(df_nutrreference.iterrows(), total=df_nutrreference.shape[0], desc="nutrientreference"):
        NutrientReference.objects.get_or_create(
            REF_C= convert_to_int(dat["REF_C"]),
            REF_DESC=dat["REF_DESC"],
            REF_DESC_F=dat["REF_DESC_F"]
        )

    for (i,dat) in tqdm.tqdm(df_nutramount.iterrows(), total=df_nutramount.shape[0], desc="nutrientamount"):
        try:
            f = Food.objects.get(pk=int(dat["FOOD_C"]))
        except:
            f = None
        try:
            n = Nutrient.objects.get(pk=int(dat["NUTR_C"]))
        except:
            n = None
        if n is None:
            print("Can't find a nutrient with code {}".format(dat["NUTR_C"]))
            continue

        try:
            s = NutrientSource.objects.get(pk=int(dat["SOURCE_C"]))
        except:
            s = None
        try:
            r = NutrientReference.objects.get(pk=int(dat["SOURCE_C"]))
        except:
            r = None


        NutrientOfFood.objects.get_or_create(
            NUTR_AMOUNT_C = convert_to_int(dat["NUTR_AMOUNT_C"]),
            FOOD = f,
            NUTR = n,
            SOURCE = s,
            REF = r,
            NUTR_VALUE = dat["NUTR_VALUE"],
            STD_ERROR = dat["STD_ERROR"],
            NUM_OBSER = dat["NUM_OBSER"],

            METHOD_C=dat["METHOD_C"],

            COMMENT_T=dat["COMMENT_T"],
            FLAG_TRACE=reformat_bool(dat["FLAG_TRACE"]),
            PUBLICATION_CODE=dat["PUBLICATION_CODE"],
            USDA_SOURCE=dat["USDA_SOURCE"],
            USDA_DERIV=dat["USDA_DERIV"],
            FN_SYS_USER_CREATE_C=dat["FN_SYS_USER_CREATE_C"],
            FN_SYS_USER_EDIT_C=dat["FN_SYS_USER_EDIT_C"],

            DATE_ENTRY=dat["DATE_ENTRY"],
            DATE_CHANGE=dat["DATE_CHANGE"],
            DATE_END=dat["DATE_END"],
            PENTAHO_CREATE_DATE=dat["PENTAHO_CREATE_DATE"]
        )

    conn = psycopg2.connect(user = "averster",
                                  password = "Boat1234",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "cnf_xplor")
    cur = conn.cursor()
    cur.execute(" SELECT setval('\"api_nutrientoffood_NUTR_AMOUNT_C_seq\"',(SELECT max(\"NUTR_AMOUNT_C\") + 1 FROM api_nutrientoffood));")
    cur.execute(" SELECT setval('\"api_nutrient_NUTR_C_seq\"',(SELECT max(\"NUTR_C\") + 1 FROM api_nutrient));")


def fill_out_nutrients():
    from cnf_xplor.api.models import Food
    from nutrition_db.food_enter.update_database import add_all_nutrients_to_food
    for f in Food.objects.all():
        add_all_nutrients_to_food(f)

enter_foodgroup()
enter_source()
enter_food()
enter_conversion_factors()
add_nutrients()
#fill_out_nutrients()
