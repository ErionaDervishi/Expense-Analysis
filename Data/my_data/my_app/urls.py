from django.urls import path
from . import views



urlpatterns = [
    path('', views.expense_analysis, name='expense_analysis'),
    path('delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('expenses/',views.show_expenses, name='show_expenses'),
    ]