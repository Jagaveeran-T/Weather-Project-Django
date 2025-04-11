from django.test import TestCase

# Create your tests here.
class SampleTest(TestCase):
    def test_basic(self):
        self.assertEqual(1 + 1, 2)