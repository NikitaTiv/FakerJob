from django.test import TestCase

from candidates.models import Candidate


class CandidateTestCase(TestCase):
    def test__manager__success_case(self):
        Candidate.objects.create(**{'email': 'real_1_test@example.com', 'username': 'real_user1'})
        Candidate.objects.create(**{'email': 'real_2_test@example.com', 'username': 'real_user2'})
        Candidate.objects.create(**{'email': 'fake_test@example.com', 'is_fake': True,'username': 'fake_user'})

        total_count = Candidate.objects.count()
        real_count = Candidate.real_objects.count()
        fake_count = Candidate.fake_objects.count()

        self.assertEqual(total_count, 3)
        self.assertEqual(real_count, 2)
        self.assertEqual(fake_count, 1)
