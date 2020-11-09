# TinyTwitter


This is a personal project with Vue/Django/Postgres, trying to reacreate some of Twitter's interesting functions

Try the demo at https://tinytwitter.zhaosean.com/


If you'd like to run this code on your machine, clone this directory (check out the green "Code" button), and go to it in the command line. I highly recommend [docker and docker-compose](https://docs.docker.com/engine/install/) (docker-compose needs to be installed separately if you're not using Windows).

If you've decided to use docker-compose, create a file called .env in this directory, write in it `DJANGO_SECRET_KEY=foobar` and save. Now you can get the code up and running by the command
```
docker-compose up -d
```
After the container is running (which you can check by command `docker ps`), let's put some example data in the database by running (if you don't like test data remove the file `network/migrations/0002_test_data.py`)
```
docker exec -it <container id> python manage.py migrate
```

Alternatively if you don't like docker, you would need to install Python3.8.6. Install the dependencies ([virtualenv](https://pypi.org/project/virtualenv/) highly recommended if you already have Python on your computer) by running
```
pip install -r requirements.txt
```
Run the code
```
python manage.py migrate
python manage.py runserver
```

Now go to http://localhost:8000/ to check out the website running on your machine!


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
* Infinite scroll
* Mobile compatible page


Planned functions:
* Notifications
* User avatar
* Image upload with tweet
* New follow suggestion
* Trending hashtags posts


Twitter functions currently not planned:
* Editable username
* Video/larger media upload with tweet
* Block user/tweet
* Events/Polls/Emojis
* Live update
* Direct messages
* Bookmarks
* Lists


Known bugs:
* Infinite scroll sometimes not working on short screen (narrow screen landscape orientation)
* Scroll position not persisted when clicking on a post then go back


Todos:
* Design diagram
* Migrate to Vuex