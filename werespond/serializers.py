from rest_framework import serializers
from werespond.models import User, Membership, Post, Comment, Group, Response, Report, Case, Achievement, AchievementProgress, AchievementReward, Event, EventAttendance

class GroupSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True) # to list out all members, many to many 
    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'members', 'created_at', 'updated_at']

class MembershipSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='group.id')
    name = serializers.ReadOnlyField(source='group.name')
    class Meta:
        model = Membership
        fields = ('id', 'name', 'join_date', )

class UserSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.hp_no')
    groups = MembershipSerializer(source='membership_set', many=True, required=False)
    cases = serializers.PrimaryKeyRelatedField(queryset=Case.objects.all(), many=True)
    class Meta:
        model = User
        fields = ['hp_no', 'name', 'gender', 'email', 'groups', 'cases', 'created_at', 'updated_at', 'user', 'is_admin']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=True)
    class Meta:
        model = Comment
        fields = ['id', 'content', 'post', 'user', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    comments = CommentSerializer(many=True, required=False, read_only=True) # to list out all comments
    class Meta:
        model = Post
        fields = ['title', 'body', 'user', 'image', 'comments', 'created_at', 'updated_at']   

class ReportSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Report
        fields = ['report_type', 'description', 'location', 'image', 'user', 'created_at']

class CaseSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    class Meta:
        model = Case
        fields = ['case_type', 'address', 'time', 'description', 'id_required', 'updated_at', 'users']

class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['id', 'user', 'case', 'response', 'arrival_time']

class AchievementProgressSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='achievement.id') # through model
    name = serializers.ReadOnlyField(source='achievement.name')
    class Meta:
        model = AchievementProgress
        fields = ['id', 'name', 'awarded']

class AchievementSerializer(serializers.ModelSerializer):
    users = AchievementProgressSerializer(source='achievementprogress_set', many=True)
    class Meta:
        model = Achievement
        fields = ['id', 'name', 'condition', 'users', 'created_at']

class AchievementRewardSerializer(serializers.ModelSerializer): #one to one rs 
    achievement = AchievementSerializer(read_only=True)
    class Meta:
        model = AchievementReward
        fields = ['achievement', 'reward']

class EventAttendanceSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='event.id')
    name = serializers.ReadOnlyField(source='event.name')
    class Meta:
        model = EventAttendance 
        fields = ['id', 'event', 'attendance']

class EventSerializer(serializers.ModelSerializer):
    users = EventAttendanceSerializer(source='eventattendance_set', many=True)
    class Meta:
        model = Event
        fields = ['id', 'name', 'details', 'time', 'organisers', 'users']


