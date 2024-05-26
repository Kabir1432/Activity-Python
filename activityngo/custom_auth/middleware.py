# middleware.py
import datetime
from datetime import datetime, time

import pytz
from django.http import JsonResponse
from django.utils import timezone

from .models import UserActivity


class UpdateUserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            try:
                user_activity, created = UserActivity.objects.get_or_create(
                    user=request.user
                )
                user_activity.last_activity = timezone.now()
                user_activity.save()
            except:
                pass

        return response


# custom_middleware.py


class TimeRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Get the current time
        indian_timezone = pytz.timezone("Asia/Kolkata")
        # Get the current time in the Indian time zone
        current_time_in_india = datetime.now(indian_timezone).time()
        # Define your time restriction window (from 14:30 to 00:15, the next day)
        start_time = time(23, 30)
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Update start_time based on user_type
            start_time = (
                time(23, 30) if request.user.user_type != "student" else time(23, 15)
            )
        end_time = time(12, 15)
        # Check if the current time is within the restriction window
        if start_time <= current_time_in_india <= end_time:
            response_data = {"message": "API access is restricted during this time."}
            return JsonResponse(response_data, status=403)

        # Allow the request to pass through if it's outside the restriction window

        return response

        # Allow the request to pass through if it's outside the restriction window
