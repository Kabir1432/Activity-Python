from celery import shared_task
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
import io
import pdfkit
from activityngo.order.models import OrderDetail
import uuid
from activityngo.activity_report.models import ReportContent
from activityngo.order.utils import (
    create_student_activity_qr_code,
    generate_student_activity_qr,
    merge_and_save_pdfs,
    generate_student_activity_chapters,
    generate_activity_pie_chart,
    generate_student_activity_task_4,
    generate_student_activity_task_9,
    generate_student_activity_task_2_and10,
    generate_student_activity_short_report_chapter,
    get_number_of_point_string,
    get_number_of_activity_hours_string,
)
from activityngo.taskapp import app
from ..entities.models import ImplementationBatches
from activityngo.order.pdf_utils import add_header_and_footer

@app.task
def generate_report(order_detail_id,request_data):
    try:
        order_detail = order_detail_id
        if type(order_detail_id) is int:
            order_detail = OrderDetail.objects.get(pk=order_detail_id)
        if type(request_data.get('implementation_batch')) is int or type(request_data.get('implementation_batch')) is str:
            implementation_batch = ImplementationBatches.objects.get(pk=request_data.get("implementation_batch"))
        try:
            project_report_content = ReportContent.objects.get(project=order_detail.project, type_point=order_detail.number_of_points)
        except:
            project_report_content = {}

        if not order_detail.qr_code_verification:
            create_student_activity_qr_code(order_detail)

        common_data_dict = {
            "number_of_points": get_number_of_point_string(order_detail.number_of_points),
            "project_report_content":project_report_content,
            "implementation_batch":implementation_batch,
            "request_data":request_data,
            "number_of_activity_hours": get_number_of_activity_hours_string(
                order_detail.number_of_points, order_detail
            ),
        }

        generate_student_activity_qr( #activity_certificate
            order_detail, common_data_dict
        )  # this will genrate student certificate with qr code
        generate_activity_pie_chart(order_detail)
        generate_student_activity_chapters(order_detail,common_data_dict)
        if order_detail.number_of_points != "points_05":
            generate_student_activity_task_4(order_detail)
        generate_student_activity_task_9(order_detail)
        generate_student_activity_task_2_and10(order_detail,project_report_content)
        # generate_student_activity_short_report_chapter(order_detail)


        context = {
            "order_detail": order_detail,
            "ngo": order_detail.project.franchise_ngo_name,
            "ngo_name": order_detail.project.franchise_ngo_name.ngo_name,
            "state_name": order_detail.project.franchise_ngo_name.state.first(),
            "user": order_detail.order.user,
            "project": order_detail.project,
            "number_of_points": common_data_dict.get("number_of_points"),
            "number_of_activity_hours": common_data_dict.get("number_of_activity_hours"),
            "project_report_content": project_report_content,
            "implementation_batch": common_data_dict.get('implementation_batch'),
            "request_data": request_data,
        }
        html = render_to_string("report/student_activity_report_1_to_5.html", context)

        options = {
            "page-size": "A4",
            "margin-top": "0.25in",
            "margin-right": "0.15in",
            "margin-bottom": "0.25in",
            "margin-left": "0.15in",
            "encoding": "UTF-8",
            "enable-local-file-access": "",  # Add the encoding option directly
        }
        pdf = pdfkit.from_string(html, False, options=options)
        pdf_file = io.BytesIO(pdf)
        print(pdf_file)
        pdf_file.seek(0)

        order_detail.student_activity_certificate_page_1_to_5_file.save(
            str(uuid.uuid4()) + ".pdf", ContentFile(pdf_file.read()), save=True
        )

        pdf1_content_student_activity_certificate_page_1_to_5_file = order_detail.student_activity_certificate_page_1_to_5_file.read()
        pdf2_content_activity_certificate_file = order_detail.student_activity_certificate_file.read()
        merge_and_save_pdfs(pdf1_content_student_activity_certificate_page_1_to_5_file, pdf2_content_activity_certificate_file, order_detail)
        #
        pdf1_content = order_detail.report_file.read()
        pdf2_content = order_detail.student_activity_chapters.read()
        merge_and_save_pdfs(pdf1_content, pdf2_content, order_detail)

        if order_detail.number_of_points != "points_05":
            pdf1_content = order_detail.report_file.read()
            pdf2_content = order_detail.student_activity_task_4.read()
            merge_and_save_pdfs(pdf1_content, pdf2_content, order_detail)

        if order_detail.number_of_points == "points_20":
            pdf1_content = order_detail.report_file.read()
            pdf2_content = order_detail.student_activity_task_9.read()
            merge_and_save_pdfs(pdf1_content, pdf2_content, order_detail)

        pdf1_content = order_detail.report_file.read()
        pdf2_content = order_detail.student_activity_task_2_and_10.read()
        merge_and_save_pdfs(pdf1_content, pdf2_content, order_detail)

        add_header_and_footer(
            order_detail,
            "report_file",
            implementation_batch,
        )

        # below code is for short report

        # pdf1_content = order_detail.report_file.read()
        # # pdf2_content = order_detail.student_activity_certificate_page_1_to_5_file.read()
        # merge_and_save_pdfs(pdf1_content, pdf1_content_student_activity_certificate_page_1_to_5_file, order_detail)
        #
        # pdf1_content = order_detail.report_file.read()
        # # pdf2_content = order_detail.student_activity_certificate_file.read()
        # merge_and_save_pdfs(pdf1_content, pdf2_content_activity_certificate_file, order_detail)
        #
        # pdf1_content = order_detail.report_file.read()
        # pdf2_content = order_detail.student_activity_short_report_chapter.read()
        # merge_and_save_pdfs(pdf1_content, pdf2_content, order_detail)
        order_detail.activity_status = "complete"
        order_detail.save()
    except Exception as e:
        print("error in main",e)
        order_detail.activity_status = "cancel"
        order_detail.save()
