from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField(label='نام کاربری')
    password = forms.CharField(widget=forms.PasswordInput,label='کلمه عبور')

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        # user_qs = User.objects.filter(username=username)
        # if user_qs.count() == 1:
        #     user = user_qs.first()
        if username and password:

            if not User.objects.filter(username=username).exists():
                raise forms.ValidationError("نام کاربری وارد شده وجود ندارد")

            user = authenticate(username=username, password=password)
                # raise forms.ValidationError("This user does not exist")
            if not user:
                raise forms.ValidationError("کلمه عبور نادرست است")
                # raise forms.ValidationError("Incorrect passsword")
            if not user.is_active:
                raise forms.ValidationError("نام کاربری غیرفعال است")
                # raise forms.ValidationError("This user is not longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)