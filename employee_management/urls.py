from django.urls import path
from .views import EmployeeListView, EmployeeFilterView,EmployeeDetailsView

urlpatterns = [
    path('employees/', EmployeeListView.as_view(), name='employee-list'),  
    path('employees/filter/', EmployeeFilterView.as_view(), name='employee-filter'),
    path("employees/<int:pk>/", EmployeeDetailsView.as_view(), name="employee-detail"), 
]