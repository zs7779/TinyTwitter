# TinyTwitter


This is a personal project using Vue/Django/PostgreSQL, recreating some of Twitter's interesting functions. Technologies used: HTML, CSS, Sass, Vue.js, Webpack, Django, PostgreSQL. Deployed on AWS EC2 using Nginx and Gunicorn.  

Try the demo at https://tinytwitter.zhaosean.com/  


If you'd like to run this code on your computer, clone this directory (check out the green "Code" button), and go to it in the command line `cd <repository path>`.  
I recommend using [docker](https://docs.docker.com/engine/install/) to test run this code. If you decided to use docker, use the following commands to get the site running:
```
docker build -t tinytwitter .
docker run -dp 8000:8000 tinytwitter
```
Now go to http://localhost:8000/ to check out the website running on your computer!


Alternatively you don't have to use docker, but you would need to first install [Python3.8.6](https://www.python.org/downloads/release/python-386/) ([virtualenv](https://pypi.org/project/virtualenv/) strongly recommended if you already have Python on your computer). Set up the site by running:
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
![Tweet Picture](demo_imgs/tweet_image.gif?raw=true "Tweet Picture") ![Retweet](demo_imgs/retweet.gif?raw=true "Retweet") ![Like and Comment](demo_imgs/like_comment.gif?raw=true "Like and Comment")
* home page
* Profile page
* Follow/unfollow user
* Modify Bio/Avatar image
* Mentions
* Hashtags
![Edit Profile](demo_imgs/edit_profile.gif?raw=true "Edit Profile") ![Follow](demo_imgs/follow.gif?raw=true "Follow") ![Hashtag and Mention](demo_imgs/hashtag_mention.gif?raw=true "Hashtag and Mention")
* Trending user/hashtag/tweet
* Notifications
* Infinite scroll
* Responsive page
![Infinite Scroll](demo_imgs/infinite_scroll.gif?raw=true "Infinite Scroll") ![Responsive Design](demo_imgs/responsive.gif?raw=true "Responsive Design")


Known issues:
* Infinite scroll sometimes not working on short screen (narrow screen landscape orientation)
* Scroll position not persisted when clicking on a post then go back
* Images uploads do not work if you run this code locally. It is because images are hosted on AWS S3 and need special permission.


Credits:
* This is an extension to project https://cs50.harvard.edu/web/2020/projects/4/network/
* Demo data generated by https://mockaroo.com/  
* Demo avatars generated by https://robohash.org/  
