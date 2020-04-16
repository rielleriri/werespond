from rest_framework import serializers
from werespond.models import User, Response, Post, PostVote, PostSave, Comment, Group, Report, Case, Achievement, UserAchievement, AchievementReward, Event, EventAttendance, UserCertificate, CertificateForm

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['hp_no', 'name', 'gender', 'email', 'groups', 'cases', 'created_at', 'updated_at', 'user', 'is_admin']

class GroupSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True) # to list out all members, many to many 
    #members = MemberSerializer(many=True)
    class Meta:
        model = Group
        fields = ['id', 'name', 'profile_pic', 'display_pic', 'email', 'website', 'description', 'members']

class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['id', 'user', 'case']

class CaseSerializer(serializers.ModelSerializer):
    users = ResponseSerializer(read_only=True, many=True, required=False)
    class Meta:
        model = Case
        fields = ['case_type', 'location', 'lattitude', 'longitude', 'time', 'description', 'users']
 
class UserSerializer(serializers.ModelSerializer):
     user = serializers.ReadOnlyField(source='user.hp_no')
     groups = GroupSerializer(many=True, read_only=True, partial=True)
     cases = CaseSerializer(required=False, many=True, read_only=True)
     class Meta:
         model = User
         fields = ['hp_no', 'name', 'gender', 'email', 'groups', 'cases', 'created_at', 'updated_at', 'user', 'is_admin']

# class UserSerializer(WritableNestedModelSerializer):
#     groups = GroupSerializer(many=True)
#     cases = CaseSerializer(many=True)
#     class Meta:
#         model = User
#         fields = ['hp_no', 'name', 'gender', 'email', 'groups', 'cases', 'created_at', 'updated_at', 'is_admin']

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['hp_no', 'name', 'gender','is_admin']

class PostBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'body', 'user', 'group', 'image', 'comments', 'votes', 'saves', 'created_at', 'updated_at']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'post', 'user', 'created_at']
    # def create(self, validated_data):
    #     return Comment.objects.create(**validated_data)

class SaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostSave
        fields = ['post', 'user']

class SaveListSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    class Meta:
        model = PostSave
        fields = ['user']

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVote
        fields = ['post', 'user']

class VoteListSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    class Meta:
        model = PostVote
        fields = ['user']

class PostSerializer(serializers.ModelSerializer):
    saves = SaveSerializer(read_only=True, many=True, required=False)
    votes = VoteSerializer(read_only=True, many=True, required=False)
    comments = CommentSerializer(read_only=True, many=True, required=False) # to list out all comments
    class Meta:
        model = Post
        fields = ['id', 'body', 'image', 'user', 'group', 'comments', 'votes', 'saves', 'created_at', 'updated_at']   

class PostListSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)
    group = GroupListSerializer(read_only=True)
    saves = SaveListSerializer(many=True, read_only=True)
    votes = VoteListSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True) # to list out all comments
    class Meta:
        model = Post
        fields = ['id', 'body', 'user', 'group', 'image', 'comments', 'votes', 'saves', 'created_at', 'updated_at']    

class ReportSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Report
        fields = ['report_type', 'description', 'location', 'image', 'user', 'created_at']

class UserAchievementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserAchievement
        fields = ['id', 'user', 'date_awarded']

class AchievementSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    class Meta:
        model = Achievement
        fields = ['id', 'name', 'condition', 'users', 'created_at']

    def get_users(self, obj):
        qset = UserAchievement.objects.filter()

class AchievementRewardSerializer(serializers.ModelSerializer): #one to one rs 
    achievement = AchievementSerializer(read_only=True)
    class Meta:
        model = AchievementReward
        fields = ['achievement', 'reward']

class EventAttendanceSerializer(serializers.ModelSerializer):
    event = serializers.ReadOnlyField(source='event.id')
    user = serializers.ReadOnlyField(source='user.hp_no')
    class Meta:
        model = EventAttendance 
        fields = ['id', 'event', 'user', 'attendance']

class EventSerializer(serializers.ModelSerializer):
    users = EventAttendanceSerializer(source='eventattendance_set', many=True)
    #users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    class Meta:
        model = Event
        fields = ['id', 'image', 'name', 'description', 'date', 'time', 'venue', 'slots', 'users']

class UserCertificateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = UserCertificate
        fields = ['id', 'user', 'cert_type', 'expiry', 'awarded_at']

class CertificateFormSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = CertificateForm
        fields = ['id', 'user', 'certificate', 'image', 'expiry', 'created_at']
