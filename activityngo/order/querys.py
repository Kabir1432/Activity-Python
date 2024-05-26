def get_task3_upload_photo_data(order_details):
    from activityngo.student_project.models import UploadPhotoQuestionAnswers

    query = UploadPhotoQuestionAnswers.objects.filter(
        status="Accepted",
        order_details=order_details,
        question__main_task_number="task_3",
    ).order_by("survey_number")
    image_dict = {}
    for i in query:
        image_dict[f"image_{i.survey_number}_url"] = i.answer.url if i.answer else None

    return image_dict


def get_task3_mcq_question_data(order_details):
    from activityngo.student_project.models import MCQQuestionAnswers

    mcq_question_queryset = MCQQuestionAnswers.objects.filter(
        status="Accepted",
        order_details=order_details,
        question__main_task_number="task_3",
    )
    mca_question_data = {
        "status": mcq_question_queryset.filter(question__sub_task_number=4)[0].status
    }
    for i in range(4, 21):
        key = f"mcq_question_{i}"  # set dynamic key name
        mcq_ans_sub_question = mcq_question_queryset.filter(
            question__sub_task_number=i
        )  # get data with sub-task number
        main_mcq_question = (
            mcq_ans_sub_question[0].question
            if mcq_ans_sub_question[0].question
            else None
        )  # get main question
        mca_question_data[key] = {}  # add dynamic key in mcq list
        mca_question_data[key].update(
            {f"question_{i}": main_mcq_question.question}
        )  # add question in dict

        for index, i in enumerate(
                main_mcq_question.mca_question_option.all(), start=1
        ):  # this loop for add nested data in mcq question
            if "options" in mca_question_data[key] and isinstance(
                    mca_question_data[key]["options"], list
            ):
                mca_question_data[key]["options"].append(i.option)
            else:
                mca_question_data[key]["options"] = [i.option]

            if "values" in mca_question_data[key] and isinstance(
                    mca_question_data[key]["values"], list
            ):
                mca_question_data[key]["values"].append(
                    mcq_question_queryset.filter(answer=i).count()
                )
            else:
                mca_question_data[key]["values"] = [
                    mcq_question_queryset.filter(answer=i).count()
                ]

    return mca_question_data


def get_short_question_data(order_details, task_number):
    from activityngo.task_evaluation.serializers import ShortQuestionAnswersSerializer
    from activityngo.student_project.models import ShortQuestionAnswers

    short_question_data = ShortQuestionAnswersSerializer(
        ShortQuestionAnswers.objects.filter(
            status="Accepted",
            order_details_id=order_details,
            question__main_task_number=task_number,  # "task_3",
        ).order_by("question__sub_task_number"),
        many=True,
    ).data
    return short_question_data


def get_essay_question_data(order_details, task_number):
    from activityngo.task_evaluation.serializers import EssayQuestionAnswersSerializer
    from activityngo.student_project.models import EssayQuestionAnswers

    essay_question_data = EssayQuestionAnswersSerializer(
        EssayQuestionAnswers.objects.filter(
            status="Accepted",
            order_details_id=order_details,
            question__main_task_number=task_number,
        ).order_by("question__sub_task_number"),
        many=True,
    ).data
    return essay_question_data


def get_task_upload_photo_data(order_details, task_number):
    from activityngo.student_project.models import UploadPhotoQuestionAnswers
    from activityngo.task_evaluation.serializers import (
        UploadPhotoQuestionAnswersSerializer,
    )

    # upload_photo_question_data = UploadPhotoQuestionAnswersSerializer(
    upload_photo_question_data = (
        UploadPhotoQuestionAnswers.objects.filter(
            status="Accepted",
            order_details_id=order_details,
            question__main_task_number=task_number,
        )
        .order_by("question__sub_task_number")
        .values_list("answer", flat=True)
    )
    #     many=True,
    # ).data

    return upload_photo_question_data


# def get_task_9_data(order_details):
#     from activityngo.student_project.models import (
#         ShortQuestionAnswers,
#         DropDownQuestionAnswers,
#         NumericQuestionAnswers,
#         PercentageQuestionAnswers,
#     )
#
#     question_answer_data = []
#
#     # Fetching all types of question answers and combining them into a single list
#     for model in [
#         ShortQuestionAnswers,
#         DropDownQuestionAnswers,
#         NumericQuestionAnswers,
#         PercentageQuestionAnswers,
#     ]:
#         question_answer_data.extend(
#             list(
#                 model.objects.filter(
#                     status="Accepted",
#                     order_details_id=order_details,
#                     question__main_task_number="task_9",
#                 ).order_by("question__sub_task_number")
#             )
#         )
#
#     data = {}
#
#     for idx, qa in enumerate(question_answer_data, start=1):
#         question_key = f"question_{idx}"
#         data[question_key] = {
#             "question": qa.question.question,
#             "answer": (
#                 qa.answer.option
#                 if isinstance(qa, DropDownQuestionAnswers)
#                 else qa.answer
#             ),
#         }
#     return data


def get_task_9_data(order_details):
    from activityngo.student_project.models import (
        ShortQuestionAnswers,
        DropDownQuestionAnswers,
        NumericQuestionAnswers,
        PercentageQuestionAnswers,
    )

    short_question_answer_data = ShortQuestionAnswers.objects.filter(
        status="Accepted",
        order_details_id=order_details,
        question__main_task_number="task_9",
    ).order_by("question__sub_task_number")
    drop_down_question_question_answer_data = DropDownQuestionAnswers.objects.filter(
        status="Accepted",
        order_details_id=order_details,
        question__main_task_number="task_9",
    ).order_by("question__sub_task_number")
    numeric_question_answer_data = NumericQuestionAnswers.objects.filter(
        status="Accepted",
        order_details_id=order_details,
        question__main_task_number="task_9",
    ).order_by("question__sub_task_number")

    percentage_question_answer_data = PercentageQuestionAnswers.objects.filter(
        status="Accepted",
        order_details_id=order_details,
        question__main_task_number="task_9",
    ).order_by("question__sub_task_number")

    data = {
        "name_of_the_company": {
            "question": short_question_answer_data[0].question.question,
            "answer": short_question_answer_data[0].answer,
        },
        "location_of_the_company": {
            "question": short_question_answer_data[1].question.question,
            "answer": short_question_answer_data[1].answer,
        },
        "sector_of_the_company": {
            "question": drop_down_question_question_answer_data[0].question.question,
            "answer": drop_down_question_question_answer_data[0].answer.option,
        },
        "source_of_investment": {
            "question": drop_down_question_question_answer_data[1].question.question,
            "answer": drop_down_question_question_answer_data[1].answer.option,
        },
        "office_advance": {
            "question": numeric_question_answer_data[0].question.question,
            "answer": numeric_question_answer_data[0].answer,
        },
        "company_establishment_fee": {
            "question": numeric_question_answer_data[1].question.question,
            "answer": numeric_question_answer_data[1].answer,
        },
        "no_of_staff": {
            "question": numeric_question_answer_data[2].question.question,
            "answer": numeric_question_answer_data[2].answer,
        },
        "office_infrastructure_expenses": {
            "question": numeric_question_answer_data[3].question.question,
            "answer": numeric_question_answer_data[3].answer,
        },
        "software_development_expenses": {
            "question": numeric_question_answer_data[4].question.question,
            "answer": numeric_question_answer_data[4].answer,
        },
        "hardware_machine_expenses": {
            "question": numeric_question_answer_data[5].question.question,
            "answer": numeric_question_answer_data[5].answer,
        },
        "total_capital_expenses": {
            "question": numeric_question_answer_data[6].question.question,
            "answer": numeric_question_answer_data[6].answer,
        },
        "office_rent_month": {
            "question": numeric_question_answer_data[7].question.question,
            "answer": numeric_question_answer_data[7].answer,
        },
        "total_staff_salary_month": {
            "question": numeric_question_answer_data[8].question.question,
            "answer": numeric_question_answer_data[8].answer,
        },
        "marketing_expenses_month": {
            "question": numeric_question_answer_data[9].question.question,
            "answer": numeric_question_answer_data[9].answer,
        },
        "software_operating_expenses_month": {
            "question": numeric_question_answer_data[10].question.question,
            "answer": numeric_question_answer_data[10].answer,
        },
        "hardware_machine_operating_expenses_month": {
            "question": numeric_question_answer_data[11].question.question,
            "answer": numeric_question_answer_data[11].answer,
        },
        "auditor_Expenses_month": {
            "question": numeric_question_answer_data[12].question.question,
            "answer": numeric_question_answer_data[12].answer,
        },
        "electricity_expenses_month": {
            "question": numeric_question_answer_data[13].question.question,
            "answer": numeric_question_answer_data[13].answer,
        },
        "internet_expenses_month": {
            "question": numeric_question_answer_data[14].question.question,
            "answer": numeric_question_answer_data[14].answer,
        },
        "total_operational_expenses": {
            "question": numeric_question_answer_data[15].question.question,
            "answer": numeric_question_answer_data[15].answer,
        },
        "total_sale_amount_month": {
            "question": numeric_question_answer_data[16].question.question,
            "answer": numeric_question_answer_data[16].answer,
        },
        "increase_percentage_in_sales_financial_year_2": {
            "question": percentage_question_answer_data[0].question.question,
            "answer": percentage_question_answer_data[0].answer,
        },
        "increase_percentage_in_investment_financial_year_2": {
            "question": percentage_question_answer_data[1].question.question,
            "answer": percentage_question_answer_data[1].answer,
        },
        "increase_percentage_in_sales_financial_year_3": {
            "question": percentage_question_answer_data[2].question.question,
            "answer": percentage_question_answer_data[2].answer,
        },
        "increase_percentage_in_investment_financial_year_3": {
            "question": percentage_question_answer_data[3].question.question,
            "answer": percentage_question_answer_data[3].answer,
        },
    }
    return data


def calculate_financials(data):
    values = {
        "Office_Advance": float(data.get("office_advance").get("answer")),
        "Company_Establishment_Fee": float(data.get("company_establishment_fee").get("answer")),
        "No_of_Staff": float(data.get("no_of_staff").get("answer")),
        "Office_Infrastructure_Expenses": float(data.get("office_infrastructure_expenses").get("answer")),
        "Software_Development_Expenses": float(data.get("software_development_expenses").get("answer")),
        "Hardware_Machine_Expenses": float(data.get("hardware_machine_expenses").get("answer")),
        "Total_Staff_Salary_Month": float(data.get("total_staff_salary_month").get("answer")),
        "Office_Rent_Month": float(data.get("office_rent_month").get("answer")),
        "Total_Capital_Expenses": float(data.get("total_capital_expenses").get("answer")),
        "Marketing_Expenses_Month": float(data.get("marketing_expenses_month").get("answer")),
        "Software_Operating_Expenses_Month": float(data.get("software_operating_expenses_month").get("answer")),
        "Hardware_Machine_Operating_Expenses_Month": float(
            data.get("hardware_machine_operating_expenses_month").get("answer")),
        "Auditor_Expenses_Month": float(data.get("auditor_Expenses_month").get("answer")),
        "Electricity_Expenses_Month": float(data.get("electricity_expenses_month").get("answer")),
        "Internet_Expenses_Month": float(data.get("internet_expenses_month").get("answer")),
        "Total_Sale_Amount_Month": float(data.get("total_sale_amount_month").get("answer")),
        "Increase_Percentage_in_Sales2": float(data.get("increase_percentage_in_sales_financial_year_2").get("answer")),
        "Increase_Percentage_in_Investment2": float(
            data.get("increase_percentage_in_investment_financial_year_2").get("answer")),
        "Increase_Percentage_in_Sales3": float(data.get("increase_percentage_in_sales_financial_year_3").get("answer")),
        "Increase_Percentage_in_Investment3": float(
            data.get("increase_percentage_in_investment_financial_year_3").get("answer")),
    }

    # Calculate Total_Staff_Salary_Month
    values["Total_Staff_Salary_Month"] = values["No_of_Staff"] * 20000

    # Calculate Total_Capital_Expenses
    # values["Total_Capital_Expenses"] = sum(
    #     [
    #         values["Office_Advance"],
    #         values["Company_Establishment_Fee"],
    #         values["Office_Infrastructure_Expenses"],
    #         values["Software_Development_Expenses"],
    #         values["Hardware_Machine_Expenses"],
    #     ]
    # )

    # Calculate Assets - FY - 1
    values["Cash"] = (values["Total_Sale_Amount_Month"] * 12 * 30) / 100
    values["Accounts_Receivable"] = 0.00
    values["Inventory"] = 0.00
    values["Prepaid_Expenses"] = 0.00
    values["Short_Term_Investments"] = 0.0
    values["Long_Term_Investments"] = values["Office_Advance"]
    values["Property_Plant_and_Equipment"] = (
                                                     values["Office_Infrastructure_Expenses"] + values[
                                                 "Hardware_Machine_Expenses"]
                                             ) * 0.60
    values["Intangible_Assets"] = values["Software_Development_Expenses"] * 0.75
    values["Income_Tax"] = 0
    values["Other"] = 0

    values["Total_Current_Assets"] = sum(
        [
            values["Cash"],
            values["Accounts_Receivable"],
            values["Inventory"],
            values["Prepaid_Expenses"],
            values["Short_Term_Investments"],
        ]
    )

    values["Total_Fixed_Assets"] = sum(
        [
            values["Long_Term_Investments"],
            values["Property_Plant_and_Equipment"],
            values["Intangible_Assets"],
        ]
    )

    values["Total_Other_Assets"] = sum([values["Income_Tax"], values["Other"]])

    values["Total_Assets"] = sum(
        [
            values["Total_Current_Assets"],
            values["Total_Fixed_Assets"],
            values["Total_Other_Assets"],
        ]
    )

    # Liabilities and Owner's Equity - FY - 1
    values["Accounts_Payable"] = values["Software_Operating_Expenses_Month"] * 12
    values["Short_Term_Loans"] = 0.00
    values["Income_Taxes_Payable"] = 0.00
    values["Accrued_Salary_Wages"] = values["Total_Staff_Salary_Month"]
    values["Unearned_Revenue"] = 0.00
    values["Current_Portion_of_Long_Term_Debt"] = 0.00
    values["Long_Term_Debt"] = values["Total_Capital_Expenses"] * 0.8
    values["Deferred_Income_Tax"] = 0.00
    values["Others"] = 0.00
    values["Owners_Investment"] = values["Total_Capital_Expenses"] * 0.05
    values["Others2"] = 0.00
    values["Retained_Earnings"] = values["Total_Assets"] - (
            values["Accounts_Payable"]
            + values["Short_Term_Loans"]
            + values["Income_Taxes_Payable"]
            + values["Accrued_Salary_Wages"]
            + values["Unearned_Revenue"]
            + values["Current_Portion_of_Long_Term_Debt"]
            + values["Long_Term_Debt"]
            + values["Deferred_Income_Tax"]
            + values["Others"]
            + values["Owners_Investment"]
            + values["Others2"]
    )

    values["Total_Current_Liabilities"] = (
            values["Accounts_Payable"]
            + values["Short_Term_Loans"]
            + values["Income_Taxes_Payable"]
            + values["Accrued_Salary_Wages"]
            + values["Unearned_Revenue"]
            + values["Current_Portion_of_Long_Term_Debt"]
    )
    values["Total_Long_Term_Liabilities"] = (
            values["Long_Term_Debt"] + values["Deferred_Income_Tax"] + values["Others"]
    )
    values["Total_Owner_Equity"] = (
            values["Owners_Investment"] + values["Others2"] + values["Retained_Earnings"]
    )
    # ASSETS (in INR) - FY - 1
    # ---------------------------------
    values["Cash"] = (values["Total_Sale_Amount_Month"] * 12 * 30) / 100
    values["Accounts_Receivable"] = 0.00
    values["Inventory"] = 0.00
    values["Prepaid_Expenses"] = 0.00
    values["Short_Term_Investments"] = 0.0
    values["Long_Term_Investments"] = values["Office_Advance"]
    values["Property_Plant_and_Equipment"] = (values["Office_Infrastructure_Expenses"] + values[
        "Hardware_Machine_Expenses"]) * 0.60
    values["Intangible_Assets"] = values["Software_Development_Expenses"] * 0.75
    values["Income_Tax"] = 0
    values["Other"] = 0

    values["Total_Current_Assets"] = (values["Cash"] + values["Accounts_Receivable"] + values["Inventory"] +
                                      values["Prepaid_Expenses"] + values["Short_Term_Investments"])
    values["Total_Fixed_Assets"] = (values["Long_Term_Investments"] + values["Property_Plant_and_Equipment"] +
                                    values["Intangible_Assets"])
    values["Total_Other_Assets"] = values["Income_Tax"] + values["Other"]

    values["Total_Assets"] = (values["Total_Current_Assets"] + values["Total_Fixed_Assets"] +
                              values["Total_Other_Assets"])

    # ASSETS (in INR) - FY - 2
    # -----------------------------
    values["Cash2"] = values["Cash"] * (100 + 12 * values["Increase_Percentage_in_Sales2"]) / 100
    values["Accounts_Receivable2"] = values["Cash2"] * 0.5
    values["Inventory2"] = 0.00
    values["Prepaid_Expenses2"] = 0.00
    values["Short_Term_Investments2"] = 0.0
    values["Long_Term_Investments2"] = values["Long_Term_Investments"] * (
            100 + 12 * values["Increase_Percentage_in_Investment2"]) / 100
    values["Property_Plant_and_Equipment2"] = values["Property_Plant_and_Equipment"]
    values["Intangible_Assets2"] = values["Intangible_Assets"]
    values["Income_Tax2"] = 0
    values["Other2"] = 0

    values["Total_Current_Assets2"] = (values["Cash2"] + values["Accounts_Receivable2"] + values["Inventory2"] +
                                       values["Prepaid_Expenses2"] + values["Short_Term_Investments2"])
    values["Total_Fixed_Assets2"] = (values["Long_Term_Investments2"] + values["Property_Plant_and_Equipment2"] +
                                     values["Intangible_Assets2"])
    values["Total_Other_Assets2"] = values["Income_Tax2"] + values["Other2"]

    values["Total_Assets2"] = (values["Total_Current_Assets2"] + values["Total_Fixed_Assets2"] +
                               values["Total_Other_Assets2"])

    # ASSETS (in INR) - FY - 3
    # -------------------------------
    # import pdb
    # pdb.set_trace()
    values["Cash3"] = values["Cash2"] * (100 + 12 * values["Increase_Percentage_in_Sales3"]) / 100
    values["Accounts_Receivable3"] = values["Cash3"] * 0.5
    values["Inventory3"] = 0.00
    values["Prepaid_Expenses3"] = 0.00
    values["Short_Term_Investments3"] = 0.0
    values["Long_Term_Investments3"] = values["Long_Term_Investments2"] * (
            100 + 12 * values["Increase_Percentage_in_Investment3"]) / 100
    values["Property_Plant_and_Equipment3"] = values["Property_Plant_and_Equipment2"]
    values["Intangible_Assets3"] = values["Intangible_Assets2"]
    values["Income_Tax3"] = 0
    values["Other3"] = 0

    values["Total_Current_Assets3"] = (values["Cash3"] + values["Accounts_Receivable3"] + values["Inventory3"] +
                                       values["Prepaid_Expenses3"] + values["Short_Term_Investments3"])
    values["Total_Fixed_Assets3"] = (values["Long_Term_Investments3"] + values["Property_Plant_and_Equipment3"] +
                                     values["Intangible_Assets3"])
    values["Total_Other_Assets3"] = values["Income_Tax3"] + values["Other3"]

    values["Total_Assets3"] = (values["Total_Current_Assets3"] + values["Total_Fixed_Assets3"] +
                               values["Total_Other_Assets3"])

    # LIABILITIES and OWNER's EQUITY (in INR) - FY - 2
    values["Accounts_Payable2"] = values["Accounts_Payable"] * (
            100 + values["Increase_Percentage_in_Sales2"] * 12) / 100
    values["Short_Term_Loans2"] = values["Short_Term_Loans"]
    values["Income_Taxes_Payable2"] = values["Income_Taxes_Payable"]
    values["Accrued_Salary_Wages2"] = values["Accrued_Salary_Wages"] * (
            100 + 12 * values["Increase_Percentage_in_Sales2"]) / 100
    values["Unearned_Revenue2"] = values["Unearned_Revenue"]
    values["Current_Portion_of_Long_Term_Debt2"] = values["Current_Portion_of_Long_Term_Debt"]
    values["Long_Term_Debt2"] = values["Long_Term_Debt"] * (
            100 + values["Increase_Percentage_in_Investment2"] * 12) / 100
    values["Deferred_Income_Tax2"] = values["Deferred_Income_Tax"]
    values["Others3"] = values["Others"]
    values["Owners_Investment2"] = values["Owners_Investment"] * (
            100 + values["Increase_Percentage_in_Sales2"] * 12) / 100
    values["Others4"] = values["Others2"]
    values["Retained_Earnings2"] = values["Total_Assets2"] - (
            values["Accounts_Payable2"] + values["Short_Term_Loans2"] + values["Income_Taxes_Payable2"] +
            values["Accrued_Salary_Wages2"] + values["Unearned_Revenue2"] + values[
                "Current_Portion_of_Long_Term_Debt2"] +
            values["Long_Term_Debt2"] + values["Deferred_Income_Tax2"] + values["Others3"] +
            values["Owners_Investment2"] + values["Others4"])

    values["Total_Current_Liabilities2"] = (values["Accounts_Payable2"] + values["Short_Term_Loans2"] +
                                            values["Income_Taxes_Payable2"] + values["Accrued_Salary_Wages2"] +
                                            values["Unearned_Revenue2"] + values["Current_Portion_of_Long_Term_Debt2"])
    values["Total_Long_Term_Liabilities2"] = values["Long_Term_Debt2"] + values["Deferred_Income_Tax2"] + values[
        "Others3"]
    values["Total_Owner_Equity2"] = (values["Owners_Investment2"] + values["Others4"] + values["Retained_Earnings2"])

    # LIABILITIES and OWNER's EQUITY (in INR) - FY - 3
    values["Accounts_Payable3"] = values["Accounts_Payable2"] * (
            100 + values["Increase_Percentage_in_Sales3"] * 12) / 100
    values["Short_Term_Loans3"] = values["Short_Term_Loans2"]
    values["Income_Taxes_Payable3"] = values["Income_Taxes_Payable2"]
    values["Accrued_Salary_Wages3"] = values["Accrued_Salary_Wages2"] * (
            100 + 12 * values["Increase_Percentage_in_Sales3"]) / 100
    values["Unearned_Revenue3"] = values["Unearned_Revenue2"]
    values["Current_Portion_of_Long_Term_Debt3"] = values["Current_Portion_of_Long_Term_Debt2"]
    values["Long_Term_Debt3"] = values["Long_Term_Debt2"] * (
            100 + values["Increase_Percentage_in_Investment3"] * 12) / 100
    values["Deferred_Income_Tax3"] = values["Deferred_Income_Tax2"]
    values["Others5"] = values["Others3"]
    values["Owners_Investment3"] = values["Owners_Investment2"] * (
            100 + values["Increase_Percentage_in_Sales3"] * 12) / 100
    values["Others6"] = values["Others4"]

    values["Retained_Earnings3"] = values["Total_Assets3"] - (
            values["Accounts_Payable3"] + values["Short_Term_Loans3"] + values["Income_Taxes_Payable3"] +
            values["Accrued_Salary_Wages3"] + values["Unearned_Revenue3"] + values[
                "Current_Portion_of_Long_Term_Debt3"] +
            values["Long_Term_Debt3"] + values["Deferred_Income_Tax3"] + values["Others5"] +
            values["Owners_Investment3"] + values["Others6"])

    values["Total_Current_Liabilities3"] = (values["Accounts_Payable3"] + values["Short_Term_Loans3"] +
                                            values["Income_Taxes_Payable3"] + values["Accrued_Salary_Wages3"] +
                                            values["Unearned_Revenue3"] + values["Current_Portion_of_Long_Term_Debt3"])
    values["Total_Long_Term_Liabilities3"] = (
            values["Long_Term_Debt3"] + values["Deferred_Income_Tax3"] + values["Others5"])
    values["Total_Owner_Equity3"] = (values["Owners_Investment3"] + values["Others6"] + values["Retained_Earnings3"])

    # Particulars - FY - 1
    values["Net_Sales"] = values["Total_Sale_Amount_Month"] * 12
    values["Cost_of_Sales"] = (
                                      values["Marketing_Expenses_Month"]
                                      + values["Software_Operating_Expenses_Month"]
                                      + values["Hardware_Machine_Operating_Expenses_Month"]
                              ) * 12
    values["Selling_Operating_Expenses"] = values["Total_Staff_Salary_Month"] * 12
    values["General_Administration_Expenses"] = (
                                                        values["Office_Rent_Month"]
                                                        + values["Auditor_Expenses_Month"]
                                                        + values["Electricity_Expenses_Month"]
                                                        + values["Internet_Expenses_Month"]
                                                ) * 12
    values["Operating_Income"] = 0
    values["Other_Income"] = 0.00
    values["Gain_Loss_on_Financial_Instruments"] = 100000
    values["Loss_Gain_on_Foreign_Currency"] = 0.00
    values["Interest_Expenses"] = 0.00
    values["Income_Tax_Expense"] = 0
    values["Net_Income"] = 0

    values["Gross_Profit"] = values["Net_Sales"] + values["Cost_of_Sales"]
    values["Total_Operating_Expenses"] = (
            values["Selling_Operating_Expenses"] + values["General_Administration_Expenses"]
    )
    values["Operating_Incomes"] = (
            values["Gross_Profit"] - values["Total_Operating_Expenses"]
    )
    values["Income_Before_Taxes"] = (values["Operating_Incomes"] + values["Other_Income"] + values[
        "Gain_Loss_on_Financial_Instruments"]) - values["Loss_Gain_on_Foreign_Currency"] - values["Interest_Expenses"]

    values["Income_Tax_Expenses"] = 0.00
    values["Net_Incomes"] = (
            values["Income_Before_Taxes"] - values["Income_Tax_Expenses"]
    )

    # Particulars - FY - 2
    values["Net_Sales2"] = values["Net_Sales"] * (
            (100 + values["Increase_Percentage_in_Sales2"] * 12) / 100
    )
    values["Cost_of_Sales2"] = values["Cost_of_Sales"] * (
            (100 + values["Increase_Percentage_in_Sales2"] * 12) / 100
    )
    values["Selling_Operating_Expenses2"] = values["Selling_Operating_Expenses"] * (
            (100 + values["Increase_Percentage_in_Investment2"] * 12) / 100
    )
    values["General_Administration_Expenses2"] = values[
                                                     "General_Administration_Expenses"
                                                 ] * ((100 + values["Increase_Percentage_in_Sales2"] * 12) / 100)
    values["Operating_Income2"] = 0
    values["Other_Income2"] = 0.00
    values["Gain_Loss_on_Financial_Instruments2"] = values[
                                                        "Gain_Loss_on_Financial_Instruments"
                                                    ] * ((100 + values["Increase_Percentage_in_Sales2"] * 12) / 100)
    values["Loss_Gain_on_Foreign_Currency2"] = 0.00
    values["Interest_Expenses2"] = 0.00
    values["Income_Tax_Expense2"] = 0
    values["Net_Income2"] = 0

    values["Gross_Profit2"] = values["Net_Sales2"] + values["Cost_of_Sales2"]
    values["Total_Operating_Expenses2"] = (
            values["Selling_Operating_Expenses2"]
            + values["General_Administration_Expenses2"]
    )
    values["Operating_Incomes2"] = (
            values["Gross_Profit2"] - values["Total_Operating_Expenses2"]
    )
    values["Income_Before_Taxes2"] = (
            values["Operating_Incomes2"]
            + values["Other_Income2"]
            + values["Gain_Loss_on_Financial_Instruments2"]
            - values["Loss_Gain_on_Foreign_Currency2"]
            - values["Interest_Expenses2"]
    )
    values["Income_Tax_Expenses2"] = 0.00
    values["Net_Incomes2"] = (
            values["Income_Before_Taxes2"] - values["Income_Tax_Expenses2"]
    )

    # Particulars - FY - 3
    values["Net_Sales3"] = values["Net_Sales2"] * (
            (100 + values["Increase_Percentage_in_Sales3"] * 12) / 100
    )
    values["Cost_of_Sales3"] = values["Cost_of_Sales2"] * (
            (100 + values["Increase_Percentage_in_Sales3"] * 12) / 100
    )
    values["Selling_Operating_Expenses3"] = values["Selling_Operating_Expenses2"] * (
            (100 + values["Increase_Percentage_in_Investment3"] * 12) / 100
    )
    values["General_Administration_Expenses3"] = values[
                                                     "General_Administration_Expenses2"
                                                 ] * ((100 + values["Increase_Percentage_in_Sales3"] * 12) / 100)
    values["Operating_Income3"] = 0
    values["Other_Income3"] = 0.00
    values["Gain_Loss_on_Financial_Instruments3"] = values[
                                                        "Gain_Loss_on_Financial_Instruments2"
                                                    ] * ((100 + values["Increase_Percentage_in_Sales3"] * 12) / 100)
    values["Loss_Gain_on_Foreign_Currency3"] = 0.00
    values["Interest_Expenses3"] = 0.00
    values["Income_Tax_Expense3"] = 0
    values["Net_Income3"] = 0

    values["Gross_Profit3"] = values["Net_Sales3"] + values["Cost_of_Sales3"]
    values["Total_Operating_Expenses3"] = (
            values["Selling_Operating_Expenses3"]
            + values["General_Administration_Expenses3"]
    )
    values["Operating_Incomes3"] = (
            values["Gross_Profit3"] - values["Total_Operating_Expenses3"]
    )
    values["Income_Before_Taxes3"] = (
            values["Operating_Incomes3"]
            + values["Other_Income3"]
            + values["Gain_Loss_on_Financial_Instruments3"]
            - values["Loss_Gain_on_Foreign_Currency3"]
            - values["Interest_Expenses3"]
    )
    values["Income_Tax_Expenses3"] = 0.00
    values["Net_Incomes3"] = (
            values["Income_Before_Taxes3"] - values["Income_Tax_Expenses3"]
    )

    # Common Financial Ratios - FY - 1
    values["Debt_Ratio_FY1"] = (
                                       values["Total_Current_Liabilities"] + values["Total_Long_Term_Liabilities"]
                               ) / values["Total_Assets"]
    values["Current_Ratio_FY1"] = (
            values["Total_Current_Assets"] / values["Total_Current_Liabilities"]
    )
    values["Working_Capital_FY1"] = (
            values["Total_Current_Assets"] - values["Total_Current_Liabilities"]
    )
    values["Assets_to_Equity_Ratio_FY1"] = (
            values["Total_Assets"] / values["Total_Owner_Equity"]
    )
    values["Debt_to_Equity_Ratio_FY1"] = (
                                                 values["Total_Current_Liabilities"] + values[
                                             "Total_Long_Term_Liabilities"]
                                         ) / values["Total_Owner_Equity"]

    # Common Financial Ratios - FY - 2
    values["Debt_Ratio_FY2"] = (
                                       values["Total_Current_Liabilities2"] + values["Total_Long_Term_Liabilities2"]
                               ) / values["Total_Assets2"]
    values["Current_Ratio_FY2"] = (
            values["Total_Current_Assets2"] / values["Total_Current_Liabilities2"]
    )
    values["Working_Capital_FY2"] = (
            values["Total_Current_Assets2"] - values["Total_Current_Liabilities2"]
    )
    values["Assets_to_Equity_Ratio_FY2"] = (
            values["Total_Assets2"] / values["Total_Owner_Equity2"]
    )
    values["Debt_to_Equity_Ratio_FY2"] = (
                                                 values["Total_Current_Liabilities2"] + values[
                                             "Total_Long_Term_Liabilities2"]
                                         ) / values["Total_Owner_Equity2"]

    # Common Financial Ratios - FY - 3
    values["Debt_Ratio_FY3"] = (
                                       values["Total_Current_Liabilities3"] + values["Total_Long_Term_Liabilities3"]
                               ) / values["Total_Assets3"]
    values["Current_Ratio_FY3"] = (
            values["Total_Current_Assets3"] / values["Total_Current_Liabilities3"]
    )
    values["Working_Capital_FY3"] = (
            values["Total_Current_Assets3"] - values["Total_Current_Liabilities3"]
    )
    values["Assets_to_Equity_Ratio_FY3"] = (
            values["Total_Assets3"] / values["Total_Owner_Equity3"]
    )
    values["Debt_to_Equity_Ratio_FY3"] = (
                                                 values["Total_Current_Liabilities3"] + values[
                                             "Total_Long_Term_Liabilities3"]
                                         ) / values["Total_Owner_Equity3"]
    values["Total_Liabilities_and_Owners_Equity"] = values["Total_Current_Liabilities"] + values[
        "Total_Long_Term_Liabilities"] + values["Total_Owner_Equity"]
    values["Total_Liabilities_and_Owners_Equity2"] = values["Total_Current_Liabilities2"] + values[
        "Total_Long_Term_Liabilities2"] + values["Total_Owner_Equity2"]
    values["Total_Liabilities_and_Owners_Equity3"] = values["Total_Current_Liabilities3"] + values[
        "Total_Long_Term_Liabilities3"] + values["Total_Owner_Equity3"]
    # print(values)
    return values
