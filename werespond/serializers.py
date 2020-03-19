from rest_framework import serializers
from werespond.models import User, Membership, Post, Comment, Group, Response, Report, Case, Certificate, UserCertificate, Achievement, AchievementProgress, AchievementReward, Event, EventAttendance

class GroupSerializer(serializers.ModelSerializer):
    members = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), many=True, view_name='user-detail')
    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'members', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.hp_no')
    groups = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), many=True, view_name='group-detail')
    cases = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), many=True, view_name='case-detail')
    posts = serializers.HyperlinkedRelatedField(queryset=Post.objects.all(), many=True, view_name='post-detail')
    certificates = serializers.HyperlinkedRelatedField(queryset=Certificate.objects.all(), many=True, view_name='certificate-detail')
    achievements = serializers.HyperlinkedRelatedField(queryset=Achievement.objects.all(), many=True, view_name='achievement-detail')

    class Meta:
        model = User
        fields = ['hp_no', 'name', 'gender', 'email', 'groups', 'posts', 'achievements', 'certificates', 'cases', 'created_at', 'updated_at', 'is_admin']

class MembershipSerializer(serializers.ModelSerializer):
    member = UserSerializer(required=False)
    group = UserSerializer(required=False)
    class Meta:
        model = Membership
        fields = ('member', 'group', 'join_date')

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    class Meta:
        model = Comment
        fields = ['id', 'content', 'post', 'user', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='user-detail')
    comments = CommentSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Post
        fields = ['title', 'body', 'user', 'image', 'comments', 'created_at', 'updated_at']   

class ReportSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='user-detail')
    class Meta:
        model = Report
        fields = ['report_type', 'description', 'location', 'image', 'user', 'created_at']

class CaseSerializer(serializers.ModelSerializer):
    users = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), many=True, view_name='user-detail')
    class Meta:
        model = Case
        fields = ['case_type', 'address', 'time', 'description', 'id_required', 'updated_at', 'users']

class ResponseSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    case = CaseSerializer(required=False)
    class Meta:
        model = Response
        fields = ['id', 'user', 'case', 'response', 'arrival_time']

class AchievementSerializer(serializers.ModelSerializer):
    users = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), many=True, view_name='user-detail')
    class Meta:
        model = Achievement
        fields = ['id', 'name', 'condition', 'users', 'created_at']

class AchievementProgressSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(required=False)
    achievement = AchievementSerializer(required=False)
    class Meta:
        model = AchievementProgress
        fields = ['id', 'user', 'achievement', 'awarded']

class AchievementRewardSerializer(serializers.ModelSerializer): #one to one rs 
    achievement = AchievementSerializer(read_only=True)
    class Meta:
        model = AchievementReward
        fields = ['achievement', 'reward']

class EventSerializer(serializers.ModelSerializer):
    users = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), many=True, view_name='user-detail')
    class Meta:
        model = Event
        fields = ['id', 'name', 'details', 'time', 'organisers', 'users']

class EventAttendanceSerializer(serializers.ModelSerializer):
    event = EventSerializer(required=False)
    class Meta:
        model = EventAttendance 
        fields = ['id', 'event', 'attendance']

class CertificateSerializer(serializers.ModelSerializer):
    users = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), many=True, view_name='user-detail')
    class Meta:
        model = Certificate
        fields = ['cert_type', 'image', 'expiry', 'users', 'submitted']

class UserCertificateSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    certificate = CertificateSerializer(required=False)
    class Meta:
        model = UserCertificate
        fields = ['cert_type', 'certificate', 'user', 'awarded', 'expiry']