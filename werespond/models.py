from __future__ import unicode_literals
from django.db import models

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
        through='Response',
        through_fields=('case','user') ,
        related_name='cases',
        blank=True
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

class Response(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    case = models.ForeignKey('Case', on_delete=models.CASCADE)
    response = models.BooleanField("Did User Respond?", default=False)
    arrival_time = models.DateField("User Responded At", auto_now_add=True)

    class Meta:
        ordering = ('id',)

class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Group Name", max_length=50)
    description = models.CharField("Group Description", max_length=100)
    created_at= models.DateTimeField("Group Created At", auto_now_add=True, editable=True)
    updated_at = models.DateTimeField("Group Updated At", auto_now=True, editable=True) #default setting editable=False, blank=True
    members = models.ManyToManyField(User, related_name='groups')

    class Meta:
        ordering = ('id',) 

    def __unicode__(self):
        return unicode(self.name)

    def display_members(self):
        """Create a string for the User. This is required to display members in Admin."""
        return ', '.join(members.name for members in self.members.all()[:3])
    
    display_members.short_description = 'Members'

class Membership(models.Model):
    member = models.ForeignKey('User', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="posts")
    title = models.CharField('Post Title', max_length=60, default='Title')
    body = models.CharField("Post Body", max_length=600)
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, null=True)
    created_at= models.DateTimeField("Group Created At", auto_now_add=True, editable=True)
    updated_at = models.DateTimeField("Group Updated At", auto_now=True, editable=True) #default setting editable=False, blank=True

    class Meta:
        ordering = ('id',) 

    def was_posted_today(self):
        return self.created_at.date() == datetime.date.today()

class Save(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    is_saved = models.BooleanField

    class Meta:
        ordering = ('id',)
    
class PostAccess(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    is_group = models.BooleanField

    class Meta:
        ordering = ('id',) 

class Vote(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="votes_user")

    class Meta:
        ordering = ('id',)

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
        through='AchievementProgress',
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

class AchievementProgress(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    achievement = models.ForeignKey('Achievement', on_delete=models.CASCADE)
    awarded = models.DateTimeField(auto_now=True, editable=True)

    class Meta:
        ordering = ('id',)

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Event Name", max_length=50)
    details = models.CharField("Event Details", max_length=500)
    time = models.DateTimeField("Event Time", auto_now=False, auto_now_add=False)
    organisers = models.CharField("Event Organisers", max_length=200)
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

class Certificate(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, null=False)
    expiry = models.DateField("User Cert Expiry")
    CERT_TYPES = (
        ('c', 'CPR'),
        ('a', 'AED'),
        ('b', 'CPR+AED'),
        ('s', 'Standard First Aid'),
        ('o', 'Occupational First Aid'),
        ('p', 'Psychological First Aid'),
        ('f', 'Fire Safety')
    )
    cert_type = models.CharField(
        "Cert Type",
        max_length=1,
        choices=CERT_TYPES,
    )
    users = models.ManyToManyField(
        User, 
        through='UserCertificate',
        through_fields=('certificate','user') ,
        related_name='certificates',
        blank=True
    )   
    submitted = models.DateTimeField(auto_now=True, editable=True)

    class Meta:
        ordering = ('id',)

class UserCertificate(models.Model):
    id = models.AutoField(primary_key=True)
    certificate = models.ForeignKey('Certificate', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    awarded = models.DateTimeField(auto_now=True, editable=True)
    expiry = models.DateField("User Cert Expiry")
    CERT_TYPES = (
        ('c', 'CPR'),
        ('a', 'AED'),
        ('b', 'CPR+AED'),
        ('s', 'Standard First Aid'),
        ('o', 'Occupational First Aid'),
        ('p', 'Psychological First Aid'),
        ('f', 'Fire Safety')
    )
    cert_type = models.CharField(
        "Cert Type",
        max_length=1,
        choices=CERT_TYPES,
    )

    class Meta:
        ordering = ('id',)

class QuizQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField("Quiz Qns", max_length=400)

    class Meta:
        ordering = ('id',)

class QuizChoice(models.Model):
    id = models.AutoField(primary_key=True)
    correct = models.BooleanField("Correct Ans")
    question = models.ForeignKey('QuizQuestion', on_delete=models.CASCADE)
    choice = models.CharField("Choice", max_length=500)

    class Meta:
        ordering = ('id',)

class QuizUserAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    question = models.ForeignKey('QuizQuestion', on_delete=models.CASCADE)
    question_choice = models.ForeignKey('QuizChoice', on_delete=models.CASCADE)
    is_right = models.BooleanField

    class Meta:
        ordering = ('id',)