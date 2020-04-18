from werespond.models import User, Post, Comment, PostSave, PostVote, Group, Report, Case, CertificateForm, Achievement, UserAchievement, AchievementReward, Event, UserCertificate
from werespond.serializers import UserSerializer, UserListSerializer, EventSerializer, PostListSerializer, PostSerializer, VoteSerializer, CertificateFormSerializer, UserCertificateSerializer, SaveSerializer, CommentSerializer, GroupSerializer, ReportSerializer, CaseSerializer, AchievementSerializer, UserAchievementSerializer, AchievementRewardSerializer
from rest_framework import viewsets
from url_filter.integrations.drf import DjangoFilterBackend

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserListViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

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

class PostListViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['user', 'group']

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['members']

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer

class AchievementRewardViewSet(viewsets.ModelViewSet):
    queryset = AchievementReward.objects.all()
    serializer_class = AchievementRewardSerializer

class UserAchievementViewSet(viewsets.ModelViewSet):
    queryset = UserAchievement.objects.all()
    serializer_class = UserAchievementSerializer

class CertificateFormViewSet(viewsets.ModelViewSet):
    queryset = CertificateForm.objects.all()
    serializer_class = CertificateFormSerializer

class UserCertificateViewSet(viewsets.ModelViewSet):
    queryset = UserCertificate.objects.all()
    serializer_class = UserCertificateSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['users', 'date']
