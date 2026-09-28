# from django.shortcuts import render
# from rest_framework.viewsets import ViewSet,ModelViewSet
# from expense.serializers import UserSerializer
# from expense.serializers import ExpenseSerializer
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.authentication import BasicAuthentication
# from rest_framework.permissions  import IsAuthenticated,AllowAny

# # Create your views here.

# class UserViewSet(ViewSet):
#     def create(self,request):
#         dser=UserSerializer(data=request.data)
#         if dser.is_valid():
#             dser.save()
#             # dser.object.create_user(**dser.validated_data)
#             return Response(data=dser.data,status=status.HTTP_201_CREATED)
#         return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)

# class ExpenseView(ViewSet):
#     authentication_classes=[BasicAuthentication]
#     permission_classes=[IsAuthenticated]
#     def create(self,request):
#         dser=ExpenseSerializer(data=request.data)
#         if dser.is_valid():
#             dser.save(owner=request.user)
#             return Response(data=dser.data,status=status.HTTP_201_CREATED)
#         return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)



from django.shortcuts import render
from expense.serializers import UserSerializer,ExpenseSerializer
from expense.models import Expenses
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated ,AllowAny
from django.utils import timezone
from django.db.models import Sum
from expense.permissions import isOwner
# Create your views here

class SignUpViewset(ViewSet):
    def create(self,request):
        dser=UserSerializer(data=request.data)
        if dser.is_valid():
            User.objects.create_user(**dser.validated_data)
            return Response(data=dser.data,status=status.HTTP_201_CREATED)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ExpenseView(ViewSet):
    authentication_classes=[TokenAuthentication]
    # permission_classes=[IsAuthenticated]
    permission_classes=[isOwner]
    def create(self,request):
        dser=ExpenseSerializer(data=request.data)
        if dser.is_valid():
            dser.save(owner=request.user)
            return Response(data=dser.data,status=status.HTTP_201_CREATED)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)

    def list(self,request):
        exp=Expenses.objects.filter(owner=request.user)
        ser=ExpenseSerializer(exp,many=True)
        return Response(data=ser.data,status=status.HTTP_200_OK)

    def retrieve(self,request,pk=0):
        pro_id=pk
        inven=Expenses.objects.get(id=pro_id)
        ser=ExpenseSerializer(inven)
        return Response (data=ser.data)

    def destroy(self,request,pk=0):
        Expenses.objects.get(id=pk).delete()
        return Response(data={"msg":"deleted!!"})

    def update(self,request,pk=0):
        exp=Expenses.objects.get(id=pk)
        dser=ExpenseSerializer(data=request.data,instance=exp,)
        if dser.is_valid():
            dser.save()
            return Response(data=dser.data)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self,request,pk=0):
        exp=Expenses.objects.get(id=pk)
        dser=ExpenseSerializer(data=request.data,instance=exp,partial=True)
        if dser.is_valid():
            dser.save()
            return Response(data=dser.data)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)


class ExpenseSummeryView(APIView):
    authentication_classes=[TokenAuthentication]
    # permission_classes=[IsAuthenticated]
    permission_classes=[isOwner]
    def get(self,request,**kwargs):
        cur_date=timezone.now()
        cur_month=cur_date.month
        cur_year=cur_date.year
        print(cur_month,cur_year)
        data=Expenses.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year=cur_year)
        category_summary=data.values('category').annotate(Sum('amount'))
        cat_summary=[summary for summary in category_summary]
        for i in category_summary:
            print(i)
        print(cat_summary) 
        total_expenses=data.values('category').annotate(Sum('amount'))
        print(total_expenses)
        context={
            "total_expense":total_expenses,
            "category_summary" :cat_summary      }
        return Response (data=context)

    

            
