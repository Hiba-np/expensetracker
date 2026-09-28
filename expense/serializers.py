from rest_framework import serializers
from expense.models import Expenses
from django.contrib.auth.models import User

class UserSerializer(serializers.Serializer):
    id=serializers.CharField(read_only=True)
    username=serializers.CharField()
    email=serializers.CharField()
    password=serializers.CharField()



# class  UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=User
#         fields=['username','password','email']
#         read_only_fields=['id'],
#         def create(self,validated_data):
#             return User.objects.create_user(**validated_data)

    

class ExpenseSerializer(serializers.ModelSerializer):
     # owner=serializers.StringRelatedField(read_only=True)

    greeting=serializers.SerializerMethodField()
    owner=serializers.SerializerMethodField()
    class Meta:
        model=Expenses
        fields='__all__'
        read_only_fields=['id','created_at','owner']
    def get_greeting(self,obj):
                return " Hi Welcome to expense tracker"
    def get_owner(self,obj):
                return obj.owner.username