from django.db import models

class Project(models.Model):
    team_name = models.CharField(max_length=100)
    team_members = models.CharField(max_length=255)  # 여러 팀원의 이름을 문자열로 저장
    code = models.FileField(upload_to='')  # MEDIA_ROOT 아래에 직접 저장되도록 설정
    score = models.FloatField(default=0.0)
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.team_name
