
from werespond.models import User, Post, Comment, PostSave, PostVote, Group, Report, Case, Achievement, UserAchievement, AchievementReward, Event, EventAttendance
from werespond.serializers import UserSerializer, PostSerializer, VoteSerializer, SaveSerializer, CommentSerializer, GroupSerializer, ReportSerializer, CaseSerializer, AchievementSerializer
from rest_framework import viewsets

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class VoteViewSet(viewsets.ModelViewSet):
    queryset = PostVote.objects.all()
    serializer_class = VoteSerializer

class SaveViewSet(viewsets.ModelViewSet):
    queryset = PostSave.objects.all()
    serializer_class = SaveSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer