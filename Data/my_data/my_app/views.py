from datetime import datetime
from calendar import monthrange
from django.shortcuts import render, redirect
import plotly.graph_objs as go
from .models import Expense
from .forms import ExpenseForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

def expense_analysis(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = ExpenseForm()

    months = [i for i in range(1, 13)]
    if 'selected_month' in request.GET:
        selected_month = int(request.GET['selected_month'])
    else:
        selected_month = datetime.now().month

    _, num_days = monthrange(datetime.now().year, selected_month)

    daily_expenses = [0] * num_days

    expenses = Expense.objects.filter(date__month=selected_month)
    for expense in expenses:
        day = expense.date.day - 1
        daily_expenses[day] += expense.amount

    graph_data = go.Bar(x=list(range(1, num_days + 1)), y=daily_expenses)
    layout = go.Layout(
        title='Daily Expenses for Month ' + str(selected_month),
        xaxis={'title': 'Day'},
        yaxis={'title': 'Amount Spent'}
    )
    graph = go.Figure(data=[graph_data], layout=layout)
    graph_html = graph.to_html(full_html=False)

    return render(request, 'base.html', {'graph_html': graph_html, 'months': months, 'selected_month': selected_month, 'form': form})

def show_expenses(request):
    expenses = Expense.objects.all()
    return render(request, 'base.html', {'expenses': expenses})

def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    expense.delete()
    return redirect('expense_analysis')
