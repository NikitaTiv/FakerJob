from django.test import TestCase

from candidates.utils import create_candidates_data


class GetCandidatesTestCase(TestCase):
    def test__get_data_without_args__success_case(self):
        self.assertEqual(create_candidates_data(), 10)
