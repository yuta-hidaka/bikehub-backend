from dj_rest_auth.views import UserDetailsView
from news.models import News, MainCategoryTag, SubCategoryTag, SubCategoryTagMap, TargetSite
from rest_framework import serializers
# from drf_queryfields import QueryFieldsMixin
from users.models import CustomUser
from dj_rest_auth.serializers import UserDetailsSerializer


class UserRegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'disp_name',
            'email',
            'birthday',
            'gender',
            # 'ubike1_by_list',
            # 'ubike2_by_list',
            'accept',
            'password',
            'password2',
        ]
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def save(self, request):
        user = CustomUser(
            email=self.validated_data['email'],
            username=self.validated_data['email'],
            disp_name=self.validated_data['disp_name'],
            birthday=self.validated_data['birthday'],
            gender=self.validated_data['gender'],
            # ubike1_by_list=self.validated_data['ubike1_by_list'],
            # ubike2_by_list=self.validated_data['ubike2_by_list'],
            accept=self.validated_data['accept'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user

    def clean(self):
        cd = self.cleaned_data
        fullname = "%s-%s" % (cd.get('first_name'), cd.get('last_name'))
        username = None


class UserSerializer(UserDetailsSerializer):
    # password2 = serializers.CharField(
    #     style={'input_type': 'password'}, write_only=True)

    class Meta(UserDetailsSerializer.Meta):
        model = CustomUser
        fields = [
            'disp_name',
            'email',
        ]

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userprofile', {})
        company_name = profile_data.get('company_name')

        instance = super(UserSerializer, self).update(instance, validated_data)

        # if validated_data['password'] != password2:
        #     raise serializers.ValidationError(
        #         {'password': 'Passwords must match.'})

        # get and update user profile
        instance.disp_name = validated_data['disp_name']
        instance.email = validated_data['email']
        instance.username = validated_data['email']

        instance.save()

        return instance
