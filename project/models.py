from django.db import models

class Project(models.Model):
    team_name = models.CharField(max_length=100)
    team_members = models.CharField(max_length=255)  # 여러 팀원의 이름을 문자열로 저장
    code = models.FileField(upload_to='')  # MEDIA_ROOT 아래에 직접 저장되도록 설정
    score = models.FloatField(default=0.0)
    comment = models.TextField(blank=True)  # 기존 댓글 필드는 유지 또는 제거 가능 (선택 사항)

    def __str__(self):
        return self.team_name


class Comment(models.Model):
    project = models.ForeignKey(Project, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()  # 댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 댓글 생성 시간

    def __str__(self):
        return f"Comment on {self.project.team_name}"
