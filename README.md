# E-Learning
Project description. Not ready yet 🥲.

Prototype (PC version): [Figma](https://www.figma.com/proto/P7KJUS52tvFb0pHoYMIyUT/DevEdu?page-id=0%3A1&type=design&node-id=1-2&viewport=228%2C259%2C0.18&t=dBVIQA5i7xh7V8kp-1&scaling=scale-down-width&starting-point-node-id=1%3A2&mode=design)
**Note:** Please go to the `Options` dropdown located in the top right and select `Fit to width` option. It might take a while depending on your internet speed.
___
## Dependencies
* Python: Install python's latest version [link](https://www.python.org/downloads/).
* Django: Locally install django using command: 
    ```
    python -m pip install Django
    ```
    more details [here](https://docs.djangoproject.com/en/4.2/howto/windows/).
* Pillow: Install Pillow using command:
    ```
    python -m pip install Pillow
    ``` 
___
## Runnig the Website on Local Server
* Download the Download.zip file and extract.
* Open terminal and Go to that folder where `manage.py` file is located.
* Run command
    ```
    python manage.py runserver
    ```
* An URL similar to `http://127.0.0.1:8000/` will be given.
* Open this link in your browser.
> **Notes:** please uninstall any code formatter like `Prettier` if you have any installed in your code editor.

___
## User Information
Check the `notes.txt` file located in the same folder as `manage.py` for already existing users information.
> **Note:** Only the user with the username of admin has the access to admin panel.


___
## Features
* Can sign up with `username`, `email` and `password`.
* Login with `username` and `password`.
* User is identified either User, Instructor or Admin automatically and the UI as well as permissions changes accordingly. 
* Admins can create a course and upload both video and pdf files.
* Admins can edit and delete the whole course as well as contents if necessary.

#### Work in Progress
* User can apply as an Instructor and only the admin can approve the application and if approved, User will be upgraded to Instructor type which allows to create and delete their own courses, and modify them as well.
* User can upload profile image and edit their profile informations.
* Users can enroll to courses by paying.
* User will have an wishlist where the can save courses.
* One User can gift course to another User.
* **Offer:** when an User sign up, two courses `Programming Fundamental with C` and `Data Structures` will be gifted to them.
