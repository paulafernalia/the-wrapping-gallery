from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Create your models here.
class Carry(models.Model):
    name = models.CharField(max_length=64, primary_key=True)

    title = models.CharField(max_length=64)

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

    shoulders = models.IntegerField(choices={0: "Zero (torso carry)", 1: "One", 2: "Two"})

    layers = models.IntegerField(choices={1: "One", 2: "Two", 3: "Three", 4: "Four"})

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
        max_length=5,
        choices={"front": "Front", "back": "Back"},
    )

    description = models.TextField(blank=True, null=True)

    pretied = models.BooleanField(default=False)

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

    def __str__(self):
        return f"{self.name}: {self.position} carry, {self.size}, {self.mmposition}"
        

    def to_dict(self):
        return {
            "name": self.name,
            "title": self.title,
            "size": self.get_size_display(),
            "shoulders": self.get_shoulders_display(),
            "layers": self.get_layers_display(),
            "mmposition": self.get_mmposition_display(),
            "position": self.get_position_display(),
            "finish": self.get_finish_display(),
            "pretied": self.pretied,
            "description": self.description,
            "videotutorial": self.videotutorial,
            "videoauthor": self.videoauthor,
            "videotutorial2": self.videotutorial2,
            "videoauthor2": self.videoauthor2,
            "videotutorial3": self.videotutorial3,
            "videoauthor3": self.videoauthor3,
        }


    def clean(self):
        # Ensure carry cannot be pretied if it is a back carry
        if self.pretied == 1 and self.position == "back":
            raise ValidationError("a back carry cannot be pretied")

        # Ensure videoauthor2 cannot be not null if videoauthor is null
        if self.videoauthor2 and not self.videoauthor:
            raise ValidationError("videoauthor2 cannot be set if videoauthor is null.")

        # Ensure videoauthor3 cannot be not null if videoauthor2 is null
        if self.videoauthor3 and not self.videoauthor2:
            raise ValidationError("videoauthor3 cannot be set if videoauthor2 is null.")

        # Ensure that if one of the pair is set, the other must also be set
        if (self.videotutorial and not self.videoauthor) or (not self.videotutorial and self.videoauthor):
            raise ValidationError("Both videoauthor and videotutorial must be either set or both blank.")

        if (self.videotutorial2 and not self.videoauthor2) or (not self.videotutorial2 and self.videoauthor2):
            raise ValidationError("Both videoauthor2 and videotutorial2 must be either set or both blank.")

        if (self.videotutorial3 and not self.videoauthor3) or (not self.videotutorial3 and self.videoauthor3):
            raise ValidationError("Both videoauthor3 and videotutorial3 must be either set or both blank.")


    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Ratings(models.Model):
    validators = [MinValueValidator(1.0), MaxValueValidator(5.0)]

    carry = models.OneToOneField(Carry, on_delete=models.CASCADE)

    newborns = models.FloatField(validators=validators, default=1)
    legstraighteners = models.FloatField(validators=validators, default=1)
    leaners = models.FloatField(validators=validators, default=1)
    bigkids = models.FloatField(validators=validators, default=1)
    feeding = models.FloatField(validators=validators, default=1)
    quickups = models.FloatField(validators=validators, default=1)

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
            "difficulty": round(self.difficulty),
            "fancy": round(self.fancy),
        }


class UserRatings(models.Model):
    validators = [MinValueValidator(1), MaxValueValidator(5)]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    carry = models.ForeignKey(Carry, on_delete=models.CASCADE)

    newborns = models.IntegerField(validators=validators)
    legstraighteners = models.IntegerField(validators=validators)
    leaners = models.IntegerField(validators=validators)
    bigkids = models.IntegerField(validators=validators)
    feeding = models.IntegerField(validators=validators)
    quickups = models.IntegerField(validators=validators)

    difficulty = models.IntegerField(validators=validators)

    fancy = models.IntegerField(validators=validators)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "carry"], name="unique_foreign_keys"
            )
        ]
