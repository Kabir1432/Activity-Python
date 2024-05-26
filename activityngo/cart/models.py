from django.conf import settings
from django.db import models
from model_utils import Choices

from activityngo.custom_auth.models import BaseModel
from activityngo.project.models import Project


class Cart(BaseModel):
    POINT = Choices(
        ("points_20", "20 Points"),
        ("points_10", "10 Points"),
        ("points_05", "05 Points"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="cart_users",
    )
    number_of_points = models.CharField(
        max_length=10,
        choices=POINT,
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="product_cart_items"
    )
