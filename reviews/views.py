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
            review.save()
            messages.success(request, "리뷰 작성이 완료되었습니다.")
            return redirect("reviews:index")
    else:
        review_form = ReviewForm()
    context = {"review_form": review_form, "item_title": request.GET.get("item_title")}
    return render(request, "reviews/form.html", context=context)


@login_required
def delete(request, pk):
    review = Review.objects.get(pk=pk)
    if request.method == "POST":
        review.delete()
        return redirect("reviews:index")
    context = {"review": review}
    return render(request, "reviews/detail.html", context)


def detail(request, pk):
    review = get_object_or_404(Review, pk=pk)

    comment_form = CommentForm()
    # template에 객체 전달
    context = {
        "review": review,
        "comments": review.comment_set.all(),
        "comment_form": comment_form,
    }
    return render(request, "reviews/detail.html", context)


@login_required
def update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user == review.user:
        if request.method == "POST":
            review_form = ReviewForm(request.POST, request.FILES, instance=review)
            if review_form.is_valid():
                review_form.save()
                messages.success(request, "리뷰가 수정되었습니다.")
                return redirect("reviews:detail", review.pk)
        else:
            review_form = ReviewForm(instance=review)
        context = {"review_form": review_form}
        return render(request, "reviews/form.html", context)
    else:
        messages.warning(request, "작성자만 수정할 수 있습니다.")
        return redirect("reviews:detail", review.pk)


# 좋아요
@require_POST
def like(request, pk):
    review = get_object_or_404(Review, pk=pk)
    # print('hi') 요청 확인 위함
    # 만약 로그인한 유저(request.user)가 이 글을 좋아요 눌렀다면,
    if request.user in review.like_users.all():
        # 좋아요 삭제하고
        review.like_users.remove(request.user)
        is_liked = False
    else:  # 좋아요 누르지 않은 상태라면 좋아요에 추가하고
        review.like_users.add(request.user)
        is_liked = True
        # 상세 페이지로 redirect
    context = {"isLiked": is_liked, "likeCount": review.like_users.count()}
    return JsonResponse(context)
