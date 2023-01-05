from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            "username",
            "password1",
            "password2",
            "email",
        )
        labels = {
            "username": "닉네임(아이디)",
            "password1": "비밀번호",
            "password2": "비밀번호 확인",
            "email": "이메일",
        }
