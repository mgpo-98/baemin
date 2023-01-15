from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_safe
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review, Comment
from reviews.forms import ReviewForm, CommentForm
from django.core.paginator import Paginator
from django.db.models import Count


@require_safe
def index(request):
    reviews = Review.objects.order_by("-pk")
    request.GET.get("shop_name")
    context = {
        "reviews": reviews,
    }
    return render(request, "reviews/index.html", context)


@login_required  # 로그인 한경우만 리뷰 작성 가능
def create(request, item_id):
    item_title = request.GET.get("item_title")
    print(request.GET.get("item_title"))
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            # 로그인한 유저 => 작성자네!
            review.user = request.user
            review.item_id = item_id
            review.item_title = item_title
            review.save()
            messages.success(request, "리뷰 작성이 완료되었습니다.")
            return redirect("reviews:index")
    else:
        review_form = ReviewForm()
    context = {"review_form": review_form, "item_title": request.GET.get("item_title")}
    return render(request, "reviews/form.html", context=context)
