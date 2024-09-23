from django.test import TestCase
from .models import Carry, Rating
from django.db import IntegrityError
from django.core.exceptions import ValidationError


# Create your tests here.
class CarryTestCase(TestCase):

    def setUp(self):
        # Create a Carry instance.
        self.c1 = Carry.objects.create(
            name="CarryTestCase",
            title="Ruck",
            longtitle="Ruck",
            size=0,
            shoulders=2,
            layers=1,
            mmposition=0,
            position="back",
            pretied=False,  # corrected boolean value
            rings=False,
            finish="TIF",
            pass_ruck=1,
        )

    def test_carries_count(self):
        c = Carry.objects.all()
        self.assertEqual(c.count(), 1)

    def test_add_rating(self):
        # Add a rating to the Carry instance.
        rating = Rating.objects.create(
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
        r = Rating.objects.get(carry=self.c1)
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
        rating = Rating.objects.create(
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
        ratings_count = Rating.objects.filter(carry__name=carry_name).count()
        self.assertEqual(ratings_count, 0)


    def test_no_duplicate_ratings(self):
        # Add a rating to the Carry instance.
        rating = Rating.objects.create(
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
            Rating.objects.create(
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
            longtitle="Test Carry",
            size=0,
            shoulders=2,
            layers=2,
            mmposition=0,
            position="front",
            finish="TIF",
            videoauthor=None,
            videoauthor2="Author 2",
            videotutorial2="video2",
            pass_sling=2,
        )

        with self.assertRaises(ValidationError):
            carry.clean()

    def test_videoauthor3_cannot_be_set_if_videoauthor2_is_null(self):
        carry = Carry(
            name="test_carry",
            title="Test Carry",
            longtitle="Test Carry",
            size=0,
            shoulders=2,
            layers=2,
            mmposition=0,
            position="front",
            finish="TIF",
            videoauthor="Author 1",
            videotutorial="video1",
            videoauthor2=None,
            videoauthor3="Author 3",
            videotutorial3="video3",
            pass_sling=2,
        )

        with self.assertRaises(ValidationError):
            carry.clean()

    def test_valid_carry_with_videoauthors(self):
        carry = Carry(
            name="test_carry",
            title="Test Carry",
            longtitle="Test Carry",
            size=0,
            shoulders=2,
            layers=2,
            mmposition=0,
            position="front",
            finish="TIF",
            videotutorial="video1",
            videotutorial2="video2",
            videotutorial3="video3",
            videoauthor="Author 1",
            videoauthor2="Author 2",
            videoauthor3="Author 3",
            pass_sling=2,
        )

        try:
            carry.clean()  # Should not raise any exceptions
        except ValidationError:
            self.fail("Carry.clean() raised ValidationError unexpectedly!")

    def test_videoauthor_and_videotutorial_both_blank_or_filled(self):
        # Test case where both fields are blank
        carry = Carry(
            name="carry_test_1",
            title="Test Carry 1",
            longtitle="Test Carry",
            size=0,
            shoulders=2,
            layers=2,
            mmposition=0,
            position="front",
            finish="TUB",
            pass_sling=2,
        )
        try:
            carry.full_clean()  # This should pass
        except ValidationError:
            self.fail("ValidationError raised unexpectedly when both videoauthor and videotutorial are blank.")

        # Test case where both fields are filled
        carry.videotutorial = "http://example.com/video"
        carry.videoauthor = "Author Name"
        try:
            carry.full_clean()  # This should pass
        except ValidationError:
            self.fail("ValidationError raised unexpectedly when both videoauthor and videotutorial are filled.")

        # Test case where only one is filled
        carry.videoauthor = ""
        with self.assertRaises(ValidationError):
            carry.full_clean()  # This should raise a ValidationError

        carry.videoauthor = "Author Name"
        carry.videotutorial = ""
        with self.assertRaises(ValidationError):
            carry.full_clean()  # This should raise a ValidationError

    def test_videoauthor2_and_videotutorial2_both_blank_or_filled(self):
        # Similar tests for videoauthor2 and videotutorial2
        carry = Carry(
            name="carry_test_2",
            title="Test Carry 2",
            longtitle="Test Carry",
            size=0,
            shoulders=2,
            layers=2,
            mmposition=0,
            position="front",
            finish="TUB",
            videoauthor="Author 1",
            videotutorial="http://example.com/video1",
            pass_sling=2,
        )

        # Test case where both fields are blank
        carry.videotutorial2 = ""
        carry.videoauthor2 = ""
        try:
            carry.full_clean()  # This should pass
        except ValidationError:
            self.fail("ValidationError raised unexpectedly when both videoauthor2 and videotutorial2 are blank.")

        # Test case where both fields are filled
        carry.videotutorial2 = "http://example.com/video2"
        carry.videoauthor2 = "Author Name 2"
        try:
            carry.full_clean()  # This should pass
        except ValidationError:
            self.fail("ValidationError raised unexpectedly when both videoauthor2 and videotutorial2 are filled.")

        # Test case where only one is filled
        carry.videoauthor2 = ""
        with self.assertRaises(ValidationError):
            carry.full_clean()  # This should raise a ValidationError

        carry.videoauthor2 = "Author Name 2"
        carry.videotutorial2 = ""
        with self.assertRaises(ValidationError):
            carry.full_clean()  # This should raise a ValidationError

    def test_videoauthor3_and_videotutorial3_both_blank_or_filled(self):
        # Similar tests for videoauthor3 and videotutorial3
        carry = Carry(
            name="carry_test_3",
            title="Test Carry 3",
            longtitle="Test Carry",
            size=0,
            shoulders=2,
            layers=2,
            mmposition=0,
            position="front",
            finish="TUB",
            videoauthor="Author 1",
            videotutorial="http://example.com/video1",
            videoauthor2="Author 2",
            videotutorial2="http://example.com/video2",
            pass_sling=2,
        )

        # Test case where both fields are blank
        carry.videotutorial3 = ""
        carry.videoauthor3 = ""
        try:
            carry.full_clean()  # This should pass
        except ValidationError:
            self.fail("ValidationError raised unexpectedly when both videoauthor3 and videotutorial3 are blank.")

        # Test case where both fields are filled
        carry.videotutorial3 = "http://example.com/video3"
        carry.videoauthor3 = "Author Name 3"
        try:
            carry.full_clean()  # This should pass
        except ValidationError:
            self.fail("ValidationError raised unexpectedly when both videoauthor3 and videotutorial3 are filled.")

        # Test case where only one is filled
        carry.videoauthor3 = ""
        with self.assertRaises(ValidationError):
            carry.full_clean()  # This should raise a ValidationError

        carry.videoauthor3 = "Author Name 3"
        carry.videotutorial3 = ""
        with self.assertRaises(ValidationError):
            carry.full_clean()  # This should raise a ValidationError
