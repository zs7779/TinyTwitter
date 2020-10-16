const URLs = {
    read_posts: "/posts/",
    read_post: "/posts/",
    read_user: "/users/",
    write_posts: "/posts/",
    write_post: "/posts/",
    write_user: "/users/",
};

function printError(error) {
    if (error.response) {
      console.log(error.response.data);
      console.log(error.response.status);
      console.log(error.response.headers);
    } else if (error.request) {
      console.log(error.request);
    } else {
      console.log('Error', error.message);
    }
}

function getToken() {
    if (document.getElementsByName('csrfmiddlewaretoken').length > 0) {
        return document.getElementsByName('csrfmiddlewaretoken')[0].value;
    }
    window.location.href = "/login/";
    return false;
}


const viewsMixin = {
    methods: {
        updatePost: function(editedPost) {
            console.log(editedPost)
            this.posts = this.posts.map(p => p.id === editedPost.id ? editedPost : p);
        },
        deletePost: function(deleteID) {
            this.posts = this.posts.filter(p => p.id !== deleteID);
        },
        updateUser: function(editedUser) {
            this.user = editedUser;
        }
    },
    created: function () {
        this.refreshView('');
    },
    watch: {
        $route(to, from) {
            this.refreshView('');
        }
    },
};

export {
    URLs,
    printError,
    getToken,
    viewsMixin,
}