# DevEdu

DevEdu is a web-application built with **Django** that offers online courses similar to Udemy. Check the [Promo](#promo-video) for detailed information.

## Table of Contents
- [Introduction](#introduction)
- [Promo video](#promo-video)
- [Features](#features)
- [Getting started](#getting-started)
- [Dependencies](#dependencies)
- [Running Locally](#runnig-on-local-server)
- [User guide](#user-guide)

___
## Introduction
DevEdu is all about online courses of Computer Science Domain. It offers courses created by admin as well as Instructors appointed by the admins.

There are currently three types of users. Admin, Student and Instructor. Students can send their CV if they want to teach in this platform and its the admin who decides to approve the application or not.

___
## Promo Video

Here is a promo video of this project which might help the user to understand the key feature of this project. Around `1 minute 22 seconds` long. 
![Watch the promo video](https://www.youtube.com/watch?v=yI3u-uOfC3w)
___
## Features
- User registration and authentication
- Course creation and management by Admin and Instructor
- Enrolling in course
- Gift course to others
- Payment handled using [Stripe API](https://stripe.com/docs/testing)
- One sample video in every course for everyone
- Search course with name, description or Instructor name
- Filter courses by price, rating and categories
- Course reviews
- User session for every course enrolled in
- Get Certificate after finishing course
- User profile and manage profile info
- Apply for Instructor position

___
## Getting Started

### Dependencies

Main dependencies are
- Python 3.6 and above
- Pillow
- Stripe
- django-xhtml2pdf

> **Note:** Check the `requirements.txt` for all packages.


### Runnig on Local Server
1. Download the Download.zip file and extract **or** clone this repository by following these steps:
    * Install `git`
    * Clone the repository:
        ```
        git clone https://github.com/Zahidul-Turja/devedu
        ```
2. Navigate to the project directory
        ```
        cd devedu
        ```
3. Install the required packages
        ```
        pip install -r requirements.txt
        ```
4. Check if you're in the same folder where `manage.py` file is located.
5. Run command
    ```
    python manage.py runserver
    ```
6. An URL similar to `http://127.0.0.1:8000/` will be given.
7. Open this link in your browser.

> **Notes:** please uninstall any code formatter like `Prettier` if you have any installed in your code editor.

___
## User Guide
1. Without Loging in:
    * User can see all available courses, sample videos for each course and reviews
    * Can search and Filter course
    * But can not enroll or gift course to anyone
    * If try to enroll, user will be redirected to `login page`
2. Sign up
    * Username have to be unique
    * Password have to contain special charecter and can't be too similar to the user name
    * Password have to match the confirm password field
3. Logged in
    * User can now enroll to course (See 4. enroll into course for detail)
    * Gift others course using the `gift` button(see 5. gift course for detail)
    * From the navigation bar user can go to their profile and edit information
    * Courses which are already enrolled will be shown there with a progress bar in the bottom of the course
    * By clicking the course from the profile page user can start learning
    * Videos will be started where you left it last time
    * If 90% of the course is finished then a `Get Certificate` button will be arrived below the progressbar for that perticular course which will generate a certificate

4. Enroll into courses
    * `Enroll` button will take the user to a payment page
    * There is a link highlighted `Stripe`
    * Click the link and this will take to a page and if scrolled down, user will find some **Dummy card** number
    * Use any card number from there
    * `MM/YY` refers to any future date. Use any future date you want i.g. **09/35**(September-2035)
    * Use random 3 digits for CVC code and random 5 digits for zip code
    * If everything was good then a success page will be redirected

5. Gift course
    * The gift button will take the user to a page where all the users are listed
    * Using the `search` field in that page user can find the person gift the course to 
    * Press the blue button along side users name and the rest of the process is similar to `4. Enroll into course`
    
    > **Note:** User can't gift the course to the Instructor of the course or someone who is already enrolled in that course

6. Review
    * After enrolling into a course user can give review about that course
    * One user can give review once to a course
    * User can find the review option in the `learning page` where user watches the video contents or the `course detail` page where the enroll button was located. After enrollment, the `Enroll` button will be replaced with `Review` button

7. Apply
    * Log in required for applying 
    * If not logged in user will be redirected to the `Login` page
    * If the user is admin or instructor then they can't apply

___
## Contributions

The illustrations used are from pinterest other than that this project has **No Contributors** yet. 
