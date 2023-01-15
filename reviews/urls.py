from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.index, name="index"),
    # 리뷰작성
    path("<int:item_id>/create/", views.create, name="create"),
    # 리뷰 상세 조회
    path("<int:pk>/", views.detail, name="detail"),
    # 리뷰 수정
    path("<int:pk>/update/", views.update, name="update"),
    # 리뷰 삭제
    path("<int:pk>/delete/", views.delete, name="delete"),
    # 리뷰 좋아요
    # path('<int:pk>/like/', views.like, name='like'),
    # 댓글 작성
    # path('<int:pk>/comments/', views.comment_create, name='comment_create'),
    # 댓글 삭제
    # path('<int:pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name ='comment_delete'),
]
