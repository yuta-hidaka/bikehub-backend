from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=False):
        data = form.cleaned_data
        user.email = data.get('email')
        # user.username = data.get('username')
        # all your custom fields
        user.birthday = data.get('birthday')
        user.gender = data.get('gender')
        user.disp_name = data.get('disp_name')
        user.ubike1_by_list = data.get('ubike1_by_list')
        user.ubike2_by_list = data.get('ubike2_by_list')
        user.accept = data.get('accept')

        if 'password1' in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            user.save()
        return user