from rest.serializer.users import UserReadonlySerializer
from rest_framework import serializers

from sell_bike.models import (Company, CompanyGroup, CompanyUserGroup,
                              Evaluation)


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = [
            'evaluation_id',
            'company',
            'user',
            'star',
            'description',
            'created_at',
            'updated_at',
        ]
        

class CompanyGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyGroup
        fields = [
            'company_group_id',
            'company',
            'user',
            'permissions',
            'created_at',
            'updated_at',
        ]


class CompanyUserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyUserGroup
        fields = [
            'company_group_id',
            'company',
            'user',
            'permissions',
            'created_at',
            'updated_at',
        ]


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'company_id',
            'name',
            'stripe_customer_id',
            'plan',
            'admin',
            'address',
            'email',
            'phone',
            'post_code',
            'description',
            'prefecture',
            'url',
            'is_child',
            'created_at',
            'updated_at'
        ]
