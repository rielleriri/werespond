from rest_framework import serializers
from werespond.models import User, Post, PostVote, PostSave, Comment, Group, Report, Case, Achievement, UserAchievement, AchievementReward, Event

class GroupSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True) # to list out all members, many to many 
    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'members']

class CaseSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    class Meta:
        model = Case
        fields = ['case_type', 'address', 'time', 'description', 'users']

class UserSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.hp_no')
    groups = GroupSerializer(many=True, read_only=True, partial=True)
    cases = CaseSerializer(required=False, many=True, read_only=True)
    class Meta:
        model = User
        fields = ['hp_no', 'name', 'gender', 'email', 'groups', 'cases', 'created_at', 'updated_at', 'user', 'is_admin']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Comment
        fields = ['content', 'post', 'user', 'created_at']

class SaveSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = PostSave
        fields = ['post', 'user']

class VoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = PostVote
        fields = ['post', 'user']

class PostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    saves = SaveSerializer(many=True, read_only=True)
    votes = VoteSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True) # to list out all comments
    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'user', 'image', 'comments', 'votes', 'saves', 'created_at', 'updated_at']   

class ReportSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Report
        fields = ['report_type', 'description', 'location', 'image', 'user', 'created_at']

class AchievementProgressSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='achievement.id') # through model
    name = serializers.ReadOnlyField(source='achievement.name')
    class Meta:
        model = UserAchievement
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


