from django.shortcuts import render
from django.views import View


class ExpenseGroupView(View):
    """
    Expense Group View
    """
    template_name = "expense/expense.html"

    def get(self, request, workspace_id):
        context = {"expense_groups_tab": "active", "expense_groups": "active"}
        return render(request, self.template_name, context)
