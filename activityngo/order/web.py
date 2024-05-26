from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.core.signing import Signer, BadSignature
from django.shortcuts import get_object_or_404
from activityngo.order.models import OrderDetail
from django.core.signing import TimestampSigner
import base64


def encrypt_id(id):
    signer = Signer()
    encrypted_id = signer.sign(str(id))
    return encrypted_id


def decrypt_id(encrypted_id):
    signer = TimestampSigner()
    try:
        decoded_id = base64.urlsafe_b64decode(signer.unsign(encrypted_id, max_age=None)).decode()
        return int(decoded_id)
    except (BadSignature, base64.binascii.Error):
        return None


def GetStudentVerificationPage(request, encrypted_id):
    id = decrypt_id(encrypted_id)
    if id is not None:
        order_details = get_object_or_404(OrderDetail, id=id, is_complete=True)

        context = {
            "order_detail": order_details,
            "student_details": order_details.order.user.student_details,
            "user": order_details.order.user
        }
        return render(request, 'student/verification_page.html', context)
    else:
        return HttpResponseBadRequest('Invalid ID')
