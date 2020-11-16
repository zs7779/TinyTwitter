# TinyTwitter


This is a personal project with Vue/Django, trying to recreate some of Twitter's interesting functions. Technologies used: HTML, CSS, Sass, Vue.js, Webpack, Django, PostgreSQL. Deployed on AWS EC2 using Nginx and Gunicorn.  

Try the demo at https://tinytwitter.zhaosean.com/  


If you'd like to run this code on your machine, clone this directory (check out the green "Code" button), and go to it in the command line `cd <repository path>`.  
I recommend using [docker](https://docs.docker.com/engine/install/) to test run this code. If you decided to use docker, running the following commands to get the site running
```
docker build -t tinytwitter .
docker run -dp 8000:8000 tinytwitter
```
Now go to http://localhost:8000/ to check out the website running on your computer!


Alternatively we don't have to use docker, you would need to first install Python3.8.6. ([virtualenv](https://pypi.org/project/virtualenv/) strongly recommended if you already have Python on your computer) set up the site by running
```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```


Current functions:
* New Tweet
* Comment
* Retweet
* Upload image with tweet/comment
* Delete tweet
* Like/unlike
* home page
* Profile page
* Follow/unfollow user
* Modify Bio/Avatar image
* Mentions
* Hashtags
* Trending user/hashtag/tweet
* Notifications
* Infinite scroll
* Responsive page


Known issues:
* Infinite scroll sometimes not working on short screen (narrow screen landscape orientation)
* Scroll position not persisted when clicking on a post then go back
* Images and tweets containing images do not work if you run this code locally. This is because they are hosted on AWS S3 and require permission to perform some of the operations.


Credits:
* This is an extension to project https://cs50.harvard.edu/web/2020/projects/4/network/
* Demo data generated by https://mockaroo.com/  
* Demo avatars generated by https://robohash.org/  
