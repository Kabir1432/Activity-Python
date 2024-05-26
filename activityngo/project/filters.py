from django.db.models import Avg
from rest_framework import filters


class HighestRatingFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        highest_rating_param = request.query_params.get("highest_rating")

        if highest_rating_param:
            try:
                # Parse the highest_rating parameter as a float
                highest_rating = float(highest_rating_param)
            except ValueError:
                # Handle the case where the parameter is not a valid float
                return queryset

            # Annotate the queryset with the average rating for each project
            queryset = queryset.annotate(
                average_rating=Avg("projects_feedback__rating")
            )

            # Filter the queryset to include only projects with an average rating greater than or equal to highest_rating
            queryset = queryset.filter(average_rating__gte=highest_rating)

        return queryset
