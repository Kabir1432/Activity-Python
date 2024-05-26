from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from datetime import datetime
from activityngo.college.models import College, CollegeDegree, DegreeBranch, BranchBatches
from activityngo.custom_auth.models import BaseModel
from activityngo.discount.utils import generate_discount_code
from activityngo.entities.models import Batches, Branch, Degree, State
from activityngo.university.models import University


# Create your models here.
class Discount(BaseModel):
    TYPE_DISCOUNT = Choices(
        ("individual_discount", "Individual Discount"),
        ("general_discount", "General Discount"),
        ("batch_discount", "Batch Discount"),
    )
    discount_name = models.CharField(_("discount_name"), max_length=60)
    description = models.CharField(
        _("Description"), max_length=256, null=True, blank=True
    )
    code = models.CharField(
        _("Code"), max_length=30, unique=True, blank=True, null=True
    )
    type_discount = models.CharField(
        max_length=30,
        choices=TYPE_DISCOUNT,
    )
    discount_price_project_type_20 = models.DecimalField(
        _("Discount price project type 20"), max_digits=10, decimal_places=2
    )
    discount_price_project_type_10 = models.DecimalField(
        _("Discount price project type 10"), max_digits=10, decimal_places=2
    )
    discount_price_project_type_05 = models.DecimalField(
        _("Discount price project type 05"), max_digits=10, decimal_places=2
    )
    conjunction_discount = models.BooleanField(_("Conjunction discount"))
    usage_limit = models.PositiveIntegerField(_("Usage limit"))
    usage_limit_per_membership_id = models.PositiveIntegerField(
        _("Usage limit per membership id")
    )
    usage_limit_per_project_subscription = models.PositiveIntegerField(
        _("Usage Limit per Project Subscription")
    )
    current_discount_usage_count = models.IntegerField(
        _("current_discount_usage_count"), default=0
    )
    discount_limit_reached = models.BooleanField(
        _("discount limit reached"), default=False
    )
    active_date = models.DateTimeField()
    expire_date = models.DateTimeField()
    user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
    )
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='discount_college_states',
                              verbose_name=_("Student College State"), null=True, blank=True)
    college = models.ForeignKey(
        College,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="student_college_discount",
        verbose_name=_("Student College"),
    )
    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="student_university_discount",
        verbose_name=_("Student University"),
    )
    degree = models.ForeignKey(
        CollegeDegree,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="student_degree_discount",
        verbose_name=_("Student Degree"),
    )
    branch = models.ForeignKey(
        DegreeBranch,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="student_branch_discount",
        verbose_name=_("Student Branch"),
    )
    batch = models.ForeignKey(
        BranchBatches,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="student_batch_discount",
        verbose_name=_("Student Batch"),
    )
    is_active = models.BooleanField(default=False)

    # @property
    # def user_usage_count(self, user):
    #     return self.discount_usage.filter(user=user).count()

    def save(self, *args, **kwargs):
        if self.type_discount != "batch_discount":
            self.college = (
                self.university
            ) = self.degree = self.batch = self.branch = None

        if not self.code:
            code = generate_discount_code(10)

            while self._meta.model._default_manager.filter(code=code).exists():
                code = generate_discount_code(10)

            self.code = code
        if self.active_date.date() <= datetime.now().date() <= self.expire_date.date():
            self.is_active = True
        else:
            self.is_active = False
        return super(Discount, self).save(*args, **kwargs)


class DiscountUsage(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    discount = models.ForeignKey(
        Discount, on_delete=models.CASCADE, related_name="discount_usage"
    )
    used_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ('user', 'discount')

    def __str__(self):
        return (
            f"{self.user.username} used {self.discount.discount_name} on {self.used_at}"
        )
