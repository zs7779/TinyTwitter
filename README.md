# TinyTwitter


This is a personal project with Vue/Django/Postgres, trying to reacreate some of Twitter's interesting functions.

Try the demo at https://tinytwitter.zhaosean.com/
**This website for demo only, it's content is not moderated and could be periodically purged!**


If you'd like to run this code on your machine, clone this directory (check out the green "Code" button), and go to it in the command line `cd <repository path>`. 

I recommend using [docker](https://docs.docker.com/engine/install/) to test run this code. If you decided to use docker, running the following commands to get the site running
```
docker build -t tinytwitter .
docker run -dp 8000:8000 tinytwitter
```
Now go to http://localhost:8000/ to check out the website running on your machine!


Alternatively we don't have to use docker, you would need to first install Python3.8.6. ([virtualenv](https://pypi.org/project/virtualenv/) strongly recommended if you already have Python on your computer) set up the site by running
```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Note the current setting in the master branch is not suitable for deployment! It is for testing only! Do not deploy as is and do not store personal information (such as your usual password)!**


Current functions:
* New Post
* Comment
* Retweet
* Delete post
* Like/unlike
* home page
* Profile page
* Follow/unfollow user
* Mentions
* Hashtags
* Notifications
* Infinite scroll
* Mobile compatible page


Planned functions:
* User avatar
* Image upload with tweet
* New follow suggestion
* Trending hashtags posts
* Fall back page for 404/No content


Twitter functions currently not planned:
* Editable username
* Video/larger media upload with tweet
* Block user/tweet
* Events/Polls/Emojis
* Live update
* Direct messages
* Bookmarks
* Lists
* Auto complete on Mentions and Hashtags


Known bugs:
* Infinite scroll sometimes not working on short screen (narrow screen landscape orientation)
* Scroll position not persisted when clicking on a post then go back