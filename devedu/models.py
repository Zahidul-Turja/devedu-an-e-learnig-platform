from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

from django.utils.text import slugify

# Create your models here.


class Tag(models.Model):
    caption = models.CharField(max_length=30)

    def __str__(self):
        return self.caption


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile"
    )
    first_name = models.CharField(blank=True, max_length=200)
    last_name = models.CharField(blank=True, max_length=200)
    profile_pic = models.ImageField(upload_to="profilePics", blank=True)
    about = models.TextField(validators=[MaxLengthValidator(2000)], blank=True)
    linkedin = models.URLField(blank=True, max_length=1000)
    github = models.URLField(blank=True, max_length=1000)
    mail = models.URLField(blank=True, max_length=1000)
    website = models.URLField(blank=True, max_length=1000)
    is_instructor = models.BooleanField(default=False, blank=True)
    applied = models.BooleanField(default=False, blank=True)
    resume = models.FileField(blank=True, null=True)

    def full_name(self):
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return f"{self.user.username}"

    def __str__(self):
        return self.full_name()


class Instructor(models.Model):
    user = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, blank=True, related_name="user_profile"
    )

    def __str__(self):
        return self.user.full_name()


class Review(models.Model):
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], blank=False)
    comment = models.TextField(
        validators=[MaxLengthValidator(500)], blank=True)
    author = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="reviews")
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.rating} {self.author}"


class Course(models.Model):
    title = models.CharField(unique=True, max_length=150, null=True)
    author = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, null=True, related_name="courses")
    description = models.TextField(validators=[MaxLengthValidator(3000)])
    thumb_nail = models.ImageField(upload_to="thumb_nails", null=True)
    created_on = models.DateField(auto_now_add=True)
    last_updated_on = models.DateField(auto_now=True)
    price = models.FloatField()
    slug = models.SlugField(blank=True, unique=True, null=True)
    git_repository = models.URLField(blank=True)
    quiz = models.URLField(blank=True)
    discord = models.URLField(blank=True)
    enrolled_students = models.ManyToManyField(
        UserProfile, blank=True, related_name="courses")
    avg_rating = models.FloatField(default=0, blank=True)
    tags = models.ManyToManyField(Tag)

    def save(self, *args, **kwargs):
        if not self.slug:  # Generate the slug only if it's not set yet
            self.slug = slugify(str(self.title))
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} {self.author}"


class CourseContent(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=True, related_name="contents")
    serial = models.IntegerField(null=True)
    title = models.CharField(max_length=150, null=True)
    file = models.FileField(null=True)
    is_free = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course} {self.title}"


class ReviewCourseMiddle(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="reviews"
    )
    review = models.OneToOneField(
        Review, on_delete=models.CASCADE, blank=True, related_name="review"
    )

    def __str__(self):
        return f"{self.course.title}, {self.review}"


class Wishlist(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="wishlist")
    course_slug = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.course_slug


class CourseSession(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="sessions", null=True)
    complete_serial = models.IntegerField(blank=True, default=0)
    current_serial = models.IntegerField(blank=True, default=0)
    video_duration = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} {self.complete_serial} {self.video_duration}"


class CourseSessionMiddle(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="sessions")
    sessions = models.OneToOneField(
        CourseSession, on_delete=models.CASCADE, related_name="session")

    def __str__(self):
        return f"{self.course.title} {self.sessions.user}"
