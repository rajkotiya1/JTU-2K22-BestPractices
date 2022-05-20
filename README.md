# Instructions
 

Git clone this repo to your PC

    $ git clone https://github.com/rajkotiya1/JTU-2K22-BestPractices.git
    
Dependencies:

Cd into your the cloned repo as such:
    $ cd JTU-2K22-BestPractices
    
requirements:
```bash
  Install the dependencies needed to run the app:
  Django==3.1.6 
  djangorestframework==3.12.2
  pytz==2019.2  
  pandas==1.4.2
  numpy==1.18.5
  django-environ==0.8.1 
```
    $ pip install -r requirements.txt
  
Make those migrations work

    $ python manage.py makemigrations
    $ python manage.py migrate

How to run on local host machine:
    $ python manage.py runserver
 after executing these command you will get an link in terminal on which application is hosted
