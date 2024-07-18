from django.test import TestCase
from .models import Carry, Ratings

# Create your tests here.
class CarryTestCase(TestCase):

    def setUp(self):

        # Create airports.
        c1 = Carry.objects.create(
            name="ruck",
            title="Ruck",
            size=0,
            shoulders=2,
            layers=1,
            mmposition=0,
            position="back",
            pretied="False",
            finish="TIF"
        )

        # Create flights.
        Ratings.objects.create(
            carry=c1,
            newborns=1,
            legstraighteners=1,
            leaners=1,
            bigkids=1,
            quickups=1,
            difficulty=1,
            feeding=1,
            fancy=1,
        )

    def test_carries_count(self):
        c = Carry.objects.all()
        self.assertEqual(c.count(), 1)


    def test_ratings_count(self):
        r = Ratings.objects.all()
        self.assertEqual(r.count(), 1)

        
