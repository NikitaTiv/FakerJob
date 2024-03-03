from django.test import TestCase
import json
import requests
from unittest.mock import Mock, patch

from candidates.consts import GENDER_DICT, INVERTED_COUNTRY_DICT
from candidates.models import Candidate
from candidates.utils import FAKE_PASSWORD, RandomUserDataCreator


class RandomUserDataCreatorTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.creator = RandomUserDataCreator()
        cls.candidate_data = {'results': [
            {
                'gender': 'male', 'name': {'title': 'Mr', 'first': 'Damien', 'last': 'Moreau'},
                'location': {
                    'street': {'number': 8384, 'name': 'Rue André-Gide'}, 'city': 'Roubaix',
                    'state': 'Pyrénées-Orientales', 'country': 'France', 'postcode': 34040,
                    'coordinates': {'latitude': '-14.6379', 'longitude': '-33.5751'},
                    'timezone': {'offset': '-5:00', 'description': 'Eastern Time (US & Canada), Bogota, Lima'}
                },
                'email': 'damien.moreau@example.com',
                'login': {
                    'uuid': '2b4d6cc4-2064-4578-8420-c72f93cda7f3', 'username': 'blackbear826', 'password': 'delphi',
                    'salt': 'kbApwBHr', 'md5': 'd2b730cdddd77b73978e845a38d0cae2',
                    'sha1': '3bf4089bdda940ab0d799e8e346136effb66c3a1',
                    'sha256': '8b7ab9af9be66a38ad434b895dac619f8058efc9f37d14502418442b832656be'
                }
            }
        ]}

    def mocked_requests_get(self, *args, **kwargs):  # noqa: U100
        response_content = json.dumps(self.candidate_data)
        response = requests.models.Response()
        response.status_code = 200
        response._content = str.encode(response_content)
        return response

    @patch('logging.Logger.info')
    @patch('requests.get')
    # can be implemented like @patch('requests.get', side_effect=mocked_requests_get)
    def test__get_data__success_case(self, request_mock, logger_mock):
        request_mock.side_effect = self.mocked_requests_get
        candidates_qty_before = Candidate.objects.count()

        self.creator.run()

        items = Candidate.objects.all()
        obj = self.candidate_data['results'][0]
        self.assertEqual(candidates_qty_before, 0)
        self.assertEqual(items.count(), len(self.candidate_data['results']))
        self.assertEqual(items.first().username, obj['login']['username'])
        self.assertEqual(items.first().first_name, obj['name']['first'])
        self.assertEqual(items.first().last_name, obj['name']['last'])
        self.assertEqual(items.first().password, FAKE_PASSWORD)
        self.assertEqual(items.first().email, obj['email'])
        self.assertEqual(items.first().gender, GENDER_DICT.get(obj['gender']))
        self.assertEqual(items.first().about, '')
        self.assertEqual(items.first().country, INVERTED_COUNTRY_DICT.get(obj['location']['country']))
        self.assertEqual(items.first().is_fake, True)
        logger_mock.assert_called_once_with('RandomUserDataCreator: the new records has been added.')

    def test__prepare_data__success_case(self):
        self.creator.data = self.candidate_data['results']
        expected_obj = self.candidate_data['results'][0]
        expected_result = [
            {
                'email': expected_obj['email'], 'gender': GENDER_DICT.get(expected_obj['gender']), 'is_fake': True,
                'country': INVERTED_COUNTRY_DICT.get(expected_obj['location']['country']), 'about': '',
                'username': expected_obj['login']['username'], 'first_name': expected_obj['name']['first'],
                'last_name': expected_obj['name']['last'], 'password': FAKE_PASSWORD,
            }
        ]

        result = self.creator.prepare_data()

        self.assertListEqual(result, expected_result)

    @patch('requests.get')
    @patch('logging.Logger.info')
    def test__get_data__fail_case_service_unavailable(self, logger_mock, request_mock):
        fake_response = Mock()
        fake_response.status_code = 404
        fake_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Not Found")
        request_mock.return_value = fake_response

        self.creator.run()

        request_mock.assert_called_once()
        logger_mock.assert_called_once_with('RandomUserDataCreator: failed to get data.')
