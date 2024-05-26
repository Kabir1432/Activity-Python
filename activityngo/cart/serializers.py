from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from activityngo.cart.models import Cart
from activityngo.order.models import OrderDetail
from activityngo.project.serializers import ProjectListSerializer


class CartSerializer(serializers.ModelSerializer):
    project_set = ProjectListSerializer(
        source="project",
        read_only=True,
    )

    class Meta:
        model = Cart
        fields = ["id", "user", "number_of_points", "project", "project_set"]
        extra_kwargs = {
            "number_of_points": {"required": True},
            "project": {"required": True},
        }

    def validate(self, attrs):
        user = self.context["request"].user
        instance = self.instance
        current_project = attrs["project"]
        if instance is None:
            # Object is being created
            if Cart.objects.filter(
                Q(project=current_project)
                | Q(project__category=current_project.category),
                user=user,
            ).exists():
                raise ValidationError(_("Sorry that item already exists in cart."))

        else:
            # Object is being updated
            if Cart.objects.filter(
                project=current_project, user=instance.user
            ).exists():
                if not attrs["project"] == instance.project:
                    raise ValidationError(_("Sorry that item already exists in cart."))
        if OrderDetail.objects.filter(
            (
                Q(project=current_project)
                | Q(project__category=current_project.category)
            ),
            Q(is_expire=False) | Q(is_complete=True),
            order__user=user,order__is_temp_order=False
        ).exists():
            raise ValidationError(_("This project you already purchased."))

        return super().validate(attrs)

    @transaction.atomic
    def create(self, validated_data):
        user = self.context.get("user") or self.context.get("request").user
        validated_data["user"] = user
        return super().create(validated_data)
