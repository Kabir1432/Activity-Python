from rest_framework.response import Response
from rest_framework.views import APIView

from activityngo.utils.permissions import IsAPIKEYAuthenticated
from activityngo.utils.sendgrid_email_send import send_email_download_student


class SendEmailToDownload(APIView):
    permission_classes = []

    def post(self, request):
        # Get email address from request data
        email = request.data.get("email")
        first_name = request.data.get("first_name")

        if email:
            try:
                first_name = first_name if first_name else "Student"
                send_email_download_student(email, first_name)
                return Response({"message": "Email sent successfully"}, status=200)
            except Exception as e:
                return Response({"message": str(e)}, status=500)
        else:
            return Response(
                {"message": "Email and first name are required fields"}, status=400
            )
