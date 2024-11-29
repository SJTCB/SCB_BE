#project models.py

from django.db import models


class Project(models.Model):
    team_name = models.CharField(max_length=100)
    team_members = models.CharField(max_length=255)
    code = models.BinaryField()  # ZIP 파일 데이터를 저장
    zip_name = models.CharField(max_length=255, blank=True)  # ZIP 파일 이름 저장
    score = models.FloatField(default=0.0)
    comment = models.TextField(blank=True)  # 사용자가 입력하는 내용

    def __str__(self):
        return self.team_name




class Comment(models.Model):
    project = models.ForeignKey(Project, related_name='comments', on_delete=models.CASCADE)  # Project와 연결
    text = models.TextField()  # 댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 댓글 작성 시간

    def __str__(self):
        return f"Comment on {self.project.team_name} by {self.id}"
