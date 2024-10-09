from django.utils import timezone
from django.db.models.functions import Round


def count_carries(user_done_carries, threshold):
    return user_done_carries.count() >= threshold

def count_position_carries(user_done_carries, position, threshold):
    return user_done_carries.filter(carry__position=position).count() >= threshold

def count_ring_carries(user_done_carries, threshold):
    return user_done_carries.filter(carry__rings=True).count() >= threshold

def count_difficulty_carries(general_ratings, difficulty, threshold):
    # Filter ratings based on the difficulty
    return general_ratings.annotate(
        rounded_difficulty=Round('difficulty')
    ).filter(
        rounded_difficulty=difficulty
    ).count() >= threshold


def count_reviews(user_ratings, threshold):
    return user_ratings.count() >= threshold

def count_account_days(user, threshold):
    # Get the current date
    current_date = timezone.now().date()
    
    # Calculate the number of days since the user joined
    days_since_joined = (current_date - user.date_joined.date()).days

    return days_since_joined >= threshold

def count_ruck_carries(user_done_carries, threshold):
    return user_done_carries.filter(carry__pass_ruck__gte=1).count() >= threshold

def count_dh_carries(user_done_carries, threshold):
    return user_done_carries.filter(carry__longtitle__icontains="Double Hammock").count() >= threshold

def count_cccb(user_done_carries, threshold):
    return user_done_carries.filter(carry__finish="CCCB").count() >= threshold

def count_shortie_carries(user_done_carries, threshold):
    # Filter ratings based on the difficulty and carry size
    return user_done_carries.filter(
        carry__size__gte=-5,  # Size greater than or equal to -5
        carry__size__lte=-2   # Size less than or equal to -2
    ).count() >= threshold

    return count >= threshold

def count_longie_carries(user_done_carries, threshold):
    # Filter ratings based on the difficulty and carry size
    return user_done_carries.filter(
        carry__size__gte=-1,  # Size greater than or equal to -5
        carry__size__lte=+2   # Size less than or equal to -2
    ).count() >= threshold

def count_pirates(user_done_carries, threshold):
    return user_done_carries.filter(carry__name__icontains="pirate").count() >= threshold


def count_toddler_prisoner(general_ratings, threshold):
    # Filter ratings based on the difficulty and carry size
    # Filter ratings based on the difficulty
    return general_ratings.filter(
        leaners__gte=4, 
        bigkids__gte=4,
        legstraighteners__gte=4   
    ).count() >= threshold


ACHIEVEMENT_FUNCTIONS = {
    'one_carry': (count_carries, 'done_carries', {'threshold': 1}),
    'five_carries': (count_carries, 'done_carries', {'threshold': 5}),
    'ten_carries': (count_carries, 'done_carries', {'threshold': 10}),
    'fifty_carries': (count_carries, 'done_carries', {'threshold': 50}),
    'one_back_carry': (count_position_carries, 'done_carries', {'threshold': 1, 'position': "back"}),
    'one_tandem': (count_position_carries, 'done_carries', {'threshold': 1, 'position': "tandem"}),
    'one_front': (count_position_carries, 'done_carries', {'threshold': 1, 'position': "front"}),
    'one_ring': (count_ring_carries, 'done_carries', {'threshold': 1}),
    'nine_rings': (count_ring_carries, 'done_carries', {'threshold': 9}),
    'twenty_rings': (count_ring_carries, 'done_carries', {'threshold': 20}),
    'one_review': (count_reviews, 'ratings', {'threshold': 1}),
    'five_reviews': (count_reviews, 'ratings', {'threshold': 5}),
    'ten_reviews': (count_reviews, 'ratings', {'threshold': 10}),
    'fifty_reviews': (count_reviews, 'ratings', {'threshold': 50}),
    'one_month': (count_account_days, 'time', {'threshold': 30}),
    'one_year': (count_account_days, 'time', {'threshold': 365}),
    'one_beginner_plus': (count_difficulty_carries, 'general_ratings', {'difficulty': 2, 'threshold': 1}),
    'one_intermediate': (count_difficulty_carries, 'general_ratings', {'difficulty': 3, 'threshold': 1}),
    'one_advanced': (count_difficulty_carries, 'general_ratings', {'difficulty': 4, 'threshold': 1}),
    'one_guru': (count_difficulty_carries, 'general_ratings', {'difficulty': 5, 'threshold': 1}),
    'ruck_star': (count_ruck_carries, 'done_carries', {'threshold': 10}),
    'dh_master': (count_dh_carries, 'done_carries', {'threshold': 10}),
    'ruck_rookie': (count_ruck_carries, 'done_carries', {'threshold': 3}),
    'dh_apprentice': (count_dh_carries, 'done_carries', {'threshold': 3}),
    'shortie_supreme': (count_shortie_carries, 'done_carries', {'threshold': 10}),
    'longie_supreme': (count_longie_carries, 'done_carries', {'threshold': 10}),
    'sweet_tooth': (count_cccb, 'done_carries', {'threshold': 10}),
    'pirates': (count_pirates, 'done_carries', {'threshold': 3}),
    'toddler_prisoner': (count_toddler_prisoner, 'general_ratings', {'threshold': 5}),
}

