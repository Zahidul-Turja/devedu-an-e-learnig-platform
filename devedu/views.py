from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse

from django.contrib.auth.models import User

from django.db.models import Q

from .models import Course, CourseContent, UserProfile, Instructor, Review, ReviewCourseMiddle, Tag, CourseSession, CourseSessionMiddle
from .forms import RegistrationForm, LoginForm, CourseForm, CourseContentForm, UserProfileForm, ReviewForm

import json

import stripe

from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.utils import timezone

from django.views.decorators.csrf import csrf_exempt

# ? Remove before pushing
stripe.api_key = "sk_test_51NiXeRG2jM3ThQGknB1YyVyOXC9emp3QciLTXpq1mUGrWZo1PIiVQO3kWvoqIQ736tG24sfih9OE0XyM7zVKMVJz00NEYUbiJK"


def generate_certificate(request, username, slug):
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)
    course = Course.objects.get(slug=slug)
    contents = course.contents.all().order_by("serial")  # type: ignore
    time = timezone.now()
    template = get_template('certificates/certificate.html')
    context = {
        'user_profile': user_profile,
        'course': course,
        "contents": contents,
        'date': time,
    }
    html_content = template.render(context)

    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html_content.encode('UTF-8')), response)

    if not pdf:
        return HttpResponse('Error generating PDF', status=500)

    response = HttpResponse(response.getvalue(),
                            content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="certificate.pdf"'
    return response


def home(request):
    courses = Course.objects.all().order_by("-avg_rating")[:8]
    reviews = Review.objects.all().order_by("-rating")[:3]
    context = {
        "courses": courses,
        "reviews": reviews,
    }
    return render(request, "devedu/home.html", context)


@csrf_exempt
@login_required(login_url="/login")
def payment(request, slug, username):
    user = User.objects.get(username=username)
    if user.is_staff:
        message = "This user is a staff. Try a Student account to enroll."
        # ! redirect to the course detail page
        return redirect(reverse("payment_error", args=[message]))
    user_profile = UserProfile.objects.get(user=user)
    course = Course.objects.get(slug=slug)
    instractor = course.author
    enrolled = course.enrolled_students.all()
    if user_profile == instractor.user:  # type: ignore
        message = "This user is the Instractor of this course!"
        # ! redirect to the course detail page
        # return redirect("course_detail")
        return redirect(reverse("payment_error", args=[message]))
    if user_profile in enrolled:
        message = "User already enrolled in this course!"
        # ! redirect to the course detail page
        # return redirect("course_detail")
        return redirect(reverse("payment_error", args=[message]))

    if request.method == 'POST':
        amount = request.POST["amount"]
        formated_amount = int(amount) * 100
        customer = stripe.Customer.create(
            email=request.POST["email"],
            name=request.POST["nickname"],
            source=request.POST["stripeToken"],
        )
        des = "Purchase: " + str(course.title)
        charge = stripe.Charge.create(
            customer=customer,
            amount=formated_amount,
            currency='bdt',
            description=des
        )

        customer_id = str(customer.id)

        return redirect(reverse('enroll_course',
                                args=[slug, username, customer_id]))  # type:ignore

    user = User.objects.get(username=username)
    course = Course.objects.get(slug=slug)
    user_profile = UserProfile.objects.get(user=user)
    price = int(course.price)

    context = {
        "course": course,
        "price": price,
        "user_profile": user_profile,
        "slug": slug,
        "username": username
    }
    return render(request, "devedu/pay.html", context)


def enroll_course(request, slug, username, customer_id):
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)
    course = Course.objects.get(slug=slug)
    enrolled = course.enrolled_students.all()
    course.enrolled_students.add(user_profile)
    course.save()
    course_session = CourseSession.objects.create(
        user=user_profile)
    course_session.save()
    courseSessionMiddle = CourseSessionMiddle.objects.create(
        course=course, sessions=course_session)
    courseSessionMiddle.save()

    message = str(course.title) + " enrolled successfully."
    context = {
        "message": message,
        "course": course,
        "en_students": enrolled,
    }
    return redirect(reverse("pay_success", args=[slug, username, customer_id]))


def success(request, slug, username, customer_id):
    retrieved_customer = stripe.Customer.retrieve(customer_id)
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)
    course = Course.objects.get(slug=slug)

    context = {
        "user_profile": user_profile,
        "course": course,
        "customer": retrieved_customer,
    }
    return render(request, "devedu/pay_success.html", context)


def payment_error(request, message):
    context = {
        "message": message
    }
    return render(request, "devedu/pay_error.html", context)

# !------------------------ LOG SIGN starts ----------------------------#


@csrf_exempt
def signup(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect("home")
    else:
        form = RegistrationForm()

    context = {
        "form": form
    }
    return render(request, "registration/sign_up.html", context)


@csrf_exempt
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        user_name = request.POST.get("username")
        password1 = request.POST.get("password1")

        user = authenticate(username=user_name, password=password1)
        if user:
            login(request, user)
            return redirect("home")
    else:
        form = LoginForm()

    context = {
        "form": form
    }
    return render(request, "registration/login.html", context)

# !------------------------ LOG SIGN end ----------------------------#


# ! -----------------------------USER PROFILE AND EDIT PROFILE START---------------#
def user_profile(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        user = None
        # ! Gives error otherwist
        return render(request, "devedu/home.html", {})
    user_profile = UserProfile.objects.get(user=user)
    course_sessions = user_profile.sessions.all()  # type: ignore
    enrolled_courses = user_profile.courses.all()  # type: ignore
    context = {
        "en_courses": enrolled_courses,
        "user_profile": user_profile,
        "course_sessions": course_sessions,
    }
    return render(request, "devedu/user_profile.html", context)


# ? Check if the same user is trying to edit or not
@csrf_exempt
def edit_profile(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        user = None
        # ! Gives error otherwist
        return render(request, "devedu/home.html", {})
    user_profile = UserProfile.objects.get(user=user)
    user_profile_form = UserProfileForm(instance=user_profile)
    if request.method == "POST":
        user_profile_form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile)
        if user_profile_form.is_valid():
            user_profile_form.save()
            return HttpResponseRedirect(reverse("user_profile", args=[username]))

    context = {
        "user_profile": user_profile,
        "user_profile_form": user_profile_form
    }
    return render(request, "devedu/edit_profile.html", context)


def teaching(request, username):
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)

    if not user_profile.is_instructor:
        return redirect(reverse("apply", args=[username]))

    instructor = Instructor.objects.get(user=user_profile)
    courses = Course.objects.filter(author=instructor)
    context = {
        "courses": courses,
        "instructor": instructor,
    }
    return render(request, "devedu/teaching.html", context)

# ! -----------------------USER PROFILE AND EDIT PROFILE END-------------------------#


# ! ----------------------------COURSE DETAIL starts-----------------#

def course_detail(request, slug):
    course = Course.objects.get(slug=slug)
    contents = course.contents.all().order_by("serial")  # type: ignore
    reviews = course.reviews.all().order_by("-review__rating")  # type: ignore
    try:
        free_content = contents.filter(is_free=True)[0]
    except:
        free_content = ""
    enrolled_students = course.enrolled_students.all()

    reviewers = []
    for r in reviews:
        reviewers.append(r.review.author.user)

    en_students = []
    for stu in enrolled_students:
        en_students.append(stu.user)
    context = {
        "course": course,
        "contents": contents,
        "reviews": reviews,
        "tot_reviews": len(reviewers),
        "free_content": free_content,
        "en_students": en_students,
    }
    return render(request, "devedu/course_detail.html", context)


def all_courses(request):
    courses = Course.objects.all().order_by("-avg_rating")
    context = {
        "courses": courses,
    }
    return render(request, "devedu/all_courses.html", context)


def learning(request, username, slug):
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)
    course = Course.objects.get(slug=slug)
    contents = course.contents.all().order_by("serial")  # type: ignore

    try:
        course_session = CourseSession.objects.filter(
            user=user_profile)

    except:
        course_session = "bell"
        courseMiddle = 'hell'
    try:
        free_content = contents.filter(is_free=True)[0]
    except:
        free_content = ''
    context = {
        "user_profile": user_profile,
        "course_session": course_session,
        "course": course,
        "contents": contents,
        "free_content": free_content
    }
    return render(request, "devedu/learning.html", context)


def session_update(request, username, slug, serial, vid_dur):
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)
    course = Course.objects.get(slug=slug)
    course_session = CourseSession.objects.filter(user=user_profile)
    for c in course_session:
        if c.session.course.slug == slug:  # type: ignore
            print(c.session.course.slug)  # type: ignore
            print(serial, vid_dur)
            c.complete_serial = int(serial) - 1
            c.current_serial = int(serial)
            c.video_duration = int(float(vid_dur))
            c.save()

    context = {

    }
    return JsonResponse(context)

# ! ------------------------------COURSE DETAIL ends---------------------#


# ! ------------------------------ Search Start ---------------------#
def search(request):
    query = request.GET.get("q")
    if query:
        courses = Course.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(author__user__first_name__icontains=query) |
            Q(author__user__last_name__icontains=query)).order_by("-avg_rating")
    else:
        courses = Course.objects.all().order_by("-avg_rating")

    context = {
        "courses": courses,
        "query": query,
    }
    return render(request, "devedu/all_courses.html", context)


def filter(request):
    query = request.GET.get("query")
    filter = request.GET.get("filter")
    sort = request.GET.get("sort")

    if query == "all-courses":
        courses = Course.objects.all()
    else:
        courses = Course.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(author__user__first_name__icontains=query) |
            Q(author__user__last_name__icontains=query))

    if filter != "all-courses":
        tag = Tag.objects.filter(caption=filter)
        courses = courses.filter(tags__in=tag)

    courses = courses.values(
        'title', 'author', 'description', 'thumb_nail', 'price', 'slug', 'avg_rating')
    courses = list(courses.order_by(sort))

    serialized_courses = json.dumps(courses)

    context = {
        "courses": serialized_courses,
        "query": query,
    }

    return JsonResponse(context)


def get_author(request):
    author = Instructor.objects.get(pk=request.GET.get("id")).user
    username = author.user.username
    first_name = author.first_name
    last_name = author.last_name

    context = {
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
    }
    return JsonResponse(context)


def search_tags(request, tag):
    tag_object = Tag.objects.filter(caption=tag)
    courses = Course.objects.all().filter(tags__in=tag_object)

    context = {
        "courses": courses,
        "tag": tag,
    }
    return render(request, "devedu/search_tags.html", context)


def search_user(request, slug):
    if request.GET:
        query = request.GET.get("q")
        user_profiles = UserProfile.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(about__icontains=query) |
            Q(user__username__icontains=query))
    else:
        query = False
        user_profiles = UserProfile.objects.all()[:10]
    context = {
        "user_profiles": user_profiles,
        "query": query,
        "slug": slug
    }
    return render(request, "devedu/search_user.html", context)

# ! ------------------------------ Search ends---------------------#


# ! ------------------------------ REVIEW STARTS ---------------------#
@csrf_exempt
def review(request, slug, username):
    user = User.objects.get(username=username)
    userProfile = UserProfile.objects.get(user=user)
    review_form = ReviewForm()
    course = Course.objects.get(slug=slug)
    reviews = course.reviews.all().order_by("-review__rating")  # type: ignore

    reviewers = []
    for r in reviews:
        reviewers.append(r.review.author.user)

    enrolled_students = course.enrolled_students.all()
    en_students = []
    for stu in enrolled_students:
        en_students.append(stu.user)

    if request.method == "POST":
        if user in en_students and not user in reviewers:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.author = userProfile
                review.save()
                reviewMid = ReviewCourseMiddle.objects.create(
                    course=course, review=review)
                all_reviews = course.reviews.all()  # type:ignore
                tot_rating = 0
                for r in all_reviews:
                    tot_rating += r.review.rating
                course.avg_rating = tot_rating / len(all_reviews)
                course.save()
                return redirect(reverse("review", args=[slug, username]))
        else:
            return redirect("home")

    context = {
        "course": course,
        "reviews": reviews,
        "review_form": review_form,
        "reviewers": reviewers,
        "tot_reviews": len(reviewers),
        # "avg_rating": avg_rating,
    }
    return render(request, "devedu/review.html", context)

# ! ------------------------------ REVIEW ENDS -----------------------#


# ! --------------------------------Application-------------------------------#
@csrf_exempt
@login_required(login_url="/login")
def apply(request, username):
    user = User.objects.get(username=username)
    user_form = UserProfileForm()

    if not user.is_staff:
        user_profile = UserProfile.objects.get(user=user)
        if request.method == "POST":
            user_form = UserProfileForm(
                request.POST, request.FILES, instance=user_profile)
            if user_form.is_valid():
                user_profile.applied = True
                user_profile.save()
                user_form.save()
                return redirect("home")
        else:
            user_form = UserProfileForm(instance=user_profile)
    else:
        user_profile = False
    context = {
        "user_profile": user_profile,
        "user_form": user_form,
    }
    return render(request, "devedu/apply.html", context)
# ! ------------------------------Application Ends----------------------------#


# ? ALL ADMIN PANEL BELOW START
def admin_dashboard(request):
    courses = Course.objects.all()
    context = {
        "courses": courses
    }
    return render(request, "admin/dashboard.html", context)


#! --------------------------------- Add Starts ------------------------------------#
# ? Check permissions before deleting

@csrf_exempt
def add_new_course(request):
    if request.method == "POST":
        course = CourseForm(request.POST, request.FILES)

        if course.is_valid():
            course.save()
            id = Course.objects.get(title=request.POST.get("title"))
            return add_contents(request, id.id)  # type: ignore
    else:
        course = CourseForm()

    context = {
        "course": course
    }
    return render(request, "admin/add_course.html", context)

# ? Check permissions before deleting


@csrf_exempt
def add_contents(request, id):
    course = Course.objects.get(pk=id)

    if request.method == "POST":
        content_form = CourseContentForm(request.POST, request.FILES)

        if content_form.is_valid():
            content = content_form.save(commit=False)
            content.course = course
            content.save()

        return HttpResponseRedirect(reverse("add_content", args=[id]))

    context = {
        "course": course,
        "contents": course.contents.all(),  # type: ignore
        "content_form": CourseContentForm()
    }

    return render(request, "admin/add_contents.html", context)

# ! -------------------------------- Add Ends -------------------------------#


# ! -------------------------------- Edits start ------------------------------#
# ? Check permissions before deleting
@csrf_exempt
def edit_course(request, id):
    course = Course.objects.get(pk=id)
    course_form = CourseForm(instance=course)
    # ! all() gives multiple contents so it wouldn't work like that
    contents = course.contents.all()  # type: ignore
    # content_form = CourseContentForm(instance=content)

    if request.method == "POST":
        course_form = CourseForm(request.POST, request.FILES, instance=course)
        if course_form.is_valid():
            course_form.save()
            return HttpResponseRedirect(reverse("edit_course", args=[id]))

    context = {
        "course": course,
        "course_form": course_form,
        "contents": contents,
        # "content_form": content_form
    }

    return render(request, "admin/edit_course.html", context)


# ? Check permissions before deleting
@csrf_exempt
def edit_content(request, id):
    content = CourseContent.objects.get(pk=id)
    content_form = CourseContentForm(instance=content)
    course = Course.objects.get(contents=content)

    if request.method == "POST":
        content_form = CourseContentForm(
            request.POST, request.FILES, instance=content)
        if content_form.is_valid():
            content_form.save()
            # HttpResponseRedirect(reverse("edit_content", args=[id]))

            return redirect(
                reverse("edit_course", args=[course.id])  # type: ignore
            )
    context = {
        "course": course,
        "content": content,
        "content_form": content_form
    }
    return render(request, "admin/edit_content.html", context)

# ! Edits Ends


# !----------------------- DELETE STARTS----------------------------#
# ? Check permissions before deleting
@csrf_exempt
def delete_course(request, id):
    course = Course.objects.get(pk=id)

    if request.method == "POST":
        course.delete()
        return redirect("admin_dashboard")

    context = {
        "course": course
    }

    return render(request, "admin/delete_course.html", context)


# ? Check permissions before deleting
@csrf_exempt
def delete_content(request, id):
    content = CourseContent.objects.get(pk=id)
    course = Course.objects.get(contents=content)

    if request.method == "POST":
        content.delete()
        return redirect(
            reverse("edit_course", args=[course.id])  # type:ignore
        )

    context = {
        "content": content
    }
    return render(request, "admin/delete_content.html", context)

# ! -------------------------------DELETE ENDS------------------------------------------#


# !----------------------------- Applications start ----------------------------#
def admin_applications(request):
    users = UserProfile.objects.filter(applied=True)
    context = {
        "users": users,
    }
    return render(request, "admin/applications.html", context)


def accept(request, username):
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)
    user_profile.is_instructor = True
    user_profile.applied = False
    user_profile.save()
    Instructor.objects.create(user=user_profile)
    return redirect("admin_applications")


def reject(request, username):
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)
    user_profile.is_instructor = False
    user_profile.applied = False
    user_profile.save()
    return redirect("admin_applications")

# !----------------------------- Applications end ----------------------------#

# !----------------------------- Instructors Start ----------------------------#


def admin_instructors(request):
    instructors = Instructor.objects.all()
    context = {
        "instructors": instructors
    }
    return render(request, "admin/instructors.html", context)


def ban_instructor(request, username):
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)
    instructor = Instructor.objects.get(user=user_profile)
    instructor.delete()
    user_profile.is_instructor = False
    user_profile.save()
    return redirect(reverse("admin_instructors"))
# !----------------------------- Instructor end -------------------------------#
# ? -----------------------------Admin panel ends---------------------------------------#
