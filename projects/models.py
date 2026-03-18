from django.db import models
import uuid
from users.models import Profile
from math import sqrt
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

# Create your models here.


class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)

    tags = models.ManyToManyField("Tag", blank=True)

    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    # rank_score = models.FloatField(default=0.0)j
    created = models.DateTimeField(auto_now_add=True)

    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', '-title']

    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ''
        return url

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner_id', flat=True)
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()
        
        ratio = (upVotes / totalVotes) * 100
        

        self.vote_total = totalVotes
        self.vote_ratio = ratio
        
        self.save()

    # chuẩn hóa link
    # def normalizeLink(self, url):
    #     if not url:
    #         return ''
    #     url = url.strip()
    #     if not url.startswith(('http://', 'https://')):
    #         url = 'https://' + url
    #     try:
    #         URLValidator()(url) #check schema, check format
    #         return url
    #     except ValidationError:
    #         return ''
        
    # def save(self, *args, **kwargs):
    #     self.demo_link = self.normalizeLink(self.demo_link)
    #     self.source_link = self.normalizeLink(self.source_link)
    #     super().save(*args, **kwargs)

class Review(models.Model):
    VOTE_TYPE = (
        ("up", "Up Vote"),
        ("down", "Down Vote"),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.name
