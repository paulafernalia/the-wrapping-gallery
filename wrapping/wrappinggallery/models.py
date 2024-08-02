from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


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
            -1: "NA",
            0: "Starts centred",
            0.5: "Starts 0.5 measures off centre",
            1: "Starts 1 measure off centre",
            1.5: "Starts 1.5 measures off centre",
            2: "Starts 2 measures off centre",
        }
    )

    videotutorial = models.URLField(blank=True, null=True)

    videoauthor = models.CharField(max_length=64, blank=True, null=True)

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
        },
    )

    def __str__(self):
        return f"{self.name}: {self.position} carry, {self.size}, {self.mmposition}"

    def is_valid_carry(self):
        return not self.pretied or not self.position == "back"

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
        }


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
