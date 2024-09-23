from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pass
    # add additional fields in here

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
        super().save(*args, **kwargs)


class Rating(models.Model):
    validators = [MinValueValidator(1.0), MaxValueValidator(5)]
    validators_ext = [MinValueValidator(0.0), MaxValueValidator(5)]

    carry = models.OneToOneField(Carry, on_delete=models.CASCADE)

    newborns = models.FloatField(validators=validators, default=1)
    legstraighteners = models.FloatField(validators=validators_ext, default=1)
    leaners = models.FloatField(validators=validators_ext, default=1)
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
        }


class FavouriteCarry(models.Model):
    carry = models.ForeignKey(Carry, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class DoneCarry(models.Model):
    carry = models.ForeignKey(Carry, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class TodoCarry(models.Model):
    carry = models.ForeignKey(Carry, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


