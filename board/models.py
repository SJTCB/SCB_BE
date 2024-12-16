
# from django.db import models

# # Create your models here.
# # class Board(models.Model):
# #     school_id=models.CharField(max_length=10, unique=True)
# #     title = models.CharField(max_length=30)
# #     content = models.TextField("내용", null=False)
# #     date_created = models.DateTimeField("작성일", auto_now_add=True, null=False)

# class Board(models.Model):
#     school_id = models.CharField(max_length=10, unique=True)
#     title = models.CharField(max_length=30)
#     content = models.TextField("내용", null=False)
#     date_created = models.DateTimeField("작성일", auto_now_add=True, null=False)

from django.db import models
from django.utils.timezone import now

class Board(models.Model):
    school_id = models.CharField("학번", max_length=10, unique=True)  # 학번
    title = models.CharField("제목", max_length=100)  # 제목
    content = models.TextField("내용", null=False)  # 내용
    date_created = models.DateTimeField("작성일", auto_now_add=True, null=False)  # 작성일
    date_updated = models.DateTimeField("수정일", auto_now=True)  # 수정일

    def __str__(self):
        return f"{self.title} ({self.school_id})"

class Comment(models.Model):
    board = models.ForeignKey(Board, related_name='comments', on_delete=models.CASCADE)  # Board와 연결
    author = models.CharField("작성자", max_length=100, blank=True)  # 댓글 작성자
    text = models.TextField("댓글 내용", null=False)  # 댓글 내용
    created_at = models.DateTimeField("작성일", auto_now_add=True)  # 댓글 작성일
    updated_at = models.DateTimeField("수정일", auto_now=True)  # 댓글 수정일

    def __str__(self):
        return f"Comment on {self.board.title} by {self.author or 'Anonymous'}"
