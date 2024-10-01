from django.test import TestCase
from .models import Carry, Rating, CustomUser, UserRating
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

    def test_ratings_count(self):
        r = Rating.objects.all()
        self.assertEqual(r.count(), 1)

    def test_cascade_delete_carry(self):
         # Delete the Carry instance.
        carry_name = self.c1.name
        self.c1.delete()

        # Check that the rating is also deleted.
        ratings_count = Rating.objects.filter(carry__name=carry_name).count()
        self.assertEqual(ratings_count, 0)


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


class UserRatingTestCase(TestCase):
    def setUp(self):
        # Create a user and a carry for testing
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword',
        )

        self.carry = Carry.objects.create(
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

    def test_user_rating_create_updates_rating(self):
        # Create a UserRating entry
        user_rating = UserRating.objects.create(
            user=self.user,
            carry=self.carry,
            newborns=4,
            legstraighteners=3,
            leaners=5,
            bigkids=2,
            feeding=4,
            quickups=3,
            pregnancy=2,
            difficulty=5,
            fancy=4,
        )

        # Fetch the corresponding Rating entry
        updated_rating = Rating.objects.get(carry=self.carry)

        # Check if the Rating entry is updated correctly
        self.assertEqual(updated_rating.newborns, 4)
        self.assertEqual(updated_rating.legstraighteners, 3)
        self.assertEqual(updated_rating.leaners, 5)
        self.assertEqual(updated_rating.bigkids, 2)
        self.assertEqual(updated_rating.feeding, 4)
        self.assertEqual(updated_rating.quickups, 3)
        self.assertEqual(updated_rating.pregnancy, 2)
        self.assertEqual(updated_rating.difficulty, 5)
        self.assertEqual(updated_rating.fancy, 4)
        self.assertEqual(updated_rating.votes, 1)

    def test_user_rating_update_updates_rating(self):
        # Create a UserRating entry
        user_rating = UserRating.objects.create(
            user=self.user,
            carry=self.carry,
            newborns=3,
            legstraighteners=2,
            leaners=4,
            bigkids=1,
            feeding=3,
            quickups=2,
            pregnancy=1,
            difficulty=4,
            fancy=3,
        )
        
        # Update the UserRating entry
        user_rating.newborns = 5
        user_rating.save()  # This should trigger update_rating

        # Fetch the corresponding Rating entry
        updated_rating = Rating.objects.get(carry=self.carry)

        # Check if the Rating entry is updated correctly
        self.assertEqual(updated_rating.newborns, 5)  # This will depend on existing UserRatings

    def test_user_rating_delete_updates_rating(self):
        # Create a UserRating entry
        user_rating = UserRating.objects.create(
            user=self.user,
            carry=self.carry,
            newborns=4,
            legstraighteners=3,
            leaners=5,
            bigkids=2,
            feeding=4,
            quickups=3,
            pregnancy=2,
            difficulty=5,
            fancy=4,
        )

        # Delete the UserRating entry
        user_rating.delete()  # This should trigger update_rating

        # Fetch the corresponding Rating entry
        updated_rating = Rating.objects.get(carry=self.carry)

        # Check if the Rating entry is updated correctly
        self.assertEqual(updated_rating.votes, 0)  # Assuming no other UserRatings exist


from django.core import mail
from django.test import TestCase
from django.urls import reverse

class PasswordResetEmailTest(TestCase):
    def setUp(self):
        # Create a user for the test
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@gmail.com',
            password='testpassword'
        )

    def test_password_reset_email(self):
        # Trigger the password reset process
        response = self.client.post(reverse('password_reset'), {
            'email': 'testuser@gmail.com'
        })

        # Check if an email was sent
        self.assertEqual(len(mail.outbox), 1)

        # Check the email subject
        self.assertEqual(mail.outbox[0].subject, 'Password reset on testserver')

        # Check the recipient list
        self.assertEqual(mail.outbox[0].to, ['testuser@gmail.com'])

        # Optionally check the email body content
        self.assertIn('you requested a password reset for your user account', mail.outbox[0].body)

