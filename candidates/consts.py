from django_countries import countries


INVERTED_COUNTRY_DICT = {country.name: country.code for country in countries}

GENDER_DICT = {'male': 0, 'female': 1}

DEFAULT_RECORDS_QTY = 10
