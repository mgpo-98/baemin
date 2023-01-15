from django import forms
from .models import Review, Comment
from django.forms.widgets import DateInput, Textarea


class ReviewForm(forms.ModelForm):

    # title => 제목
    title = forms.CharField(
        label="제목", widget=forms.TextInput(attrs={"placeholder": "제목"})
    )
    # content => 내용
    content = forms.CharField(
        label="내용", widget=forms.TextInput(attrs={"placeholder": "내용"})
    )

    class Meta:
        model = Review
        fields = ["title", "image", "content", "order_at"]
        widgets = {
            "order_at": DateInput(attrs={"type": "date"}),
            "content": Textarea(attrs={"rows": 4}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "content",
        ]
        widgets = {"content": Textarea(attrs={"rows": 4})}
