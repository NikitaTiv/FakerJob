import logging
import os
import requests

from candidates.consts import GENDER_DICT, INVERTED_COUNTRY_DICT
from candidates.models import Candidate

logger = logging.getLogger(__name__)

FAKE_PASSWORD = os.environ.get('FAKE_PASSWORD', 'test_password')


class RandomUserDataCreator:
    CANDIDATES_URL = 'https://randomuser.me/api/'
    REQUIRED_FIELDS = 'gender,name,location,email,login'
    DEFAULT_RECORDS_QTY = 10

    def __init__(self, quantity: int = DEFAULT_RECORDS_QTY) -> None:
        self.data: list = []
        self.quantity: int = quantity

    def get_data(self) -> None:
        params: dict[str, str | int] = {'results': self.quantity, 'inc': self.REQUIRED_FIELDS}
        try:
            response = requests.get(self.CANDIDATES_URL, params=params)
            response.raise_for_status()
            self.data = response.json()['results']
        except requests.exceptions.HTTPError:
            return

    def prepare_data(self) -> list[dict[str, str | bool]]:
        prepared_data = []
        for obj in self.data:
            prepared_data.append({
                'email': obj['email'],
                'gender': GENDER_DICT.get(obj['gender']),
                'about': '',
                'country': INVERTED_COUNTRY_DICT.get(obj['location']['country']),
                'is_fake': True,
                'username': obj['login']['username'],
                'first_name': obj['name']['first'],
                'last_name': obj['name']['last'],
            })
        return prepared_data

    def create_candidates_records(self, validated_data: list[dict[str, str | bool]]) -> list[Candidate]:
        candidate_list = []
        for obj_data in validated_data:
            user = Candidate(**obj_data)
            user.set_password(FAKE_PASSWORD)
            user.save()
            candidate_list.append(user)
        return candidate_list

    def run(self) -> None:
        self.get_data()
        if not self.data:
            logger.info('RandomUserDataCreator: failed to get data.')
            return
        validated_data = self.prepare_data()
        if self.create_candidates_records(validated_data):
            logger.info('RandomUserDataCreator: the new records has been added.')
