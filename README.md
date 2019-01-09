# simpleWebMessanger

This project implements a simple web messenger. 
Friends are added by the phone number that
 was specified when creating the user.
Messages come immediately to all sessions of the user. Similarly, 
the messages sent will be displayed in all sessions of the user.
The project uses web sockets. Redis is chosen as a repository for messages and some information about users and existing chats.


### Start project
* `git clone https://repo.url` - clone repo
* `virtualenv venv --python=/path/to/python` - configure virtual environment
* `pip install -r requirements.txt` - install requirements
* `python manage.py migrate` - migrate database
* `python manage.py loaddata db.json` - load test database with  5 users
* `python manage.py collectstatic` - collect static files
* `python manage.py runserver` - run development server

### Usage project
* `go to 127.0.0.1:8000/chat/` - and login from one of 5 users
* username: admin
   * password: 123456
   * phone: 380955081131
* username: bob
  * password: 123456
  * phone: 380955081132
* username: liza
  * password: 123456
  * phone: 380955081133
* username: john
   * password: 123456
   * phone: 380955081134
* username: antony
  * password: 123456
  * phone: 380955081135
* add friend by mobile phone and start messaging!!!
   
   
   
      
