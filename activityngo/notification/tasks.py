from activityngo.custom_auth.models import ApplicationUser
from activityngo.notification.models import Notification
from activityngo.notification.serializer import SendNotificationSerializer
from activityngo.utils.sendgrid_email_send import send_notification_email
import json
from activityngo.notification.FCM_manager import send_to_topic, sendPush
from activityngo.taskapp import app


@app.task
def send_notification_to_individual_student(student_id, admin_id, request_data):
    student = ApplicationUser.objects.get(pk=student_id)
    admin = ApplicationUser.objects.get(pk=admin_id)
    notification = Notification.objects.create(
        receiver=student,
        sender=admin,
        tag=request_data.get("tag"),
        title="Admin Notification",
        message=request_data.get("message"),
    )

    # PushNotification.send_notification_to_individual_student(notification)

    # send email
    send_notification_email(student, notification.title, notification.message)

    data = {
        "notification_id": str(notification.id),
        "tag": str(notification.tag),
        # "model_id": str(sender_user.id),
        "title": str(notification.title),
        "body": str(notification.message),
    }

    response = data.copy()
    response["custom_data"] = json.dumps(
        {
            "tag": str(notification.tag),
            "title": str(notification.title),
            "body": str(notification.message),
        }
    )
    if student.device_token:
        sendPush(
            notification.title,
            notification.message,
            student.device_token,
            response,
        )


@app.task
def send_notification_to_group_of_students(admin_id, request_data, unique_users):
    admin = ApplicationUser.objects.get(pk=admin_id)
    notification = Notification.objects.create(
        sender=admin,
        tag=request_data.get("tag"),
        title="Admin Notification",
        message=request_data.get("message"),
    )

    for students in unique_users:
        student = ApplicationUser.objects.filter(id=students).first()
        notification.group_of_student.add(student)

        # send email
        send_notification_email(student, notification.title, notification.message)

        data = {
            "notification_id": str(notification.id),
            "tag": str(notification.tag),
            # "model_id": str(sender_user.id),
            "title": str(notification.title),
            "body": str(notification.message),
        }

        response = data.copy()
        response["custom_data"] = json.dumps(
            {
                "tag": str(notification.tag),
                "title": str(notification.title),
                "body": str(notification.message),
            }
        )
        if student.device_token:
            sendPush(
                notification.title,
                notification.message,
                student.device_token,
                response,
            )


@app.task
def send_notification_to_all_students(admin_id, request_data, unique_users):
    admin = ApplicationUser.objects.get(pk=admin_id)
    notification = Notification.objects.create(
        sender=admin,
        tag=request_data.get("tag"),
        title="Admin Notification",
        message=request_data.get("message"),
    )

    for students in unique_users:
        student = ApplicationUser.objects.filter(id=students).first()
        notification.group_of_student.add(student)

        # send email
        send_notification_email(student, notification.title, notification.message)

        data = {
            "notification_id": str(notification.id),
            "tag": str(notification.tag),
            # "model_id": str(sender_user.id),
            "title": str(notification.title),
            "body": str(notification.message),
        }

        response = data.copy()
        response["custom_data"] = json.dumps(
            {
                "tag": str(notification.tag),
                "title": str(notification.title),
                "body": str(notification.message),
            }
        )
        if student.device_token:
            sendPush(
                notification.title,
                notification.message,
                student.device_token,
                response,
            )
