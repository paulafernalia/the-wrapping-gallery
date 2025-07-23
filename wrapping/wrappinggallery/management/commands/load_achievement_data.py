from typing import List, TypedDict

from django.core.management.base import BaseCommand

from wrappinggallery.models import Achievement


class Command(BaseCommand):
    help = "Loads achievement data into The Wrapping Gallery"

    def handle(self, *args, **kwargs):
        class AchievementData(TypedDict):
            name: str
            title: str
            order: int
            category: int
            description: str

        data: List[AchievementData] = [
            {
                "name": "one_carry",
                "title": "First carry",
                "order": 1,
                "category": 0,
                "description": "Registered your first woven wrap carry",
            },
            {
                "name": "five_carries",
                "title": "5 carries",
                "order": 2,
                "category": 1,
                "description": "You have done 5 woven wrap carries",
            },
            {
                "name": "ten_carries",
                "title": "10 carries",
                "order": 3,
                "category": 1,
                "description": "You have done 10 woven wrap carries",
            },
            {
                "name": "fifty_carries",
                "title": "50 carries",
                "order": 4,
                "category": 1,
                "description": "You have done 50 woven wrap carries",
            },
            {
                "name": "one_back_carry",
                "title": "First back carry",
                "order": 6,
                "category": 1,
                "description": "You have done your first back carry",
            },
            {
                "name": "one_tandem",
                "title": "First tandem carry",
                "order": 7,
                "category": 1,
                "description": "You have done your first tandem carry",
            },
            {
                "name": "one_front",
                "title": "First front carry",
                "order": 5,
                "category": 1,
                "description": "You have done your first front carry",
            },
            {
                "name": "one_beginner_plus",
                "title": "One beginner+ carry",
                "order": 8,
                "category": 1,
                "description": "You are no longer a beginner",
            },
            {
                "name": "one_intermediate",
                "title": "One intermediate carry",
                "order": 9,
                "category": 1,
                "description": "You are venturing out of your comfort zone",
            },
            {
                "name": "one_advanced",
                "title": "One advanced carry",
                "order": 10,
                "category": 1,
                "description": "You like a challenge",
            },
            {
                "name": "one_guru",
                "title": "One guru level carry",
                "order": 11,
                "category": 1,
                "description": "Nothing can stop you now",
            },
            {
                "name": "one_ring",
                "title": "The One Ring",
                "order": 12,
                "category": 1,
                "description": "You have done one carry with rings",
            },
            {
                "name": "nine_rings",
                "title": "Ringwraith",
                "order": 13,
                "category": 1,
                "description": "You have done 9 carry with rings",
            },
            {
                "name": "twenty_rings",
                "title": "Ring Leader",
                "order": 14,
                "category": 1,
                "description": "You have done 20 carries with rings",
            },
            {
                "name": "dh_apprentice",
                "title": "Double Hammock Apprentice",
                "order": 17,
                "category": 1,
                "description": "Completed 3 Double Hammock variations",
            },
            {
                "name": "dh_master",
                "title": "Double Hammock Master",
                "order": 18,
                "category": 1,
                "description": "Completed 10 Double Hammock variations",
            },
            {
                "name": "ruck_rookie",
                "title": "Ruck Rookie",
                "order": 15,
                "category": 1,
                "description": "Completed 3 Ruck variations",
            },
            {
                "name": "ruck_star",
                "title": "Ruck Star",
                "order": 16,
                "category": 1,
                "description": "Completed 10 Ruck variations",
            },
            {
                "name": "shortie_supreme",
                "title": "Less is more",
                "order": 19,
                "category": 1,
                "description": "Completed 10 shortie (base -5 to base -2) carries",
            },
            {
                "name": "longie_supreme",
                "title": "More is more",
                "order": 20,
                "category": 1,
                "description": "Completed 10 carries with a long wrap (base -1 to base +2)",
            },
            {
                "name": "sweet_tooth",
                "title": "Sweet Tooth",
                "order": 21,
                "category": 1,
                "description": "Completed 10 carries with a candy cane chest belt",
            },
            {
                "name": "toddler_prisoner",
                "title": "Toddler Prisoner",
                "order": 22,
                "category": 1,
                "description": "Completed 5 great carries for heavy, wriggly, seat poppers",
            },
            {
                "name": "pirates",
                "title": "Fearsome Pirate",
                "order": 23,
                "category": 1,
                "description": "Completed 3 pirate carries",
            },
            {
                "name": "one_review",
                "title": "Novice Critic",
                "order": 24,
                "category": 0,
                "description": "Completed your first review",
            },
            {
                "name": "five_reviews",
                "title": "Advisor",
                "order": 25,
                "category": 2,
                "description": "You have completed 5 reviews",
            },
            {
                "name": "ten_reviews",
                "title": "Advisor",
                "order": 26,
                "category": 2,
                "description": "You have completed 10 reviews",
            },
            {
                "name": "fifty_reviews",
                "title": "Expert Advisor",
                "order": 27,
                "category": 2,
                "description": "You have completed 50 reviews",
            },
            {
                "name": "one_month",
                "title": "Monthiversary",
                "order": 28,
                "category": 3,
                "description": "You have been a member of The Wrapping Gallery for a whole month",
            },
            {
                "name": "one_year",
                "title": "Anniversary",
                "order": 29,
                "category": 3,
                "description": "You have been a member of The Wrapping Gallery for a whole year",
            },
        ]

        for item in data:
            # Try to get the existing achievement
            achievement_qs = Achievement.objects.filter(name=item["name"])
            if achievement_qs.exists():
                achievement = achievement_qs.first()

                if (
                    (achievement.title != item["title"])
                    or (achievement.description != item["description"])
                    or (achievement.category != item["category"])
                    or (achievement.order != item["order"])
                ):
                    # Update the achievement
                    achievement.title = item["title"]
                    achievement.description = item["description"]
                    achievement.category = item["category"]
                    achievement.order = item["order"]

                    achievement.save()
                    self.stdout.write(
                        self.style.SUCCESS(f"- Updated: {achievement.name}")
                    )
                else:
                    self.stdout.write(f"- No changes for: {achievement.name}")
            else:
                Achievement.objects.create(
                    name=item["name"],
                    title=item["title"],
                    category=item["category"],
                    description=item["description"],
                    order=item["order"],
                )
                self.stdout.write(self.style.SUCCESS(f"- Created: {item['name']}"))

        self.stdout.write(
            self.style.SUCCESS("Successfully loaded data into Achievement")
        )

        # Collect all names from the data
        data_names = {item["name"] for item in data}

        # Find and delete entries that are not in the data
        deleted_entries = Achievement.objects.exclude(name__in=data_names)

        for entry in deleted_entries:
            self.stdout.write(self.style.WARNING(f"- Deleted: {entry.name}"))

        deleted_entries.delete()
