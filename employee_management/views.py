from django.shortcuts import render
from rest_framework import generics
from .models import Department, Employee
from .serializers import DepartmentSerializer, EmployeeSerializer
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.core.cache import cache

class SimplePagination(PageNumberPagination):
    page_size = 3

class DepartmentListView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class DepartmentRetrieveView(generics.RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class DepartmentDetailsView(generics.GenericAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)  
        return Response(serializer.errors, status=400)  

    def put(self, request, pk):
        department = self.get_object()
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        department = self.get_object()
        department.delete()
        return Response(status=204)

class EmployeeListView(generics.ListAPIView):
    serializer_class = EmployeeSerializer
    pagination_class = SimplePagination  

    def get_queryset(self):
        cache_key = "employee_list"
        employees = cache.get(cache_key) 
        print("cache data") 

        if not employees:  
            employees = Employee.objects.all()
            cache.set(cache_key, employees, timeout=60)  

        return employees

class EmployeeDetailsView(generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)  
        return Response(serializer.errors, status=400)  

    def put(self, request, pk):
        employee = self.get_object()
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        employee = self.get_object()
        employee.delete()
        return Response(status=204)

class EmployeeFilterView(generics.ListAPIView):
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        queryset = Employee.objects.all()
        dept_id = self.request.query_params.get('department')
        min_salary = self.request.query_params.get('min_salary')
        max_salary = self.request.query_params.get('max_salary')

        if dept_id:
            queryset = queryset.filter(department_id=dept_id)
        if min_salary:
            queryset = queryset.filter(salary__gte=min_salary)
        if max_salary:
            queryset = queryset.filter(salary__lte=max_salary)

        return queryset
