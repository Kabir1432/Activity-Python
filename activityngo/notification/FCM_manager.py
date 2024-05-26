import os

import firebase_admin
from django.contrib.auth import get_user_model
from firebase_admin import credentials, messaging

# from config import settings
#
# cred = credentials.Certificate(os.path.join(settings.BASE_DIR,
#                                             'accounts/fcm/lend-b968f-firebase-adminsdk-rce9p-1cbfd45ddb.json'))
# firebase_admin.initialize_app(cred)

User = get_user_model()


# to send notification using firebase admin to one user
def sendPush(title, msg, registration_token, dataObject):
    if registration_token is None:
        registration_token = [0]
    elif not isinstance(registration_token, list):
        registration_token = [registration_token]

    aps = messaging.Aps(sound="default", badge=0)
    payload = messaging.APNSPayload(aps)
    message = messaging.MulticastMessage(
        notification=messaging.Notification(title=title, body=msg),
        data=dataObject,
        android=messaging.AndroidConfig(priority="high"),
        tokens=registration_token,
        apns=messaging.APNSConfig(payload=payload),
    )
    response = messaging.send_multicast(message)
    print(registration_token)
    print(
        f"Notification Data >> {dataObject} : "
        f"Response {response.success_count} | Error : {response.responses[0].exception}"
    )
    # return response
    return {
        "success_count": response.success_count,
        "errors": [str(resp.exception) for resp in response.responses],
    }


# to send notification using topic  to all users
def send_to_topic(title, msg, topic, data):
    condition = "'" + topic + "' in topics"
    aps = messaging.Aps(sound="default", badge=0)
    payload = messaging.APNSPayload(aps)
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=msg,
        ),
        data=data,
        android=messaging.AndroidConfig(priority="high"),
        apns=messaging.APNSConfig(payload=payload),
        condition=condition,
    )
    # sending message to all user
    response = messaging.send(message)
    print(response, "all notifications sent successfully")


# subscribe one token of user from given topic
def subscribe_to_topic(topic, registration_token):
    response = messaging.subscribe_to_topic(registration_token, topic)
    print(response.success_count, "token was subscribed successfully")


# unsubscribe one token of user from given topic
def unsubscribe_from_topic(topic, registration_token):
    response = messaging.unsubscribe_from_topic(registration_token, topic)
    print(response.success_count, "token was unsubscribed successfully")


# subscribe all user from given topic
def subscribe_to_topic_all(topic):
    # from accounts.models import User

    registration_tokens = list(
        User.objects.all()
        .exclude(device_token__null=True)
        .values_list("device_token", flat=True)
    )
    while len(registration_tokens) > 0:
        registration_token = registration_tokens[:999]
        response = messaging.subscribe_to_topic(registration_token, topic)
        print("batch+registration_token", len(registration_token))
        del registration_tokens[:999]
    print("all tokens were subscribed successfully")


# unsubscribe all user from given topic
def unsubscribe_from_topic_all(topic):
    # from accounts.models import User

    registration_tokens = list(
        User.objects.all()
        .exclude(device_token__null=True)
        .values_list("device_token", flat=True)
    )
    while len(registration_tokens) > 0:
        registration_token = registration_tokens[:999]
        response = messaging.unsubscribe_from_topic(registration_token, topic)
        print("batch+registration_token", len(registration_token))
        del registration_tokens[:999]
    print(response.success_count, "all tokens were unsubscribed successfully")
