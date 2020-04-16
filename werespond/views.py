
from werespond.models import User, Post, Comment, PostSave, PostVote, Group, Report, Case, UserCertificate, CertificateForm, Achievement, UserAchievement, AchievementReward, Event, EventAttendance
from werespond.serializers import UserSerializer, UserListSerializer, EventSerializer, PostListSerializer, PostSerializer, VoteSerializer, UserCertificateSerializer, EventAttendanceSerializer, CertificateFormSerializer, SaveSerializer, CommentSerializer, GroupSerializer, ReportSerializer, CaseSerializer, AchievementSerializer, UserAchievementSerializer, AchievementRewardSerializer
from rest_framework import viewsets

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

class EventAttendanceViewSet(viewsets.ModelViewSet):
    queryset = EventAttendance.objects.all()
    serializer_class = EventAttendanceSerializer

