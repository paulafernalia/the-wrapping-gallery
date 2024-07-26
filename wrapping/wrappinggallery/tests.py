from django.test import TestCase
from .models import Carry


# Create your tests here.
class CarryTestCase(TestCase):

    def setUp(self):

        # Create airports.
        c1 = Carry.objects.create(
            name="CarryTestCase",
            title="Ruck",
            size=0,
            shoulders=2,
            layers=1,
            mmposition=0,
            position="back",
            pretied="False",
            finish="TIF",
        )

    def test_carries_count(self):
        c = Carry.objects.all()
        self.assertEqual(c.count(), 1)
