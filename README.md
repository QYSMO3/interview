# A simple Interview Time Arrangement API
This is a simple API service that could help arrange a interview's time for some users. This project is for **personal practice**.
copyright @ Chemondis

## Setup Instructions
1.	Pull the code
2.	Install the dependency based on requirements.py
3.	Change the database settings. Modify the **/interview_api/settings.py** at line 80, database name, username and password.
4.	Sync the databases by running `python manage.py makemigrations` and `python manage.py migrate`
5.	run the server using `python manage.py runserver`
6.	Go to `http://127.0.0.1:8000/index` to see the webpage (by default)

## Setup Instructions
Detailed description with picture could be seen from the user manual. Basicly, to test the API, 
1. Some users need to be created first. 
2. Each involved user's available time need to be created then.
3. User's role(cadidate/interviewer) need to be specified.
4. The API could then be tested by clicting **Test the API** button or **Arrange an interview** button. the first button would only send the request to get available time slots, while the second one would arrange a interview for the first alailable time. 
5. The arranged interview could then be shown on each user's detailed time page.
6. Django's build in admin site is also good to manage the date. `http://127.0.0.1:8000/admin`. To access the admin page, a superuser is needed. `python manage.py createsuperuser`

## License
See [LICENSE](LICENSE).
