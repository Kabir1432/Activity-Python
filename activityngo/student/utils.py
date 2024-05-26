from django.utils import timezone
from spellchecker import SpellChecker
from activityngo.student import models


def generate_complaint_number():
    latest_entry = models.Complaints.objects.order_by("-complaint_number").first()

    if latest_entry:
        if int(latest_entry.complaint_number) < 999999:
            incremented = int(latest_entry.complaint_number) + 1
            formatted_numeric_part = str(incremented).zfill(6)
        else:
            formatted_numeric_part = False
        new_complaint_number = formatted_numeric_part
    else:
        new_complaint_number = "000001"

    return new_complaint_number


def generate_student_membership_id_code():
    latest_entry = models.StudentDetails.objects.order_by(
        "-student_membership_id"
    ).first()
    if latest_entry and latest_entry.student_membership_id:
        numeric_part = int(latest_entry.student_membership_id[3:])

        if numeric_part < 999999:
            incremented_numeric_part = numeric_part + 1
            formatted_numeric_part = str(incremented_numeric_part).zfill(6)
        else:
            formatted_numeric_part = False
        new_franchise_code = "APS" + formatted_numeric_part
    else:
        new_franchise_code = "APS000001"

    return new_franchise_code


def set_otp_expiration_time():
    return timezone.now() + timezone.timedelta(minutes=5)


# def correct_spelling(input_text):
#     spell = SpellChecker()
#
#     # Split the input text into words
#     words = input_text.split()
#
#     # Find misspelled words
#     misspelled_words = spell.unknown(words)
#
#     corrections = {}
#     for word in misspelled_words:
#         # Get the most likely correct spelling
#         corrections[word] = spell.correction(word)
#
#     return corrections
