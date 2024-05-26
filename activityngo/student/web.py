from django.shortcuts import render


def get_student_deletion_instructions(request):
    return render(request, 'student/deletion_page.html', )


def get_student_index_page(request):
    return render(request, 'student/index.html', )
