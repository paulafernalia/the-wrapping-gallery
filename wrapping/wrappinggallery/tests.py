from django.test import TestCase
from .models import Carry, Ratings
from django.db import IntegrityError
from django.core.exceptions import ValidationError


# Create your tests here.
class CarryTestCase(TestCase):

    def setUp(self):
        # Create a Carry instance.
        self.c1 = Carry.objects.create(
            name="CarryTestCase",
            title="Ruck",
            size=0,
            shoulders=2,
            layers=1,
            mmposition=0,
            position="back",
            pretied=False,  # corrected boolean value
            finish="TIF",
        )

    def test_carries_count(self):
        c = Carry.objects.all()
        self.assertEqual(c.count(), 1)

    def test_add_rating(self):
        # Add a rating to the Carry instance.
        rating = Ratings.objects.create(
            carry=self.c1,
            newborns=4.0,
            legstraighteners=3.0,
            leaners=5.0,
            bigkids=2.0,
            feeding=4.0,
            quickups=5.0,
            difficulty=3.0,
            fancy=4.0,
            votes=10,
        )
        
        # Fetch the rating and check its values.
        r = Ratings.objects.get(carry=self.c1)
        self.assertEqual(r.newborns, 4.0)
        self.assertEqual(r.legstraighteners, 3.0)
        self.assertEqual(r.leaners, 5.0)
        self.assertEqual(r.bigkids, 2.0)
        self.assertEqual(r.feeding, 4.0)
        self.assertEqual(r.quickups, 5.0)
        self.assertEqual(r.difficulty, 3.0)
        self.assertEqual(r.fancy, 4.0)
        self.assertEqual(r.votes, 10)

    def test_cascade_delete_carry(self):
        # Add a rating to the Carry instance.
        rating = Ratings.objects.create(
            carry=self.c1,
            newborns=4.0,
            legstraighteners=3.0,
            leaners=5.0,
            bigkids=2.0,
            feeding=4.0,
            quickups=5.0,
            difficulty=3.0,
            fancy=4.0,
            votes=10,
        )

         # Delete the Carry instance.
        carry_name = self.c1.name
        self.c1.delete()

        # Check that the rating is also deleted.
        ratings_count = Ratings.objects.filter(carry__name=carry_name).count()
        self.assertEqual(ratings_count, 0)


    def test_no_duplicate_ratings(self):
        # Add a rating to the Carry instance.
        rating = Ratings.objects.create(
            carry=self.c1,
            newborns=4.0,
            legstraighteners=3.0,
            leaners=5.0,
            bigkids=2.0,
            feeding=4.0,
            quickups=5.0,
            difficulty=3.0,
            fancy=4.0,
            votes=10,
        )

        # Attempt to add another rating for the same Carry instance.
        with self.assertRaises(IntegrityError):
            Ratings.objects.create(
                carry=self.c1,
                newborns=5.0,
                legstraighteners=4.0,
                leaners=3.0,
                bigkids=2.0,
                feeding=1.0,
                quickups=2.0,
                difficulty=5.0,
                fancy=1.0,
                votes=5,
            )

class CarryVideoTest(TestCase):

    def test_videoauthor2_cannot_be_set_if_videoauthor_is_null(self):
        carry = Carry(
            name="test_carry",
            title="Test Carry",
            size=0,
            shoulders=2,
            layers=2,
            mmposition=0,
            position="front",
            finish="TIF",
            videoauthor=None,
            videoauthor2="Author 2",
        )

        with self.assertRaises(ValidationError):
            carry.clean()

    def test_videoauthor3_cannot_be_set_if_videoauthor2_is_null(self):
        carry = Carry(
            name="test_carry",
            title="Test Carry",
            size=0,
            shoulders=2,
            layers=2,
            mmposition=0,
            position="front",
            finish="TIF",
            videoauthor="Author 1",
            videoauthor2=None,
            videoauthor3="Author 3",
        )

        with self.assertRaises(ValidationError):
            carry.clean()

    def test_valid_carry_with_videoauthors(self):
        carry = Carry(
            name="test_carry",
            title="Test Carry",
            size=0,
            shoulders=2,
            layers=2,
            mmposition=0,
            position="front",
            finish="TIF",
            videoauthor="Author 1",
            videoauthor2="Author 2",
            videoauthor3="Author 3",
        )

        try:
            carry.clean()  # Should not raise any exceptions
        except ValidationError:
            self.fail("Carry.clean() raised ValidationError unexpectedly!")
