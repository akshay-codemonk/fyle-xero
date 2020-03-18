import ast

from dateutil.parser import parse
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.fyle_expense.models import ExpenseGroup, Expense
from apps.task_log.models import TaskLog
from apps.task_log.tasks import create_invoice_task
from apps.task_log.tasks_test import fetch_expenses_and_create_groups, async_create_invoice_and_post_to_xero
from apps.xero_workspace.models import CategoryMapping


class ExpenseGroupView(View):
    """
    Expense Group View
    """
    template_name = "expense/expense_group.html"

    def get(self, request, workspace_id):
        """
        Render expense group screen with necessary fields
        :param request
        :param workspace_id
        :return: render expense groups screen
        """
        context = {"expense_groups_tab": "active"}

        if request.GET.get('state') == 'complete':
            expense_groups = ExpenseGroup.objects.filter(
                workspace__id=workspace_id,
                status="Complete"
            )
            context["complete"] = "active"
        elif request.GET.get('state') == 'failed':
            expense_groups = ExpenseGroup.objects.filter(
                workspace__id=workspace_id,
                status="Failed"
            )
            context["failed"] = "active"
        else:
            expense_groups = ExpenseGroup.objects.filter(
                workspace__id=workspace_id
            )
            context["all"] = "active"

        for expense_group in expense_groups:
            expense_group.description["approved_at"] = parse(expense_group.description["approved_at"])

        page = request.GET.get('page', 1)
        paginator = Paginator(expense_groups, 10)
        try:
            expense_groups = paginator.page(page)
        except PageNotAnInteger:
            expense_groups = paginator.page(1)
        except EmptyPage:
            expense_groups = paginator.page(paginator.num_pages)

        context["expense_groups"] = expense_groups
        return render(request, self.template_name, context)

    def post(self, request, workspace_id):
        value = request.POST.get('submit')
        selected_expense_group_id = [ast.literal_eval(x) for x in request.POST.getlist('expense_group_ids')]
        if value == 'resync' and selected_expense_group_id:
            for expense_group_id in selected_expense_group_id:
                create_invoice_task(expense_group_id)
            messages.success(request, 'Resync started successfully. Expenses will be exported soon!')
        return HttpResponseRedirect(self.request.path_info)


class ExpenseGroupTaskView(APIView):
    """
    Expense Group Task view
    """
    http_method_names = ['post']

    def post(self, request, workspace_id):
        task_log = TaskLog.objects.get(id=request.data.get('task_log_id'))

        fetch_expenses_and_create_groups(workspace_id, task_log, request.user)

        return Response(status=status.HTTP_200_OK)


class ExpenseView(View):
    """
    Expense View
    """
    template_name = "expense/expense.html"

    def get(self, request, workspace_id, group_id):
        """
        Render expenses screen with necessary fields
        :param request
        :param workspace_id
        :param group_id
        :return: render expenses screen
        """
        expense_group = ExpenseGroup.objects.get(id=group_id)
        report_id = expense_group.description["report_id"]
        task_status = TaskLog.objects.filter(expense_group=expense_group).first().task.success
        expenses = expense_group.expenses.all()

        page = request.GET.get('page', 1)
        paginator = Paginator(expenses, 10)
        try:
            expenses = paginator.page(page)
        except PageNotAnInteger:
            expenses = paginator.page(1)
        except EmptyPage:
            expenses = paginator.page(paginator.num_pages)

        context = {"expense_groups_tab": "active", "expenses": expenses,
                   "report_id": report_id, "expense_group_id": expense_group.id,
                   "status": task_status}
        return render(request, self.template_name, context)


class ExpenseDetailsView(View):
    """
    Expense details view
    """

    @staticmethod
    def get(request, workspace_id, group_id, expense_id):
        """
        Return fields for expense details modal
        :param request
        :param workspace_id
        :param group_id
        :param expense_id
        :return: expense fields JSON
        """
        expense = Expense.objects.get(id=expense_id)
        expense_fields = model_to_dict(expense)
        expense_fields["category_code"] = CategoryMapping.objects.get(
            workspace__id=workspace_id, category=expense.category).account_code
        expense_fields["expense_created_at"] = expense.expense_created_at.strftime('%b. %d, %Y, %-I:%M %-p')
        expense_fields["spent_at"] = expense.spent_at.strftime('%b. %d, %Y, %-I:%M %-p')
        return JsonResponse(expense_fields)


class InvoiceDetailsView(View):
    """
    Invoice details view
    """

    @staticmethod
    def get(request, workspace_id, group_id):
        """
        Return fields for invoice details modal
        :param request
        :param workspace_id
        :param group_id
        :return: invoice fields JSON
        """
        invoice = ExpenseGroup.objects.get(id=group_id).invoice
        invoice_fields = model_to_dict(invoice)
        invoice_fields["date"] = invoice.date.strftime('%b. %d, %Y, %-I:%M %-p')
        invoice_fields["line_items"] = []
        for invoice_line_item in invoice.invoice_line_items.all():
            invoice_fields["line_items"].append(model_to_dict(invoice_line_item))
        return JsonResponse(invoice_fields)


class InvoiceTaskView(APIView):
    """
    Invoice task view
    """
    http_method_names = ['post']

    def post(self, request, workspace_id, group_id):
        task_log_id = request.data.get('task_log_id')

        expense_group = ExpenseGroup.objects.get(id=group_id)
        task_log = TaskLog.objects.get(id=task_log_id)

        async_create_invoice_and_post_to_xero(expense_group, task_log)

        return Response(status=status.HTTP_200_OK)
