import io
import uuid
from django.core.files.base import ContentFile
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas


def add_header_and_footer(order_detail, pdf_file_field,implementation_batch=None):
    try:
        header_text = "AICTE Activity Points Programme"
        # Open the PDF file
        # with open(order_detail.__dict__.get(f'{pdf_file_field}'), 'rb') as pdf_file:
        with order_detail.__dict__.get(f'{pdf_file_field}').open(mode='rb') as pdf_file:
            # Create a PDF reader object
            pdf_reader = PdfReader(pdf_file)

            # Create a PDF writer object
            pdf_writer = PdfWriter()

            # Iterate through all pages in the original PDF
            for page_num in range(len(pdf_reader.pages)):
                # Get the page
                page = pdf_reader.pages[page_num]

                # Create a new PDF object for the header
                header_pdf = PdfWriter()

                # Add the header text to the new PDF
                header_page = header_pdf.add_blank_page(width=page.mediabox.width, height=page.mediabox.height)

                # Create a canvas to draw text and border on the header_page
                packet = io.BytesIO()
                can = canvas.Canvas(packet)

                # Draw a rectangle as the border around the entire page
                border_padding = 10  # Adjust the padding as needed
                if page_num > 5:
                    can.rect(border_padding, border_padding, page.mediabox.width - 2 * border_padding,
                             page.mediabox.height - 2 * border_padding, stroke=1, fill=0)

                # Calculate X-coordinate for centering the text
                if page_num > 6:
                    x_coord = (float(page.mediabox.width) - can.stringWidth(header_text, 'Helvetica', 12)) / 2
                    # Draw text inside the rectangle
                    # can.setFont('Helvetica-Bold', 12)
                    # can.setFont('Times-Roman', 12)
                    can.setFont('Times-Bold', 12)
                    can.drawString(x_coord + 150, float(page.mediabox.height) - 30, header_text)

                    # Calculate Y-coordinate for the underline
                    underline_y = float(page.mediabox.height) - 35
                    # Draw a line under the text
                    can.line(30, underline_y, 375 + can.stringWidth(header_text, 'Helvetica', 12), underline_y)

                if page_num > 7:

                    # Calculate X-coordinate for centering the footer text
                    x_coord_footer_left = 50
                    x_coord_footer_center = (float(page.mediabox.width) - can.stringWidth("2023-2024", 'Helvetica', 12)) / 2
                    x_coord_footer_right = float(page.mediabox.width) - 50

                    # Calculate Y-coordinate for the underline in the footer
                    underline_y_footer = 30
                    # Draw footer text inside the rectangle
                    can.drawString(x_coord_footer_left, underline_y_footer,
                                   f"Student ID/USN - {order_detail.order.user.student_details.id_number}")
                    # can.drawString(x_coord_footer_center, underline_y_footer, f"{implementation_batch.start_year}-{implementation_batch.end_year}")
                    if implementation_batch:
                        can.drawString(x_coord_footer_center, underline_y_footer, f"{implementation_batch.start_year}-{implementation_batch.end_year}")
                    else:
                        can.drawString(x_coord_footer_center, underline_y_footer, "-")
                    can.drawString(x_coord_footer_right - 50, underline_y_footer, "Page {}".format(page_num - 7))


                    can.line(30, underline_y_footer + 20,
                             515 + can.stringWidth("Page {}".format(page_num), 'Helvetica', 12), underline_y_footer + 20)

                can.save()

                # Move the buffer position to the beginning
                packet.seek(0)
                # new_pdf = PdfReader(packet)
                new_pdf = PdfReader(packet)
                if new_pdf.pages:  # Check if new_pdf.pages has elements
                    header_page.merge_page(new_pdf.pages[0])
                # Merge the original page with the header page
                # header_page.merge_page(new_pdf.pages[0])
                page.merge_page(header_page)

                # Add the modified page to the writer
                pdf_writer.add_page(page)
            # loop end----------------
            # Create the output PDF file
            # output_pdf_path = f"new_pdf_{uuid.uuid4()}.pdf"
            # with open(output_pdf_path, 'wb') as modified_pdf_file:
            #     # Write the modified PDF to the output file
            #     pdf_writer.write(modified_pdf_file)
            output_pdf = io.BytesIO()
            pdf_writer.write(output_pdf)
            output_pdf.seek(0)
            # Save the modified PDF to the model's FileField
            # getattr(order_detail, pdf_file_field).save(
            #     f"{uuid.uuid4()}.pdf", ContentFile(open(output_pdf_path, 'rb').read())
            # )
            # Save the modified PDF to the model's FileField
            getattr(order_detail, pdf_file_field).save(
                f"{uuid.uuid4()}.pdf", ContentFile(output_pdf.read())
            )
    except Exception as e:
        print("error in pdf ",e)
