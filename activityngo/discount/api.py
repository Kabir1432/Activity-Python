# from rest_framework.viewsets import ModelViewSet
from django.db.models import BooleanField, Case, Count, F, Q, Subquery, When
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from activityngo.discount.models import Discount, DiscountUsage
from activityngo.discount.serializers import (DiscountSerializer,
                                              DiscountUsageSerializer)
from activityngo.utils.permissions import IsAPIKEYAuthenticated


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    ordering_fields = ["discount_name", ]

    # PLEASE DO NOT REMOVE ANY COMMENT CODE FROM BELOW
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.user_type == "student":
            # used_discount_ids = DiscountUsage.objects.filter(user=user).values('discount_id')
            # .exclude(id__in=Subquery(used_discount_ids))
            queryset = queryset.filter(is_active=True)
            discount_type_q = (
                Q(type_discount="general_discount")
                | Q(type_discount="individual_discount", user=user)
                | Q(
                    type_discount="batch_discount",
                    college=user.student_details.college,
                    university=user.student_details.university,
                    degree=user.student_details.degree,
                    branch=user.student_details.branch,
                    batch=user.student_details.batch,
                )
            )
            # Work continue from here discount query issue
            # PLEASE DO NOT REMOVE ANY CODE FROM HERE
            queryset = (
                queryset.annotate(
                    user_usage_count=Count(
                        "discount_usage", filter=Q(discount_usage__user=user)
                    ),
                    usage_limit_reached=Case(
                        When(
                            user_usage_count__gte=F("usage_limit_per_membership_id"),
                            then=True,
                        ),
                        default=False,
                        output_field=BooleanField(),
                    ),
                )
                .exclude(usage_limit_reached=True)
                .filter(discount_type_q, discount_limit_reached=False)
            )
            # PLEASE DO NOT REMOVE ANY COMMENT CODE FROM BELOW
            # queryset = queryset.annotate(
            #     user_usage_count=Count('discount_usage', filter=Q(discount_usage__user=self.request.user)),
            #     usage_limit_reached=Case(
            #         When(user_usage_count__gte=F('usage_limit_per_membership_id'), then=True),
            #         default=False,
            #         output_field=BooleanField()  # Use BooleanField here
            #     )
            # )
            # queryset.filter(usage_limit_reached=False)
            # queryset = queryset.filter(
            #     Q(type_discount='general_discount') |
            #     Q(type_discount='individual_discount', user=user)
            # ).filter(discount_limit_reached=False)
            # PLEASE DO NOT REMOVE ANY COMMENT CODE FROM BELOW
            # queryset.filter(discount_limit_reached=False)
            # eligible_discounts = queryset.exclude(
            #     discountusage__user=user,
            #     discountusage__usage_count__gte=models.F('max_usage_per_user')
            # )
            # PLEASE DO NOT REMOVE ANY COMMENT CODE FROM BELOW
            # eligible_discounts = []
            # for discount in Discount.objects.all():
            #     existing_usage = DiscountUsage.objects.filter(user=user, discount=discount).first()
            #     usage_count = eligible_discounts = Discount.objects.exclude(
            #             discountusage__user=user,
            #             discountusage__usage_count__gte=models.F('max_usage_per_user')
            #         )
            #
            #     if not existing_usage or existing_usage.usage_count < discount.max_usage_per_user:
            #         eligible_discounts.append(discount.id)
            # queryset = queryset.filter(id__in=eligible_discounts)
        return queryset.order_by("-create_time")


class DiscountUsageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DiscountUsage.objects.all()
    serializer_class = DiscountUsageSerializer
    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        "discount",
    ]
    # filterset_fields = ['status_of_payment', ]
    # search_fields = ('user__email', 'user__student_details__student_membership_id', 'user__phone',)
