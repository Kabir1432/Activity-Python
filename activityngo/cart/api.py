from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from activityngo.cart.models import Cart
from activityngo.cart.serializers import CartSerializer
from activityngo.utils.permissions import IsAPIKEYAuthenticated, IsStudentUser
from django.db.models import Case, DecimalField, ExpressionWrapper, F, Sum, Value, When


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated]

    def get_permissions(self):
        if self.action == "create":
            # Use the custom permission class for creating orders
            return [IsAuthenticated(), IsAPIKEYAuthenticated(), IsStudentUser()]
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.user_type == "student":
            return queryset.filter(user=user, project__is_active=True).order_by("-create_time")
        return queryset.order_by("-create_time")

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        # total_cart_price = Cart.objects.filter(user=self.request.user).aggregate(
        #     total=Sum("project__subscription_price")
        # )
        point_to_field_mapping = {
            "points_20": "price_of_20_point",
            "points_10": "price_of_10_point",
            "points_05": "price_of_05_point",
        }

        total_cart_price = Cart.objects.filter(user=self.request.user, project__is_active=True).aggregate(
            total_price=Sum(
                Case(
                    *[When(number_of_points=point, then=F("project__" + field_name)) for point, field_name in
                      point_to_field_mapping.items()],
                    default=Value(0),
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                )
            )
        )
        response.data.update({"total_cart_price": total_cart_price.get("total_price")})
        return response
