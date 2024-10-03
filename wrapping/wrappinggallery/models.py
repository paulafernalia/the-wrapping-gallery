from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum, Count, Case, When, IntegerField, FloatField
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, blank=False, null=False)

    def __str__(self):
        return self.username

# Create your models here.
class Carry(models.Model):
    name = models.CharField(max_length=64, primary_key=True)

    title = models.CharField(max_length=64)
    longtitle = models.CharField(max_length=128)

    size = models.IntegerField(
        choices={
            -5: "Base - 5",
            -4: "Base - 4",
            -3: "Base - 3",
            -2: "Base - 2",
            -1: "Base - 1",
            0: "Base",
            1: "Base + 1",
            2: "Base + 2",
        }
    )

    shoulders = models.IntegerField(choices={0: "0", 1: "1", 2: "2"})

    layers = models.IntegerField(choices={-1: "Varies", 1: "1", 2: "2", 3: "3", 4: "4"})

    mmposition = models.IntegerField(
        choices={
            -1: "Follow tutorial",
            0: "Centred",
            6: "0.5 DH off centre",
            1: "1 DH off centre",
            7: "1.5 DH off centre",
            2: "2 DH off centre",
            3: "Centred on your chest",
            4: "Centred on your back",
            5: "Under your armpit",
        }
    )

    videotutorial = models.URLField(blank=True, null=True)
    videotutorial2 = models.URLField(blank=True, null=True)
    videotutorial3 = models.URLField(blank=True, null=True)

    videoauthor = models.CharField(max_length=64, blank=True, null=True)
    videoauthor2 = models.CharField(max_length=64, blank=True, null=True)
    videoauthor3 = models.CharField(max_length=64, blank=True, null=True)

    position = models.CharField(
        max_length=10,
        choices={"front": "Front", "back": "Back", "tandem": "Tandem"},
    )

    description = models.TextField(blank=True, null=True)

    pretied = models.BooleanField(default=False)
    rings = models.BooleanField(default=False)

    finish = models.CharField(
        max_length=16,
        choices={
            "knotless": "Knotless",
            "knotless tibetan": "Knotless Tibetan",
            "tibetan": "Tibetan",
            "TUB": "Tied under bum",
            "TIF": "Tied in front",
            "TAS": "Tied at shoulder",
            "buleria": "Buleria",
            "CCCB": "Candy Cane Chest Belt",
            "slipknot": "Slipknot",
            "ring(s)": "Rings",
            "rapunzel": "Rapunzel",
            "tied at the back": "Tied at the back",
            "strangleproof": "Strangleproof",
        },
    )

    PASS_CHOICES = {0: "", 1: "", 2: "(2)", 3: "(3)"}

    pass_horizontal = models.IntegerField(default=0, choices=PASS_CHOICES)
    pass_sling = models.IntegerField(default=0, choices=PASS_CHOICES)
    pass_cross = models.IntegerField(default=0, choices=PASS_CHOICES)
    pass_reinforcing_cross = models.IntegerField(default=0, choices=PASS_CHOICES)
    pass_reinforcing_horizontal = models.IntegerField(default=0, choices=PASS_CHOICES)
    pass_poppins = models.IntegerField(default=0, choices=PASS_CHOICES)
    pass_ruck = models.IntegerField(default=0, choices=PASS_CHOICES)
    pass_kangaroo = models.IntegerField(default=0, choices=PASS_CHOICES)

    other_chestpass = models.BooleanField(default=0)
    other_bunchedpasses = models.BooleanField(default=0)
    other_shoulderflip = models.BooleanField(default=0)
    other_twistedpass = models.BooleanField(default=0)
    other_waistband = models.BooleanField(default=0)
    other_legpasses = models.BooleanField(default=0)
    other_s2s = models.BooleanField(default=0)
    other_eyelet = models.BooleanField(default=0)
    other_sternum = models.BooleanField(default=0)
    other_poppins = models.BooleanField(default=0)


    def __str__(self):
        return f"{self.name}: {self.position} carry, {self.size}, {self.mmposition}"
        

    def to_dict(self):
        return {
            "name": self.name,
            "title": self.title,
            "longtitle": self.longtitle,
            "size": self.get_size_display(),
            "shoulders": self.get_shoulders_display(),
            "layers": self.get_layers_display(),
            "mmposition": self.get_mmposition_display(),
            "position": self.get_position_display(),
            "finish": self.get_finish_display(),
            "pretied": self.pretied,
            "rings": self.rings,
            "description": self.description,
            "videotutorial": self.videotutorial,
            "videoauthor": self.videoauthor,
            "videotutorial2": self.videotutorial2,
            "videoauthor2": self.videoauthor2,
            "videotutorial3": self.videotutorial3,
            "videoauthor3": self.videoauthor3,
            "passes": [
                pass_name for pass_name in [
                    f"horizontal (2)" if self.pass_horizontal == 2 else "horizontal" if self.pass_horizontal == 1 else None,
                    f"sling (2)" if self.pass_sling == 2 else "sling" if self.pass_sling == 1 else None,
                    f"cross (2)" if self.pass_cross == 2 else "cross" if self.pass_cross == 1 else None,
                    f"reinforcing cross (2)" if self.pass_reinforcing_cross == 2 else "reinforcing cross" if self.pass_reinforcing_cross == 1 else None,
                    f"reinforcing horizontal (2)" if self.pass_reinforcing_horizontal == 2 else "reinforcing horizontal" if self.pass_reinforcing_horizontal == 1 else None,
                    f"poppins (2)" if self.pass_poppins == 2 else "poppins" if self.pass_poppins == 1 else None,
                    f"ruck (2)" if self.pass_ruck == 2 else "ruck" if self.pass_ruck == 1 else None,
                    f"kangaroo (2)" if self.pass_kangaroo == 2 else "kangaroo" if self.pass_kangaroo == 1 else None,
                ]  if pass_name is not None
            ],
            "other": [
                other_name for other_name in [
                    "chest pass" if self.other_chestpass == True else None,
                    "bunched passes" if self.other_bunchedpasses == True else None,
                    "shoulder flip" if self.other_shoulderflip == True else None,
                    "twisted pass" if self.other_twistedpass == True else None,
                    "waist band" if self.other_waistband == True else None,
                    "leg passes" if self.other_legpasses == True else None,
                    "shoulder to shoulder" if self.other_s2s == True else None,
                    "eyelet" if self.other_eyelet == True else None,
                    "sternum belt" if self.other_sternum == True else None,
                    "poppins" if self.other_poppins == True else None,
                ] if other_name is not None
            ]
        }


    def clean(self):
        # Ensure carry cannot be pretied if it is a back carry
        if self.pretied == 1 and self.position == "back" and self.name != "traditional_back_carry":
            raise ValidationError(
                "a back carry cannot be pretied"
            )

        # Ensure videoauthor2 cannot be not null if videoauthor is null
        if self.videoauthor2 and not self.videoauthor:
            raise ValidationError(
                "videoauthor2 cannot be set if videoauthor is null."
            )

        # Ensure videoauthor3 cannot be not null if videoauthor2 is null
        if self.videoauthor3 and not self.videoauthor2:
            raise ValidationError(
                "videoauthor3 cannot be set if videoauthor2 is null."
            )

        # Ensure that if one of the pair is set, the other must also be set
        if (self.videotutorial and not self.videoauthor) or \
           (not self.videotutorial and self.videoauthor):
            raise ValidationError(
                "Both videoauthor and videotutorial must be either set or both blank."
            )

        if (self.videotutorial2 and not self.videoauthor2) or \
           (not self.videotutorial2 and self.videoauthor2):
            raise ValidationError(
                "Both videoauthor2 and videotutorial2 must be either set or both blank."
            )

        if (self.videotutorial3 and not self.videoauthor3) or \
           (not self.videotutorial3 and self.videoauthor3):
            raise ValidationError(
                "Both videoauthor3 and videotutorial3 must be either set or both blank."
            )

        if not (self.rings) == ("ring" in self.title.lower()) and \
            ("xena" not in self.name) and ("mermaid" not in self.name)  and ("lola" not in self.name):
            raise ValidationError("inconsistent information regarding ring(s)")

        num_passes = self.pass_sling
        num_passes += self.pass_ruck
        num_passes += self.pass_horizontal
        num_passes += self.pass_cross
        num_passes += self.pass_kangaroo
        num_passes += self.pass_reinforcing_cross
        num_passes += self.pass_reinforcing_horizontal
        num_passes += 2 * self.pass_poppins
        if self.layers != num_passes and self.position != "tandem":
            raise ValidationError(
                f"Layers ({self.layers}) inconsistent with passes ({num_passes})"
            )

        num_shoulders = self.pass_cross
        num_shoulders += self.pass_sling
        num_shoulders += 2 * self.pass_ruck
        num_shoulders += 2 * self.pass_kangaroo
        if (self.name != "ruck_celtic_knot") and \
           (self.position != "tandem") and \
           ('fwcc' not in self.name) and \
           ('frts' not in self.name) and \
           ('poppins' not in self.name) and \
           (self.shoulders != num_shoulders):
            raise ValidationError(
                f"Shoulders ({self.shoulders}) inconsistent with passes ({num_shoulders})"
            )

        if not self.other_legpasses and self.pass_reinforcing_cross + self.pass_cross > 0:
            raise ValidationError(
                f"Leg passes cannot be 0 with cross and reinforcing cross pass"
            )

        if "dh" in self.name and "fdh"not in self.name and self.other_chestpass == False:
            raise ValidationError(
                f"Chest pass cannot be 0 in a double hammock variation"
            )

        if (self.name != "ruckless_bikini_carry") and \
            ("christina" not in self.name) and \
            ("ruck" in self.name and self.pass_ruck == 0):
            raise ValidationError(
                f"Ruck pass cannot be empty in a ruck variation"
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)  # Save the Carry instance first

        # Check if a Rating entry exists for this carry
        rating, created = Rating.objects.get_or_create(
            carry=self,
            defaults={
                "newborns": 0,
                "legstraighteners": 0,
                "leaners": 0,
                "bigkids": 0,
                "feeding": 0,
                "quickups": 0,
                "pregnancy": 0,
                "difficulty": 0,
                "fancy": 0,
                "votes": 0,
            }
        )

        if created:
            print(f"- Rating entry has been created for {self.name}")  # Log when a new Rating is created


class Rating(models.Model):
    validators = [MinValueValidator(0.0), MaxValueValidator(5)]

    carry = models.OneToOneField(Carry, on_delete=models.CASCADE)

    newborns = models.FloatField(validators=validators, default=1)
    legstraighteners = models.FloatField(validators=validators, default=1)
    leaners = models.FloatField(validators=validators, default=1)
    bigkids = models.FloatField(validators=validators, default=1)
    feeding = models.FloatField(validators=validators, default=1)
    quickups = models.FloatField(validators=validators, default=1)

    pregnancy = models.FloatField(validators=validators, default=1)
    difficulty = models.FloatField(validators=validators, default=1)
    fancy = models.FloatField(validators=validators, default=1)

    votes = models.IntegerField(blank=True, null=True, default=0)

    def to_dict(self):
        return {
            "newborns": round(self.newborns),
            "legstraighteners": round(self.legstraighteners),
            "leaners": round(self.leaners),
            "bigkids": round(self.bigkids),
            "feeding": round(self.feeding),
            "quickups": round(self.quickups),
            "pregnancy": round(self.pregnancy),
            "difficulty": round(self.difficulty),
            "fancy": round(self.fancy),
            "votes": self.votes,
        }


def NZ_AVG(queryset, field_name):
    # Count non-zero values
    count_non_zero = queryset.filter(**{field_name + '__gt': 0}).count()
    
    # Sum non-zero values
    sum_non_zero = queryset.filter(**{field_name + '__gt': 0}).aggregate(Sum(field_name))[f"{field_name}__sum"] or 0

    # Calculate average, return 0 if there are no non-zero values
    return sum_non_zero / count_non_zero if count_non_zero > 0 else 0


class UserRating(models.Model):
    validators = [MinValueValidator(0.0), MaxValueValidator(5)]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    carry = models.ForeignKey(Carry, on_delete=models.CASCADE)

    newborns = models.FloatField(validators=validators, default=1)
    legstraighteners = models.FloatField(validators=validators, default=1)
    leaners = models.FloatField(validators=validators, default=1)
    bigkids = models.FloatField(validators=validators, default=1)
    feeding = models.FloatField(validators=validators, default=1)
    quickups = models.FloatField(validators=validators, default=1)

    pregnancy = models.FloatField(validators=validators, default=1)
    difficulty = models.FloatField(validators=validators, default=1)
    fancy = models.FloatField(validators=validators, default=1)

    class Meta:
        unique_together = ('user', 'carry')

    def to_dict(self):
        return {
            "newborns": round(self.newborns),
            "legstraighteners": round(self.legstraighteners),
            "leaners": round(self.leaners),
            "bigkids": round(self.bigkids),
            "feeding": round(self.feeding),
            "quickups": round(self.quickups),
            "pregnancy": round(self.pregnancy),
            "difficulty": round(self.difficulty),
            "fancy": round(self.fancy),
            "username": self.user.username,  # Get the username from CustomUser
            "carry_name": self.carry.name,    # Get the name from Carry
        }

    def update_rating(self):
        # Now update the corresponding Rating entry
        try:
            # Fetch the Rating entry for the associated carry
            rating = Rating.objects.get(carry=self.carry)

            # Fetch all UserRating entries for this carry and calculate averages in one query
            user_ratings = UserRating.objects.filter(carry=self.carry)

            # Calculate counts of non-zero entries
            non_zero_counts = user_ratings.aggregate(
                newborns_count=Count(Case(When(newborns__gt=0, then=1), output_field=IntegerField())),
                legstraighteners_count=Count(Case(When(legstraighteners__gt=0, then=1), output_field=IntegerField())),
                leaners_count=Count(Case(When(leaners__gt=0, then=1), output_field=IntegerField())),
                bigkids_count=Count(Case(When(bigkids__gt=0, then=1), output_field=IntegerField())),
                feeding_count=Count(Case(When(feeding__gt=0, then=1), output_field=IntegerField())),
                quickups_count=Count(Case(When(quickups__gt=0, then=1), output_field=IntegerField())),
                pregnancy_count=Count(Case(When(pregnancy__gt=0, then=1), output_field=IntegerField())),
                difficulty_count=Count(Case(When(difficulty__gt=0, then=1), output_field=IntegerField())),
                fancy_count=Count(Case(When(fancy__gt=0, then=1), output_field=IntegerField())),
            )

            # Calculate sums of non-zero entries
            total_sums = user_ratings.aggregate(
                newborns_sum=Sum(Case(When(newborns__gt=0, then='newborns'), default=0, output_field=FloatField())),
                legstraighteners_sum=Sum(Case(When(legstraighteners__gt=0, then='legstraighteners'), default=0, output_field=FloatField())),
                leaners_sum=Sum(Case(When(leaners__gt=0, then='leaners'), default=0, output_field=FloatField())),
                bigkids_sum=Sum(Case(When(bigkids__gt=0, then='bigkids'), default=0, output_field=FloatField())),
                feeding_sum=Sum(Case(When(feeding__gt=0, then='feeding'), default=0, output_field=FloatField())),
                quickups_sum=Sum(Case(When(quickups__gt=0, then='quickups'), default=0, output_field=FloatField())),
                pregnancy_sum=Sum(Case(When(pregnancy__gt=0, then='pregnancy'), default=0, output_field=FloatField())),
                difficulty_sum=Sum(Case(When(difficulty__gt=0, then='difficulty'), default=0, output_field=FloatField())),
                fancy_sum=Sum(Case(When(fancy__gt=0, then='fancy'), default=0, output_field=FloatField())),
            )

            # Update the rating fields using the sums and counts
            rating.newborns = total_sums['newborns_sum'] / non_zero_counts['newborns_count'] if non_zero_counts['newborns_count'] > 0 else 0
            rating.legstraighteners = total_sums['legstraighteners_sum'] / non_zero_counts['legstraighteners_count'] if non_zero_counts['legstraighteners_count'] > 0 else 0
            rating.leaners = total_sums['leaners_sum'] / non_zero_counts['leaners_count'] if non_zero_counts['leaners_count'] > 0 else 0
            rating.bigkids = total_sums['bigkids_sum'] / non_zero_counts['bigkids_count'] if non_zero_counts['bigkids_count'] > 0 else 0
            rating.feeding = total_sums['feeding_sum'] / non_zero_counts['feeding_count'] if non_zero_counts['feeding_count'] > 0 else 0
            rating.quickups = total_sums['quickups_sum'] / non_zero_counts['quickups_count'] if non_zero_counts['quickups_count'] > 0 else 0
            rating.pregnancy = total_sums['pregnancy_sum'] / non_zero_counts['pregnancy_count'] if non_zero_counts['pregnancy_count'] > 0 else 0
            rating.difficulty = total_sums['difficulty_sum'] / non_zero_counts['difficulty_count'] if non_zero_counts['difficulty_count'] > 0 else 0
            rating.fancy = total_sums['fancy_sum'] / non_zero_counts['fancy_count'] if non_zero_counts['fancy_count'] > 0 else 0

            # Update the vote field with the count of UserRating entries for this carry
            rating.votes = user_ratings.count()

            rating.save()  # Save the updated Rating entry

        except Rating.DoesNotExist:
            print("Rating does not exist for the given carry.")
        except Exception as e:
            print(str(e))


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the parent class's save method

        # Call your shared logic
        self.update_rating()
        

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)  # Call the parent class's delete method
        
        # Call your shared logic
        self.update_rating()


class FavouriteCarry(models.Model):
    carry = models.ForeignKey(Carry, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class DoneCarry(models.Model):
    carry = models.ForeignKey(Carry, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class TodoCarry(models.Model):
    carry = models.ForeignKey(Carry, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Achievement(models.Model):
    name = models.CharField(max_length=64, primary_key=True, unique=True)
    title = models.CharField(max_length=64)

    CATEGORY_CHOICES = [
        (0, "Onboarding"),
        (1, 'Wrapping'),
        (2, 'Contributor'),
        (3, 'Special'),
    ]

    category = models.IntegerField(
        choices=CATEGORY_CHOICES
    )

    description = models.TextField()
    order = models.FloatField(blank=True)


class UserAchievement(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

