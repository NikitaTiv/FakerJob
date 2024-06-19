from django.test import TestCase
from unittest.mock import patch

from candidates.models import Candidate


class CandidateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.candidate_1 = Candidate.objects.create(**{'email': 'real_1_test@example.com', 'username': 'real_user1',
                                                      'photo': 'folder/test.jpg'})
        cls.candidate_2 = Candidate.objects.create(**{'email': 'real_2_test@example.com', 'username': 'real_user2'})
        Candidate.objects.create(**{'email': 'fake_test@example.com', 'is_fake': True, 'username': 'fake_user'})

    def test__manager__success_case(self):
        self.assertEqual(Candidate.objects.count(), 3)
        self.assertEqual(Candidate.real_objects.count(), 2)
        self.assertEqual(Candidate.fake_objects.count(), 1)

    def test__check_remove__success_case(self):  # need to cover the case more
        old_file_name = self.candidate_1.photo

        with patch('os.remove', side_effect=FileNotFoundError) as remove_mock, \
            patch('logging.Logger.info') as logger_mock:
            self.candidate_1.photo = 'folder/test_delete.jpg'
            self.candidate_1.save()

        remove_mock.assert_called_once()
        logger_mock.assert_called_once_with(f"The {old_file_name} for user ID "
                                            f"{self.candidate_1.pk} doesn't exist.")

    def test__check_remove__no_photo_remove_wont_happen(self):
        with patch('os.remove') as remove_mock, \
            patch('logging.Logger.info') as logger_mock:
            self.candidate_2.save()
            remove_mock.assert_not_called()
            logger_mock.assert_not_called()
