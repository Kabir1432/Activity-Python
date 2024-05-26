import os
import uuid
from datetime import datetime
from django.conf import settings
from django.db import models
from django.db.models import Subquery
from django.utils import timezone


def get_user_photo_random_filename(instance, filename):
    extension = os.path.splitext(filename)[1]
    return "{}/{}{}".format(settings.USER_PHOTOS, uuid.uuid4(), extension)


class SQCount(Subquery):
    template = "(SELECT count(1) FROM (%(subquery)s) _count)"
    output_field = models.IntegerField()


def make_active(modeladmin, request, queryset):
    for item in queryset:
        item.is_active = True
        item.save()


def make_inactive(modeladmin, request, queryset):
    for item in queryset:
        item.is_active = False
        item.save()


def get_llp_Certificate_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    file = os.path.splitext(filename)[0]
    return "{}/{}{}".format(settings.LLP_CERTIFICATE, file, extension)


def get_student_complaint_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    return "{}/{}{}".format(settings.STUDENT_COMPLAINT, uuid.uuid4(), extension)


def get_order_invoice_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    return "{}/{}{}".format(settings.ORDER_INVOICE, uuid.uuid4(), extension)


def get_activity_report_file_path(instance, filename):
    try:
        extension = os.path.splitext(filename)[1]
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # Current timestamp
        return "{}/{}{}".format(settings.ACTIVITY_REPORT_FILE,
                                f"{instance.order.user.student_details.id_number}_{instance.number_of_points}_{timestamp}",
                                extension)
    except Exception as e:
        print("error is-->", e)


def get_upload_photo_question_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    return "{}/{}{}".format(settings.UPLOAD_PHOTO_QUESTION, uuid.uuid4(), extension)


def get_website_cover_photo_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    return "{}/{}{}".format(settings.WEBSITE_COVER_PHOTO, uuid.uuid4(), extension)


# def get_llp_Certificate_path(instance, filename):
#     extension = os.path.splitext(filename)[1]
#     return '{}/{}{}'.format(settings.GSTIN_DOCUMENT, uuid.uuid4(), extension)


def get_gstin_document_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    file = os.path.splitext(filename)[0]
    # return "{}/{}{}".format(settings.GSTIN_DOCUMENT, uuid.uuid4(), extension)
    return "{}/{}{}".format(settings.GSTIN_DOCUMENT, file, extension)


def get_text_tutorial_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    return "{}/{}{}".format(settings.TEXT_TUTORIAL, uuid.uuid4(), extension)


def how_to_complete_tasks_user_manual(instance, filename):
    extension = os.path.splitext(filename)[1]
    return "{}/{}{}".format(settings.HOW_TO_COMPLETE_TASKS_USER_MANUAL, uuid.uuid4(), extension)


def get_screenshot_tutorial_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    return "{}/{}{}".format(settings.SCREENSHOT_TUTORIAL, uuid.uuid4(), extension)


def get_udhyam_aadhar_document_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    file = os.path.splitext(filename)[0]
    return "{}/{}{}".format(settings.UDHYAM_AADHAR_DOCUMENT, file, extension)


def get_dpiit_document_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    file = os.path.splitext(filename)[0]
    return "{}/{}{}".format(settings.DPIIT_DOCUMENT, file, extension)


def get_pan_card_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    file = os.path.splitext(filename)[0]
    return "{}/{}{}".format(settings.PAN_CARD, file, extension)


def get_tan_card_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    file = os.path.splitext(filename)[0]
    return "{}/{}{}".format(settings.TAN_CARD, file, extension)


def get_logo_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    file = os.path.splitext(filename)[0]
    return "{}/{}{}".format(settings.LOGO, file, extension)


def get_ngo_office_photo_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    return "{}/{}{}".format(settings.NGO_OFFICE_PHOTO, uuid.uuid4(), extension)


def get_seal_and_sign_of_trustee_3_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    return "{}/{}{}".format(
        settings.SEAL_AND_SIGN_OF_TRUSTEE_3, uuid.uuid4(), extension
    )


def get_franchise_certificate_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    return "{}/{}{}".format(settings.FRANCHISE_CERTIFICATE, uuid.uuid4(), extension)


def get_trustee_1_Aadhar_card_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    file = os.path.splitext(filename)[0]
    return "{}/{}{}".format(settings.TRUSTEE_1_AADHAR_CARD, file, extension)


def get_trustee_2_aadhar_card_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    file = os.path.splitext(filename)[0]
    return "{}/{}{}".format(settings.TRUSTEE_2_AADHAR_CARD, file, extension)


def get_cancelled_cheque_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    file = os.path.splitext(filename)[0]
    return "{}/{}{}".format(settings.CANCELLED_CHEQUE, file, extension)


def get_seal_and_sign_of_director_1_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    file = os.path.splitext(filename)[0]
    return "{}/{}{}".format(
        settings.SEAL_AND_SIGN_OF_DIRECTOR_1, file, extension
    )


def get_seal_and_sign_of_director_2_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    file = os.path.splitext(filename)[0]
    return "{}/{}{}".format(
        settings.SEAL_AND_SIGN_OF_DIRECTOR_2, file, extension
    )


def get_issue_of_certificate_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    return "{}/{}{}".format(settings.ISSUE_OF_CERTIFICATE, uuid.uuid4(), extension)


def get_trust_deed(instance, filename):
    extension = os.path.splitext(filename)[1]
    return "{}/{}{}".format(settings.TRUST_DEED, uuid.uuid4(), extension)


def set_otp_reset_expiration_time():
    return timezone.now() + timezone.timedelta(minutes=5)


def get_walkthrought_random_filename(instance, filename):
    extension = os.path.splitext(filename)[1]
    return "{}/{}{}".format(settings.WALKTHROUGHT_MEDIA, uuid.uuid4(), extension)


def get_student_qr_code_verification_filename(instance, filename):
    extension = os.path.splitext(filename)[1]
    return "{}/{}{}".format(settings.STUDENT_QR_CODE_VERIFICATION, uuid.uuid4(), extension)


def get_student_pie_chart_filename(instance, filename):
    extension = os.path.splitext(filename)[1]
    return "{}/{}{}".format(settings.STUDENT_ACTIVITY_PIE_CHART, uuid.uuid4(), extension)


def get_student_activity_certificate_file_filename(instance, filename):
    extension = os.path.splitext(filename)[1]
    return "{}/{}{}".format(settings.STUDENT_ACTIVITY_CERTIFICATE, uuid.uuid4(), extension)


def get_student_activity_certificate_page_1_to_5_file_filename(instance, filename):
    extension = os.path.splitext(filename)[1]
    return "{}/{}{}".format(settings.STUDENT_ACTIVITY_CERTIFICATE_PAGE_1_TO_5, uuid.uuid4(), extension)


def get_student_activity_chapters_file_filename(instance, filename):
    extension = os.path.splitext(filename)[1]
    return "{}/{}{}".format(settings.STUDENT_ACTIVITY_CHAPTERS, uuid.uuid4(), extension)


def get_complaint_photo_random_filename(instance, filename):
    extension = os.path.splitext(filename)[1]
    return "{}/{}{}".format(settings.COMPLAINT_MEDIA, uuid.uuid4(), extension)


def get_upload_thumbnail_video_question_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    return "{}/{}{}".format(settings.VIDEO_QUESTION_THUMBNAIL, uuid.uuid4(), extension)


def get_user_manual_project_task_tutorial(instance, filename):
    extension = os.path.splitext(filename)[1]
    return "{}/{}{}".format(
        settings.USER_MANUAL_PROJECT_TASK_TUTORIAL, uuid.uuid4(), extension
    )
