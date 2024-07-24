from django.test import TestCase
from .models import Carry, Ratings

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
            finish="TIF"
        )

    def test_carries_count(self):
        c = Carry.objects.all()
        self.assertEqual(c.count(), 1)


    def test_ratings_count(self):
        r = Ratings.objects.all()
        self.assertEqual(r.count(), 1)

        

class CarrySignalTestCase(TestCase):

    def test_create_ratings_on_carry_creation(self):
        # Create a Carry instance
        carry_instance = Carry.objects.create(
            name="CarrySignalTestCase",
            title="Ruck",
            size=0,
            shoulders=2,
            layers=1,
            mmposition=0,
            position="back",
            pretied="False",
            finish="TIF"
        )

        # Retrieve the Ratings instance that should have been created by the signal
        try:
            ratings_instance = Ratings.objects.get(carry=carry_instance)
        except Ratings.DoesNotExist:
            ratings_instance = None

        # Check that a Ratings instance was created
        self.assertIsNotNone(
            ratings_instance, "Ratings instance was not created"
        )

        # Check that the Ratings instance has the correct default values
        self.assertEqual(
            ratings_instance.bigkids, 1,
            "Ratings instance does not have default bigkids value of 1"
        )

        # Ensure that only one Ratings instance was created for the Carry instance
        self.assertEqual(
            Ratings.objects.count(), 1,
            "More than one Ratings instance was created for the Carry instance"
        )
