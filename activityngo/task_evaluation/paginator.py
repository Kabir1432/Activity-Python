from rest_framework import pagination
from rest_framework.response import Response


class EssayEvaluationQuestionPagination(pagination.PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "page_size"
    max_page_size = 1000

    def get_paginated_response(self, data):
        order_details = data.serializer.context.get('order_details')
        custom_task_number = {
            "task_1": "task1",
            "task_2": "task2",
            "task_3": "task3",
            "task_4": "task4",
            "task_5": "task5",
            "task_6": "task6",
            "task_7": "task7",
            "task_8": "task8",
            "task_9": "task9",
            "task_10": "task10",
        }
        task_number = data.serializer.context.get('task_number')
        return Response(
            {
                "page": self.page.number,
                "page_size": len(self.page.object_list),
                "total_page_count": self.page.paginator.num_pages,
                "total_count": self.page.paginator.count,
                "question_type": "essay_question",
                "task_number_evaluation": custom_task_number.get(task_number),
                "student_name": order_details.order.user.fullname,
                "project_name": order_details.project.title,
                "project_type": order_details.project.category.name if order_details.project.category else None,
                "task_number": task_number,
                "task_name": order_details.project.task_instructions_question_projects.filter(
                main_task_number=task_number).first().task_instructions if order_details.project.task_instructions_question_projects.filter(
                main_task_number=task_number).first() else "",
                "results": data,
            }
        )
