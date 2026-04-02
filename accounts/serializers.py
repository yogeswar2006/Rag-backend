from django.contrib.auth import get_user_model
from rest_framework import serializers
from companies.serializers import CompanySerializer
from companies.models import Company


User  = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    employee_count=serializers.SerializerMethodField()
    
   
    
    
    class Meta:
        model=User
        fields=['id','email','password','first_name','last_name','role','company','employee_count']
        extra_kwargs={'password':{'write_only':True}}
        
    def get_employee_count(self,obj):
        if obj.company:
            return User.objects.filter(company=obj.company).count()
        return 0
        
    def create(self, validated_data):
        user= User.objects.create_user(**validated_data)
        return user