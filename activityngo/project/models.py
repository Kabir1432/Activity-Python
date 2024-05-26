from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from django.conf import settings
from activityngo.college.models import College, CollegeDegree, DegreeBranch
from activityngo.custom_auth.models import BaseModel
from activityngo.entities.models import (Batches, Degree, ProjectCategory,
                                         ProjectType, State)
from activityngo.ngo.models import Ngo
from activityngo.university.models import University
from activityngo.utils.utils import get_issue_of_certificate_path


# Create your models here.
class Project(BaseModel):  # main Project table
    # POINT = Choices(
    #     ("points_20", "20 Points"),
    #     ("points_10", "10 Points"),
    #     ("points_05", "05 Points"),
    # )
    # number_of_points = models.CharField(max_length=10, choices=POINT, )
    # number_of_hours = models.IntegerField(_('Number of Hours'))
    franchise_ngo_name = models.ForeignKey(
        Ngo, on_delete=models.SET_NULL, null=True, related_name="ngo_projects"
    )
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.SET_NULL,
        related_name="project_category_details",
        null=True,
        blank=True,
    )
    title = models.CharField(_("Project Title"), max_length=256)
    type = models.ForeignKey(
        ProjectCategory,
        on_delete=models.SET_NULL,
        related_name="project_type_details",
        null=True,
        blank=True,
    )
    expire_duration_in_days_by_students = models.IntegerField(
        _("Expire Duration in Days (Project Completion by Students)"),
    )
    expire_duration_in_days_by_evaluate = models.IntegerField(
        _("Expire Duration in Days (Admin to Evaluate and Generate Report)"),
    )
    subscription_price = models.DecimalField(
        _("Subscription Price"),
        max_digits=10,
        decimal_places=6,
        null=True,
        blank=True
    )
    minimum_number_of_days = models.IntegerField(_("Minimum Number of Days"), null=True, blank=True, )
    gst_inclusive = models.FloatField(
        _("GST Inclusive / Exclusive in Project Price"), max_length=10
    )
    price_of_20_point = models.DecimalField(
        _("Price of 20 point"), max_digits=10, decimal_places=2, default=0
    )
    price_of_10_point = models.DecimalField(
        _("Price of 10 point"), max_digits=10, decimal_places=2, default=0
    )
    price_of_05_point = models.DecimalField(
        _("Price of 05 point"), max_digits=10, decimal_places=2, default=0
    )
    days_of_20_point = models.PositiveIntegerField(_("Hours of 20 point"), default=0)
    days_of_10_point = models.PositiveIntegerField(_("Hours of 10 point"), default=0)
    days_of_05_point = models.PositiveIntegerField(_("Hours of 05 point"), default=0)

    # Manage add project related Fields is Fulfill
    is_basic_details = models.BooleanField(_("Basic Details"), default=False)
    is_project_details = models.BooleanField(_("Project Details"), default=False)
    is_task_summary = models.BooleanField(_("Task Summary"), default=False)
    is_task_1 = models.BooleanField(_("Task 1"), default=False)
    is_task_2 = models.BooleanField(_("Task 2"), default=False)
    is_task_3 = models.BooleanField(_("Task 3"), default=False)
    is_task_4 = models.BooleanField(_("Task 4"), default=False)
    is_task_5 = models.BooleanField(_("Task 5"), default=False)
    is_task_6 = models.BooleanField(_("Task 6"), default=False)
    is_task_7 = models.BooleanField(_("Task 7"), default=False)
    is_task_8 = models.BooleanField(_("Task 8"), default=False)
    is_task_9 = models.BooleanField(_("Task 9"), default=False)
    is_task_10 = models.BooleanField(_("Task 10"), default=False)

    # handle project visible
    is_visible = models.BooleanField(_('Is Visible'), default=False)


class ProjectDetails(BaseModel):
    MODE = Choices(
        ("online", "Online"),
        ("offline", "Offline"),
        ("online_and_offline", "Online and Offline"),
    )
    project = models.OneToOneField(
        Project, on_delete=models.CASCADE, related_name="projects_details"
    )
    mode = models.CharField(
        max_length=20,
        choices=MODE,
    )
    beneficiary_in_society = models.CharField(
        _("beneficiary_in_society"), max_length=300
    )
    number_of_tasks = models.IntegerField(_("Number of Tasks"), null=True)
    field_visit_mandation = models.CharField(
        _("Field Visit Mandation"), max_length=128,
        null=True, blank=True
    )
    scheduling_field_visit_by_ngo = models.BooleanField(
        _("Scheduling Field Visit by NGO"), default=True
    )
    can_students_visit_field_by_themselves = models.BooleanField(
        _("Can students visit field by themselves"), default=True
    )
    places_that_can_be_considered_for_field_visit = models.CharField(
        _("Places that can be considered for field visit"), null=True, max_length=512
    )
    issue_of_certificate = models.CharField(
        _("Issue of Certificate"), null=True, max_length=512
    )
    issue_of_report = models.CharField(_("Issue of Report"), null=True, max_length=512)
    mode_of_receiving_report_and_certificate = models.CharField(
        _("Mode of Receiving Report & Certificate"), null=True, max_length=512
    )


class StudentFeedback(BaseModel):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="projects_feedback"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="project_feedback_users",
    )
    feedback = models.CharField(max_length=2048)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )


class SpecialPower(BaseModel):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="project_special_power"
    )
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name="state_special_power"
    )
    college = models.ForeignKey(
        College, on_delete=models.CASCADE, related_name="college_special_power"
    )
    university = models.ForeignKey(
        University, on_delete=models.CASCADE, related_name="university_special_power"
    )
    degree = models.ForeignKey(
        CollegeDegree, on_delete=models.CASCADE, related_name="degree_special_power"
    )
    batch = models.ForeignKey(
        DegreeBranch, on_delete=models.CASCADE, related_name="batch_special_power"
    )

# class ProjectPrice(BaseModel):
#     POINT = Choices(
#         ("points_20", "20 Points"),
#         ("points_10", "10 Points"),
#         ("points_05", "05 Points"),
#     )
#     number_of_points = models.CharField(max_length=10, choices=POINT, default=POINT.points_20)
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_project_price")
#     price = models.DecimalField(_('Price'), max_digits=10, decimal_places=2)
#     number_of_hour = models.IntegerField(_('Number of Hours'))
#
#     class Meta:
#         verbose_name = _('Project Price')
#         verbose_name_plural = _('Project Price')
#         unique_together = ('number_of_points', 'project')
