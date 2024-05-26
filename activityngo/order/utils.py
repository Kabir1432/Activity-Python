import datetime
import io
from decimal import Decimal
import qrcode
import pyshorteners
import pdfkit
from django.db.models import (
    Case,
    DecimalField,
    ExpressionWrapper,
    F,
    Sum,
    Value,
    When,
)
from django.template.loader import render_to_string
from django.utils import timezone
from num2words import num2words
import os
from activityngo.order import models
from PyPDF2 import PdfReader, PdfWriter
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from django.core.signing import TimestampSigner
import base64
from activityngo.order.pdf_utils import add_header_and_footer
from activityngo.order.querys import (
    get_task3_mcq_question_data,
    get_task3_upload_photo_data,
    get_short_question_data,
    get_essay_question_data,
    get_task_upload_photo_data, get_task_9_data, calculate_financials,
)
from django.conf import settings
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
from django.core.files.base import ContentFile
import uuid

matplotlib.use("Agg")


def get_number_of_point_string(number_of_point):
    return (
        "20"
        if number_of_point == "points_20"
        else "10" if number_of_point == "points_10" else "05"
    )


def get_number_of_activity_hours_string(number_of_point, order_details):
    return (
        order_details.project.days_of_20_point
        if number_of_point == "points_20"
        else (
            order_details.project.days_of_10_point
            if number_of_point == "points_10"
            else order_details.project.days_of_05_point
        )
    )


def set_expire_days(days):
    return timezone.now() + timezone.timedelta(days=days)


def generate_invoice_number():
    latest_entry = models.Order.objects.order_by("-invoice_number").first()
    # Get the current year
    current_year = datetime.datetime.now().year

    if latest_entry and latest_entry.invoice_number:
        numeric_part = int(latest_entry.invoice_number[9:])

        if numeric_part < 999999:
            incremented_numeric_part = numeric_part + 1
            formatted_numeric_part = str(incremented_numeric_part).zfill(6)
        else:
            formatted_numeric_part = False
        new_franchise_code = "STU/" + f"{current_year}/" + formatted_numeric_part
    else:
        new_franchise_code = "STU/" + f"{current_year}/" + "000001"

    return new_franchise_code


def student_invoice_generate(id):
    order_data = models.Order.objects.prefetch_related("order_details").get(pk=id)
    total_tax_per = models.GSTCategory.objects.first().total_gst_percentage
    gst_data = models.GSTCategory.objects.first()
    point_to_field_mapping = {
        "points_20": "price_of_20_point",
        "points_10": "price_of_10_point",
        "points_05": "price_of_05_point",
    }

    # Annotate the OrderDetail queryset with total_price and total_tax_amount
    order_details = order_data.order_details.annotate(
        total_price=Case(
            *[
                When(number_of_points=point, then=F("project__" + field_name))
                for point, field_name in point_to_field_mapping.items()
            ],
            default=Value(0),  # Default value if number_of_points value not found
            output_field=DecimalField(
                max_digits=10, decimal_places=2
            ),  # Specify DecimalField as output_field
        ),
        order_tax_amount=ExpressionWrapper(
            F("total_price") * Decimal(str(total_tax_per)) / 100 + F("total_price"),
            output_field=DecimalField(max_digits=10, decimal_places=2),
        ),
        tax_amount=ExpressionWrapper(
            F("total_price") * Decimal(str(total_tax_per)) / 100 + F("total_price"),
            output_field=DecimalField(max_digits=10, decimal_places=2),
        ),
    )
    total_tax = order_details.aggregate(total_tax=Sum("tax_amount")).get("total_tax")
    new_total_tax = order_data.cgst + order_data.sgst + order_data.igst
    total_project_price = order_details.aggregate(
        total_project_price=Sum("total_price")
    ).get("total_project_price")
    amount_in_words = num2words(order_data.total_amount).capitalize()
    data = {
        "order_data": order_data,
        "order_details": order_details,
        "total_tax": total_tax,
        "total_project_price": order_data.total_amount,
        "gst_data": gst_data,
        "amount_in_words": amount_in_words,
        "order_details_count": order_data.order_details.all().count(),
        "base_url": settings.PROJECT_BASE_URL,
        "new_total_tax": new_total_tax,
    }

    html = render_to_string("report/student_order_invoice.html", data)
    options = {
        "page-size": "A4",
        "margin-top": "0.01in",
        "margin-right": "0.01in",
        "margin-bottom": "0.01in",
        "margin-left": "0.01in",
        "encoding": "UTF-8",
        "enable-local-file-access": "",  # Add the encoding option directly
        # 'base-url': f'{settings.PROJECT_BASE_URL}/static/'
    }
    pdf = pdfkit.from_string(html, False, options=options)
    pdf_file = io.BytesIO(pdf)
    pdf_file.seek(0)
    order_data.invoice_file.save(
        str(order_data.invoice_number) + ".pdf", ContentFile(pdf_file.read()), save=True
    )
    return False


def encrypt_id(id):
    # Convert ID to bytes and encode using base64
    encoded_id = base64.urlsafe_b64encode(str(id).encode()).decode()

    signer = TimestampSigner()
    encrypted_id = signer.sign(encoded_id)
    return encrypted_id


def create_student_activity_qr_code(obj):
    obj_id = encrypt_id(obj.id)
    url = f"https://activitypointsengg.com/student/verification/{obj_id}/"
    # Shorten the URL
    s = pyshorteners.Shortener()
    short_url = s.tinyurl.short(url)

    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=5, border=5)
    qr.add_data(short_url)
    qr.make(fit=True)
    filename = f"qr_code_{uuid.uuid4()}.png"
    # Create a temporary file to save the QR code image
    qr_code_temp_file = NamedTemporaryFile(delete=False)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(qr_code_temp_file, format="PNG")

    # Save the QR code image in the model's image field
    obj.qr_code_verification.save(filename, File(qr_code_temp_file))

    # Clean up the temporary file
    os.remove(qr_code_temp_file.name)


def generate_student_activity_qr(order_detail, common_data_dict):
    context = {
        "order_detail": order_detail,
        "ngo": order_detail.project.franchise_ngo_name,
        "trustee_details": order_detail.project.franchise_ngo_name.ngo_franchise.franchise_organization.organization_directors.all()[
                           :3],
        "ngo_name": order_detail.project.franchise_ngo_name.ngo_name,
        "state_name": order_detail.project.franchise_ngo_name.state,
        "user": order_detail.order.user,
        "project": order_detail.project,
        "ngo_darpan_no": order_detail.project.franchise_ngo_name.ngo_franchise.franchise_organization.ngo_darpan_no,
        "number_of_points": common_data_dict.get('number_of_points'),
        "number_of_activity_hours": common_data_dict.get('number_of_activity_hours'),
        "start_activity_date": common_data_dict.get('request_data').get('activity_subscribed_date'),
        "end_activity_date": common_data_dict.get('request_data').get('expire_on'),
    }
    html = render_to_string("report/student_activity_certificate.html", context)
    options = {
        "page-size": "A4",
        "orientation": "Landscape",  # Set landscape orientation
        "margin-top": "0.25in",
        "margin-right": "0.15in",
        "margin-bottom": "0.25in",
        "margin-left": "0.15in",
        "encoding": "UTF-8",
        "enable-local-file-access": "",
    }
    try:
        pdf = pdfkit.from_string(html, False, options=options)
        pdf_file = io.BytesIO(pdf)
        pdf_file.seek(0)

        order_detail.student_activity_certificate_file.save(
            str(uuid.uuid4()) + ".pdf", ContentFile(pdf_file.read()), save=True
        )
    except Exception as e:
        print("hello-->", e)


def merge_pdfs(pdf1_content, pdf2_content):
    # Convert bytes objects to BytesIO
    pdf1_stream = BytesIO(pdf1_content)
    pdf2_stream = BytesIO(pdf2_content)

    # Create PdfReader objects
    pdf1_reader = PdfReader(pdf1_stream)
    pdf2_reader = PdfReader(pdf2_stream)

    # Create PdfWriter object for merged PDF
    merged_pdf_writer = PdfWriter()

    # Add pages from the first PDF
    for page_num in range(len(pdf1_reader.pages)):
        merged_pdf_writer.add_page(pdf1_reader.pages[page_num])

    # Add pages from the second PDF
    for page_num in range(len(pdf2_reader.pages)):
        merged_pdf_writer.add_page(pdf2_reader.pages[page_num])

    # Create a BytesIO object to store the merged PDF
    merged_pdf_content = BytesIO()

    # Write the merged PDF to the BytesIO object
    merged_pdf_writer.write(merged_pdf_content)

    return merged_pdf_content.getvalue()


def merge_and_save_pdfs(pdf1_content, pdf2_content, order_detail):
    merged_pdf_content = merge_pdfs(pdf1_content, pdf2_content)

    # Create a ContentFile with the merged PDF content
    merged_pdf_file = ContentFile(merged_pdf_content)

    # Save the ContentFile to the report_file field
    order_detail.report_file.save(
        "viraj" + ".pdf", merged_pdf_file, save=True
    )
    order_detail.save()


def generate_student_activity_chapters(order_detail, common_data_dict):
    upload_photo_data_3 = get_task3_upload_photo_data(order_detail)
    upload_photo_question_data_4 = get_task_upload_photo_data(order_detail, "task_4")
    try:
        upload_photo_question_data_4_dict = {
            "image_1_url": (
                    "https://activityngo.s3.amazonaws.com/activityngo/media/"
                    + upload_photo_question_data_4[0]
            ),
            "image_2_url": (
                    "https://activityngo.s3.amazonaws.com/activityngo/media/"
                    + upload_photo_question_data_4[1]
            ),
            "image_3_url": (
                    "https://activityngo.s3.amazonaws.com/activityngo/media/"
                    + upload_photo_question_data_4[2]
            ),
        }
    except IndexError as e:
        upload_photo_question_data_4_dict = {
            "image_1_url": None,
            "image_2_url": None,
            "image_3_url": None,
        }

    # print(upload_photo_question_data_4_dict)

    context = {
        "order_detail": order_detail,
        "ngo": order_detail.project.franchise_ngo_name,
        "ngo_name": order_detail.project.franchise_ngo_name.ngo_name,
        "state_name": order_detail.project.franchise_ngo_name.state,
        "user": order_detail.order.user,
        "project": order_detail.project,
        "upload_photo_data": upload_photo_data_3,
        "upload_photo_question_data_4_dict": upload_photo_question_data_4_dict,
        "project_report_content": common_data_dict.get('project_report_content'),
        "number_of_points": common_data_dict.get("number_of_points"),
    }
    html = render_to_string("report/student_activity_chapters.html", context)
    options = {
        "page-size": "A4",
        "margin-top": "0.75in",
        "margin-right": "0.75in",
        "margin-bottom": "0.75in",
        "margin-left": "0.75in",
        "encoding": "UTF-8",
        "enable-local-file-access": "",  # Add the encoding option directly
    }

    # try:
    pdf = pdfkit.from_string(html, False, options=options)
    pdf_file = io.BytesIO(pdf)
    pdf_file.seek(0)

    order_detail.student_activity_chapters.save(
        str(uuid.uuid4()) + ".pdf", ContentFile(pdf_file.read()), save=True
    )

    # add_header_and_footer(order_detail, "student_activity_chapters")


def truncate_label(label, max_length=15):
    if len(label) > max_length:
        return label[: max_length - 3] + "..."
    return label


def generate_pie_chart(
        question, options, percentages, order_detail, image_field, question_number
):
    # Create a pie chart
    fig, ax = plt.subplots(figsize=(10, 6))

    # Truncate long labels and add "..."
    # truncated_labels = [truncate_label(label) for label in options]
    numbered_labels = [f"Option {chr(ord('A') + i)}" for i in range(len(options))]
    wedges, texts, autotexts = ax.pie(
        percentages,
        autopct="%1.1f%%",
        startangle=90,
        rotatelabels=True,
        wedgeprops={"edgecolor": "black", "linewidth": 2, "antialiased": True},
        textprops={'fontsize': 14}
    )

    ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Title of the pie chart (question)
    plt.title(
        truncate_label(f"Question - no {question_number} : {question}", max_length=70), fontsize=17
    )
    ax.legend(
        wedges,
        numbered_labels,
        title="Options",
        loc="lower right",
        bbox_to_anchor=(1, 0),
        bbox_transform=plt.gcf().transFigure,
        fontsize=14
    )
    # Save the pie chart as an image in memory
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    # Save the image to the ImageField
    getattr(order_detail, image_field).save(
        str(uuid.uuid4()) + ".png", ContentFile(buffer.read())
    )

    # Close the Matplotlib plot
    plt.close()


def generate_activity_pie_chart(order_detail):
    mca_question_data = get_task3_mcq_question_data(order_detail)
    for i in range(4, 21):
        key = f"mcq_question_{i}"

        question = mca_question_data.get(key).get(f"question_{i}")
        options = mca_question_data.get(key).get("options")
        percentages = mca_question_data.get(key).get("values")
        generate_pie_chart(
            question,
            options,
            percentages,
            order_detail,
            f"student_activity_pie_chart_{i}",
            i,
        )  # question, options, percentages


def generate_student_activity_task_4(order_detail):
    # Get Task 4 data
    short_question_data_task_4 = get_short_question_data(order_detail, "task_4")
    upload_photo_question_data_4 = get_task_upload_photo_data(order_detail, "task_4")
    essay_question_data_4 = get_essay_question_data(order_detail, "task_4")

    try:
        upload_photo_question_data_4_dict = {
            "image_1_url": (
                    "https://activityngo.s3.amazonaws.com/activityngo/media/"
                    + upload_photo_question_data_4[0]
            ),
            "image_2_url": (
                    "https://activityngo.s3.amazonaws.com/activityngo/media/"
                    + upload_photo_question_data_4[1]
            ),
            "image_3_url": (
                    "https://activityngo.s3.amazonaws.com/activityngo/media/"
                    + upload_photo_question_data_4[2]
            ),
        }
    except IndexError as e:
        upload_photo_question_data_4_dict = {
            "image_1_url": None,
            "image_2_url": None,
            "image_3_url": None,
        }

    # Get Task 5 data
    essay_question_data_5 = get_essay_question_data(order_detail, "task_5")

    # Get Task 6 data
    essay_question_data_6 = get_essay_question_data(order_detail, "task_6")

    # Get Task 7 data
    essay_question_data_7 = get_essay_question_data(order_detail, "task_7")

    # Get Task 8 data
    essay_question_data_8 = get_essay_question_data(order_detail, "task_8")

    context = {
        "order_detail": order_detail,
        "ngo": order_detail.project.franchise_ngo_name,
        "ngo_name": order_detail.project.franchise_ngo_name.ngo_name,
        "state_name": order_detail.project.franchise_ngo_name.state,
        "user": order_detail.order.user,
        "project": order_detail.project,
        # set task 4 data
        "short_question_data_task_4": short_question_data_task_4,
        "upload_photo_question_data_4_dict": upload_photo_question_data_4_dict,
        "essay_question_data_4": essay_question_data_4,
        # set task 5 data
        "essay_question_data_5": essay_question_data_5,
        # set task 6 data
        "essay_question_data_6": essay_question_data_6,
        # set task 7 data
        "essay_question_data_7": essay_question_data_7,
        # set task 8 data
        "essay_question_data_8": essay_question_data_8,
        "task_9_data": get_task_9_data(order_detail) if order_detail.number_of_points == "points_20" else {}
    }

    html = render_to_string("report/student_activity_task_4.html", context)
    # print(html)

    options = {
        "page-size": "A4",
        "margin-top": "0.75in",
        "margin-right": "0.15in",
        "margin-bottom": "0.75in",
        # "margin-bottom": "1.25in",
        "margin-left": "0.15in",
        "encoding": "UTF-8",
        "enable-local-file-access": "",  # Add the encoding option directly
    }

    # Generate PDF using pdfkit
    pdf = pdfkit.from_string(html, False, options=options)

    # Save the PDF file to Django model field
    pdf_file = io.BytesIO(pdf)
    pdf_file.seek(0)
    order_detail.student_activity_task_4.save(
        str(uuid.uuid4()) + ".pdf", ContentFile(pdf_file.read()), save=True
    )
    # add_header_and_footer(
    #     order_detail,
    #     "student_activity_task_4",
    # )

    print("PDF generated and saved successfully.")


def generate_student_activity_task_9(order_detail):
    if order_detail.number_of_points != "points_20":
        return
    student_data = get_task_9_data(order_detail)
    calculate_financials_student = calculate_financials(student_data)
    task_9_data = {
        "task_9_data": student_data,
        "calculate_financials": calculate_financials_student
    }
    html = render_to_string("report/student_activity_task_9.html", task_9_data)

    options = {
        "page-size": "A4",
        "margin-top": "0.01in",
        "margin-right": "0.01in",
        "margin-bottom": "0.01in",
        "margin-left": "0.01in",
        "encoding": "UTF-8",
        "enable-local-file-access": "",  # Add the encoding option directly
    }

    # Generate PDF using pdfkit
    pdf = pdfkit.from_string(html, False, options=options)

    # Save the PDF file to Django model field
    pdf_file = io.BytesIO(pdf)
    pdf_file.seek(0)
    order_detail.student_activity_task_9.save(
        str(uuid.uuid4()) + ".pdf", ContentFile(pdf_file.read()), save=True
    )
    # add_header_and_footer(
    #     order_detail,
    #     "student_activity_task_9",
    # )
    # add_header_and_footer(order_detail, "student_activity_task_9_2_10", )


def generate_student_activity_task_2_and10(order_detail, project_report_content):
    # Get Task 8 data
    essay_question_data_2 = get_essay_question_data(order_detail, "task_2")
    context = {
        "essay_question_data_2": essay_question_data_2,
        "project_report_content": project_report_content,
        "order_detail": order_detail
    }
    html = render_to_string("report/student_activity_task_2_and_10.html", context)
    options = {
        "page-size": "A4",
        "margin-top": "0.75in",
        "margin-right": "0.15in",
        "margin-bottom": "1in",
        "margin-left": "0.15in",
        "encoding": "UTF-8",
        "enable-local-file-access": "",  # Add the encoding option directly
    }

    # Generate PDF using pdfkit
    pdf = pdfkit.from_string(html, False, options=options)

    # Save the PDF file to Django model field
    pdf_file = io.BytesIO(pdf)
    pdf_file.seek(0)
    order_detail.student_activity_task_2_and_10.save(
        str(uuid.uuid4()) + ".pdf", ContentFile(pdf_file.read()), save=True
    )
    # add_header_and_footer(
    #     order_detail,
    #     "student_activity_task_2_and_10",
    # )


def generate_student_activity_short_report_chapter(order_detail):
    upload_photo_data_3 = get_task3_upload_photo_data(order_detail)
    upload_photo_question_data_4 = get_task_upload_photo_data(order_detail, "task_4")
    try:
        upload_photo_question_data_4_dict = {
            "image_1_url": (
                    "https://activityngo.s3.amazonaws.com/activityngo/media/"
                    + upload_photo_question_data_4[0]
            ),
            "image_2_url": (
                    "https://activityngo.s3.amazonaws.com/activityngo/media/"
                    + upload_photo_question_data_4[1]
            ),
            "image_3_url": (
                    "https://activityngo.s3.amazonaws.com/activityngo/media/"
                    + upload_photo_question_data_4[2]
            ),
        }
    except IndexError as e:
        upload_photo_question_data_4_dict = {
            "image_1_url": None,
            "image_2_url": None,
            "image_3_url": None,
        }

    context = {
        "order_detail": order_detail,
        "ngo": order_detail.project.franchise_ngo_name,
        "ngo_name": order_detail.project.franchise_ngo_name.ngo_name,
        "state_name": order_detail.project.franchise_ngo_name.state,
        "user": order_detail.order.user,
        "project": order_detail.project,
        "upload_photo_data": upload_photo_data_3,
        "upload_photo_question_data_4_dict": upload_photo_question_data_4_dict,
    }
    html = render_to_string(
        "report/student_activity_short_report_chapeter.html", context
    )

    options = {
        "page-size": "A4",
        "margin-top": "0.25in",
        "margin-right": "0.15in",
        "margin-bottom": "0.25in",
        "margin-left": "0.15in",
        "encoding": "UTF-8",
        "enable-local-file-access": "",  # Add the encoding option directly
    }

    # Generate PDF using pdfkit
    pdf = pdfkit.from_string(html, False, options=options)

    # Save the PDF file to Django model field
    pdf_file = io.BytesIO(pdf)
    pdf_file.seek(0)
    order_detail.student_activity_short_report_chapter.save(
        str(uuid.uuid4()) + ".pdf", ContentFile(pdf_file.read()), save=True
    )
