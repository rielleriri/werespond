from __future__ import unicode_literals
from django.db import models
import datetime as dt

# Create your models here.
class User(models.Model):
    """Model representing a user account."""
    hp_no = models.IntegerField("User Hp No.", unique=True, primary_key=True) #max length ignored when used with int
    name = models.CharField("User Full Name", max_length=60)
    GENDER_TYPES =(
        ('m', 'Male'),
        ('f', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_TYPES)
    is_admin = models.BooleanField("Admin User?", default=False)
    email = models.EmailField("User Email", max_length=254, null=True)
    created_at= models.DateTimeField("User Created At", auto_now_add=True, editable=True)
    updated_at = models.DateTimeField("User Updated At", auto_now=True, editable=True) #default setting editable=False, blank=True
    
    class Meta:
        ordering = ('hp_no',) 

    def create(self, validated_data):
        groups_data = validated_data.pop('groups')
        user = User.objects.create(**validated_data)
        for group_data in groups_data:
            # Group.objects.create(user=user, **group_data)
            user.groups.add(group_data)
        return user

    def __str__(self):
        return '%s' % (self.name)

class Report(models.Model):
    #id primary key auto added if not specified
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE) #one-to-many rs
    location = models.CharField("Report Location", max_length=250)
    description = models.CharField("Report Description", max_length=250)
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, null=True)
    created_at = models.DateTimeField("Report submitted at", auto_now_add=True, editable=True)

    REPORT_TYPES = (
        ('c', 'Cardiac Arrest'),
        ('f', 'Fire Report'),
        ('h', 'Fire Hazard')
    )

    report_type = models.CharField(
        max_length=1,
        choices = REPORT_TYPES,
    )

    class Meta:
        ordering = ('id',)

class Case(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField("Case Address", max_length=600)
    time = models.DateField("Time of Case", auto_now_add=True, editable=True)
    description = models.CharField("Case Description", max_length=600)
    id_required = models.BooleanField("ID Required?", default=True)
    updated_at = models.DateTimeField("Case Updated At", auto_now=True, editable=True) #default setting editable=False, blank=True
    #many-to-many rs
    users = models.ManyToManyField(
        User, 
        related_name='cases',
    )

    CASE_TYPES = (
        ('c', 'Cardiac Arrest'),
        ('f', 'Fire Case'),
    )

    case_type = models.CharField(
        "Case Type",
        max_length=1,
        choices=CASE_TYPES,
    )

    class Meta:
        ordering = ('id',) 
    
    def __unicode__(self):
       return unicode(self.description)
# a case can be shown to many users 

class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Group Name", max_length=50)
    description = models.CharField("Group Description", max_length=100)
    created_at= models.DateTimeField("Group Created At", auto_now_add=True, editable=True)
    updated_at = models.DateTimeField("Group Updated At", auto_now=True, editable=True) #default setting editable=False, blank=True
    members = models.ManyToManyField(User, related_name='groups')

    class Meta:
        ordering = ('id',) 

#membership

class PostSave(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name='saves', on_delete=models.CASCADE)
    is_saved = models.BooleanField(default=True)

    class Meta:
        ordering = ('id',)

class PostVote(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="votes_user")
    post = models.ForeignKey('Post', related_name='votes', on_delete=models.CASCADE)
    is_voted = models.BooleanField(default=True)

    class Meta:
        ordering = ('id',)

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="post_user")
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    title = models.CharField('Post Title', max_length=60, default='Title')
    body = models.CharField("Post Body", max_length=600)
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, null=True)
    created_at= models.DateTimeField("Created At", auto_now_add=True, editable=True)
    updated_at = models.DateTimeField("Updated At", auto_now=True, editable=True) #default setting editable=False, blank=True

    class Meta:
        ordering = ('id',) 

    def was_posted_today(self):
        return self.created_at.date() == datetime.date.today()

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey('User', related_name='comment_user', on_delete=models.CASCADE)
    content = models.CharField(max_length=140)
    created_at= models.DateTimeField(auto_now_add=True, editable=True)

    class Meta:
        ordering = ('id',)

class Achievement(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Achievement Name', max_length=50)
    condition = models.CharField('Achievement Condition', max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, editable=True)
    users = models.ManyToManyField(
        User, 
        through='UserAchievement',
        through_fields=('achievement','user') ,
        related_name='achievements',
        blank=True
    )    

    class Meta:
        ordering = ('id',)

class AchievementReward(models.Model):
    achievement = models.OneToOneField('Achievement', on_delete=models.CASCADE, primary_key=True)
    reward = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, null=True)

    class Meta:
        ordering = ('achievement',)

class UserAchievement(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    achievement = models.ForeignKey('Achievement', on_delete=models.CASCADE)
    date_awarded = models.DateTimeField(auto_now=True, editable=True)

    class Meta:
        ordering = ('id',)

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Event Name", max_length=50)
    details = models.CharField("Event Details", max_length=500)
    time = models.DateTimeField("Event Time", auto_now=False, auto_now_add=False)
    organisers = models.CharField("Event Organisers", max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, editable=True)
    users = models.ManyToManyField(
        User,
        through='EventAttendance',
        through_fields=('event','user') ,
        related_name='events',
        blank=True
    )    

    class Meta:
        ordering = ('id',)

class EventAttendance(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    attendance = models.BooleanField("Event Attendance")

    class Meta:
        ordering = ('id',)

class CertificateForm(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=True)   
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    CERT_TYPES = (
        ('c', 'CPR'),
        ('a', 'AED'),
        ('b', 'CPR+AED'),
        ('s', 'Standard First Aid'),
        ('o', 'Occupational First Aid'),
        ('p', 'Psychological First Aid'),
        ('f', 'Fire Safety')
    )
    certificate = models.CharField(
        "Cert Type",
        max_length=1,
        choices=CERT_TYPES,
    )
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, null=True)
    expiry = models.DateField("Cert Expiry")

    class Meta:
        ordering = ('id',)

class UserCertificate(models.Model):
    id = models.AutoField(primary_key=True)
    OPTIONS = (
        ('c', 'CPR'),
        ('a', 'AED'),
        ('b', 'CPR+AED'),
        ('s', 'Standard First Aid'),
        ('o', 'Occupational First Aid'),
        ('p', 'Psychological First Aid'),
        ('f', 'Fire Safety')
    )
    cert_type = models.CharField(
        "User Cert Type",
        max_length=1,
        choices=OPTIONS,
    )
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    expiry = models.DateField("User Cert Expiry")
    awarded_at = models.DateTimeField(auto_now_add=True, editable=True)

    class Meta:
        ordering = ('id',)

class QuizQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField("Quiz Qns", max_length=400)

    class Meta:
        ordering = ('id',)

class QuizChoice(models.Model):
    id = models.AutoField(primary_key=True)
    is_correct = models.BooleanField("Correct Ans")
    question = models.ForeignKey('QuizQuestion', on_delete=models.CASCADE)
    choice = models.CharField("Choice", max_length=500)

    class Meta:
        ordering = ('id',)

class QuizUserAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    question = models.ForeignKey('QuizQuestion', on_delete=models.CASCADE)
    question_choice = models.ForeignKey('QuizChoice', on_delete=models.CASCADE)
    point_awarded = models.BooleanField

    class Meta:
        ordering = ('id',)