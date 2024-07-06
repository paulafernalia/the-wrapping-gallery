from django.db import models

# Create your models here.
class Carry(models.Model):
    name = models.CharField(max_length=64, primary_key=True)

    title = models.CharField(max_length=64)

    size = models.IntegerField(
        choices = {
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

    shoulders = models.IntegerField(
        choices={0: "Torso", 1: "One", 2: "Two"}
    )

    layers = models.IntegerField(
        choices={1: "One", 2: "Two", 3: "Three", 4: "Four"}
    )

    mmposition = models.IntegerField(
        choices={
            0: "Starts centred",
            0.5: "Starts half an arm length off centre",
            1: "Starts one arm length off centre",
            1.5: "Starts one and a half arm lengths off centre",
            2: "Starts two arm lengths off centre",
        }
    )

    videotutorial = models.URLField(blank=True)

    videoauthor = models.CharField(max_length=64, blank=True)

    position = models.CharField(
        max_length=5,
        choices={"front": "front", "back": "back"},
    )

    description = models.TextField(blank=True)

    pretied = models.BooleanField()

    finish = models.CharField(
        max_length=16,
        choices={
            "knotless": "knotless",
            "knotless tibetan": "knotless tibetan",
            "tibetan": "tibetan",
            "TUB": "tied under bum",
            "TIF": "tied in front",
            "TAS": "tied at shoulder",
            "buleria": "buleria",
            "CCCB": "candy cane chest belt",
            "slipknot": "slipknot",
            "ring(s)": "rings",
            "rapunzel": "rapunzel",
            "tied at the back": "tied at the back"
        }
    )

    coverpicture = models.ImageField(blank=True)

    def __str__(self):
        return f"{self.name}: {self.position} carry, {self.size}, {self.mmposition}"
