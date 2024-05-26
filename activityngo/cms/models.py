from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from tinymce.models import HTMLField

from activityngo.custom_auth.models import BaseModel
from activityngo.utils.utils import (
    get_screenshot_tutorial_path,
    get_text_tutorial_path,
    get_user_manual_project_task_tutorial, how_to_complete_tasks_user_manual,
)


class CMS(BaseModel):
    """
    Define Cms Model to use Content Management System
    """

    META_KEY = (
        ("necessity", "Necessity"),
        ("aicte_rules", "AICTE Rules"),
        ("university_rules", "University Rules"),
        ("implementation_method", "Implementation Method"),
        ("our_team", "Our Team"),
        ("terms_and_conditions", "Terms and Conditions"),
        ("about_us", "About US"),
        ("privacy_policy", "Privacy Policy"),
        ("read_instructions", "Read Instructions"),
    )

    meta_key = models.CharField(max_length=32, choices=META_KEY, unique=True)
    slug = models.SlugField(_("slug"), max_length=64, null=True, blank=True)
    meta_value = HTMLField()

    def __str__(self):
        return f"{self.get_meta_key_display()}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.get_meta_key_display())
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "CMS"


class UserManual(BaseModel):
    # This filed for How to Buy Projects
    buy_projects_text_tutorial = models.FileField(
        _("text_tutorial"), upload_to=get_text_tutorial_path, null=True, blank=True
    )
    buy_projects_screenshot_tutorial = models.FileField(
        _("text_tutorial"),
        upload_to=get_screenshot_tutorial_path,
        null=True,
        blank=True,
    )
    buy_projects_video_url = models.URLField(_("video url"), max_length=251)

    # This filed for How to Complete Tasks
    complete_tasks_text_tutorial = models.FileField(
        _("text_tutorial"), upload_to=get_text_tutorial_path, null=True, blank=True
    )
    complete_tasks_screenshot_tutorial = models.FileField(
        _("text_tutorial"),
        upload_to=get_screenshot_tutorial_path,
        null=True,
        blank=True,
    )
    complete_tasks_video_url = models.URLField(_("video url"), max_length=251)

    # This filed for How to Resubmit Wrong Answers
    resubmit_wrong_answers_text_tutorial = models.FileField(
        _("text_tutorial"), upload_to=get_text_tutorial_path, null=True, blank=True
    )
    resubmit_wrong_answers_screenshot_tutorial = models.FileField(
        _("text_tutorial"),
        upload_to=get_screenshot_tutorial_path,
        null=True,
        blank=True,
    )
    resubmit_wrong_answers_video_url = models.URLField(_("video url"), max_length=251)

    #  User Manual Project Tasks Tutorial
    how_to_complete_task_1 = models.CharField(
        default="How To Complete Task 1", max_length=32
    )
    project_task_file_1 = models.FileField(
        _("Complete task 1 tutorial file"),
        null=True,
        blank=True,
        upload_to=get_user_manual_project_task_tutorial,
    )
    how_to_complete_task_2 = models.CharField(
        default="How To Complete Task 2", max_length=32
    )
    project_task_file_2 = models.FileField(
        _("Complete task 2 tutorial file"),
        null=True,
        blank=True,
        upload_to=get_user_manual_project_task_tutorial,
    )
    how_to_complete_task_3 = models.CharField(
        default="How To Complete Task 3", max_length=32
    )
    project_task_file_3 = models.FileField(
        _("Complete task 3 tutorial file"),
        null=True,
        blank=True,
        upload_to=get_user_manual_project_task_tutorial,
    )
    how_to_complete_task_4 = models.CharField(
        default="How To Complete Task 4", max_length=32
    )
    project_task_file_4 = models.FileField(
        _("Complete task 4 tutorial file"),
        null=True,
        blank=True,
        upload_to=get_user_manual_project_task_tutorial,
    )
    how_to_complete_task_5 = models.CharField(
        default="How To Complete Task 5", max_length=32
    )
    project_task_file_5 = models.FileField(
        _("Complete task 5 tutorial file"),
        null=True,
        blank=True,
        upload_to=get_user_manual_project_task_tutorial,
    )
    how_to_complete_task_6 = models.CharField(
        default="How To Complete Task 6", max_length=32
    )
    project_task_file_6 = models.FileField(
        _("Complete task 6 tutorial file"),
        null=True,
        blank=True,
        upload_to=get_user_manual_project_task_tutorial,
    )
    how_to_complete_task_7 = models.CharField(
        default="How To Complete Task 7", max_length=32
    )
    project_task_file_7 = models.FileField(
        _("Complete task 7 tutorial file"),
        null=True,
        blank=True,
        upload_to=get_user_manual_project_task_tutorial,
    )
    how_to_complete_task_8 = models.CharField(
        default="How To Complete Task 8", max_length=32
    )
    project_task_file_8 = models.FileField(
        _("Complete task 8 tutorial file"),
        null=True,
        blank=True,
        upload_to=get_user_manual_project_task_tutorial,
    )
    how_to_complete_task_9 = models.CharField(
        default="How To Complete Task 9", max_length=32
    )
    project_task_file_9 = models.FileField(
        _("Complete task 9 tutorial file"),
        null=True,
        blank=True,
        upload_to=get_user_manual_project_task_tutorial,
    )
    how_to_complete_task_10 = models.CharField(
        default="How To Complete Task 10", max_length=32
    )
    project_task_file_10 = models.FileField(
        _("Complete task 10 tutorial file"),
        null=True,
        blank=True,
        upload_to=get_user_manual_project_task_tutorial,
    )
    how_to_complete_task_11 = models.CharField(
        default="How To Complete Task 11", max_length=32
    )
    project_task_file_11 = models.FileField(
        _("Complete task 11 tutorial file"),
        null=True,
        blank=True,
        upload_to=get_user_manual_project_task_tutorial,
    )

    # Other User Manual
    other_text_tutorial = models.FileField(
        _("text_tutorial"), upload_to=get_text_tutorial_path, null=True, blank=True
    )
    other_screenshot_tutorial = models.FileField(
        _("text_tutorial"),
        upload_to=get_screenshot_tutorial_path,
        null=True,
        blank=True,
    )
    other_projects_video_url = models.URLField(
        _("video url"), max_length=251, null=True, blank=True
    )

    # How to complete task
    how_to_complete_tasks_20_points = models.FileField(
        _("text_tutorial"), upload_to=how_to_complete_tasks_user_manual, null=True, blank=True
    )
    how_to_complete_tasks_10_points = models.FileField(
        _("text_tutorial"), upload_to=how_to_complete_tasks_user_manual, null=True, blank=True
    )
    how_to_complete_tasks_05_points = models.FileField(
        _("text_tutorial"), upload_to=how_to_complete_tasks_user_manual, null=True, blank=True
    )

    # class UserManualProjectTasksTutorial(BaseModel):
    #     title = models.CharField(_("Title"), max_length=64, unique=True)
    #     file = models.FileField(_("Complete task tutorial"), null=True, blank=True,
    #                             upload_to=get_user_manual_project_task_tutorial)

    @property
    def task_1(self):
        return {
            "project_task_file_1": self.how_to_complete_task_1,  # File name
            "url": (
                self.project_task_file_1.url if self.project_task_file_1 else ""
            ),  # URL to access the file
        }

    @property
    def task_2(self):
        return {
            "project_task_file_2": self.how_to_complete_task_2,  # File name
            "url": (
                self.project_task_file_2.url if self.project_task_file_2 else ""
            ),  # URL to access the file
        }

    @property
    def task_3(self):
        return {
            "project_task_file_3": self.how_to_complete_task_3,  # File name
            "url": (
                self.project_task_file_3.url if self.project_task_file_3 else ""
            ),  # URL to access the file
        }

    @property
    def task_4(self):
        return {
            "project_task_file_4": self.how_to_complete_task_4,  # File name
            "url": (
                self.project_task_file_4.url if self.project_task_file_4 else ""
            ),  # URL to access the file
        }

    @property
    def task_5(self):
        return {
            "project_task_file_5": self.how_to_complete_task_5,  # File name
            "url": (
                self.project_task_file_5.url if self.project_task_file_5 else ""
            ),  # URL to access the file
        }

    @property
    def task_6(self):
        return {
            "project_task_file_6": self.how_to_complete_task_6,  # File name
            "url": (
                self.project_task_file_6.url if self.project_task_file_6 else ""
            ),  # URL to access the file
        }

    @property
    def task_7(self):
        return {
            "project_task_file_7": self.how_to_complete_task_7,  # File name
            "url": (
                self.project_task_file_7.url if self.project_task_file_7 else ""
            ),  # URL to access the file
        }

    @property
    def task_8(self):
        return {
            "project_task_file_8": self.how_to_complete_task_8,  # File name
            "url": (
                self.project_task_file_8.url if self.project_task_file_8 else ""
            ),  # URL to access the file
        }

    @property
    def task_9(self):
        return {
            "project_task_file_9": self.how_to_complete_task_9,  # File name
            "url": (
                self.project_task_file_9.url if self.project_task_file_9 else ""
            ),  # URL to access the file
        }

    @property
    def task_10(self):
        return {
            "project_task_file_10": self.how_to_complete_task_10,  # File name
            "url": (
                self.project_task_file_10.url if self.project_task_file_10 else ""
            ),  # URL to access the file
        }

    @property
    def task_11(self):
        return {
            "project_task_file_11": self.how_to_complete_task_11,  # File name
            "url": (
                self.project_task_file_11.url if self.project_task_file_11 else ""
            ),  # URL to access the file
        }


class FAQ(BaseModel):
    question = models.CharField(max_length=2064)
    answers = models.TextField((_("answers")))


class ContactUS(BaseModel):
    phone = PhoneNumberField(
        _("Mobile Number"),
    )
    whatsapp_phone = PhoneNumberField(
        _("Whatspapp Mobile Number"), null=True, blank=True
    )
    visit_at = models.TextField(_("visit at"))
    filled_form_to_be_emailed_to = models.EmailField(_("Email"))


class MyCartInstructions(BaseModel):
    instructions = models.TextField(_("My Cart Instructions"))


class ContactUSForm(BaseModel):
    """
    Define ContactUS Model to use ContactUS Details Store
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="contact_form_user",
    )
    firstname = models.CharField(_("firstName"), max_length=64)
    lastname = models.CharField(_("lastName"), max_length=64)
    email = models.CharField(_("Email"), max_length=128)
    subject = models.CharField(_("Subject"), max_length=128)
    description = models.TextField(_("Description"))

    class Meta:
        verbose_name = _("ContactUS")
        verbose_name_plural = _("ContactUS")

    def __str__(self):
        return f"{self.email}"
