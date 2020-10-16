const URLs = {
    posts: (postID='') => `/api/posts/${postID}`,
    users: (userID='') => `/api/users/${userID}`,
    usersPosts: (userID='', postID='') => `/api/users/${userID}/posts/${postID}`,
};

const SIGNALs = {
    updatePost: 'edit-ok',
    deletePost: 'delete-ok',
    fetchPosts: 'post-ok',
    updateUser: 'user-ok',
};

const PLACEHOLDERs = {
    user: {},
    post: {
        author: {id: -1, username: 'username'},
        id: -1,
        text: "",
        create_time: null,
        like_count: null,
    },
    posts: [],
}

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


const postsViewsMixin = {
    methods: {
        updatePost: function(editedPost) {
            if (this.post && this.post.id === editedPost.id) {
                this.post = editedPost;
            } else {
                this.posts = this.posts.map(p => p.id === editedPost.id ? editedPost : p);
            }
        },
        deletePost: function(deleteID) {
            if (this.post && this.post.id === deleteID) {
                this.post = PLACEHOLDERs.post;
            } else {
                this.posts = this.posts.filter(p => p.id !== deleteID);
            }
        },
        doLike: function(post) {
            const token = getToken();
            if (!token) return;
            axios.put(`${URLs.posts(post.id)}`, {
                like: post.liked,
            }, {
                headers: {
                    'X-CSRFTOKEN': token,
                },
            }).then(response => {
                this.updatePost(post);
            })
        },
        doEdit: function(post) {
            const token = getToken();
            if (!token) return;
            axios.put(`${URLs.posts(post.id)}`, {
                postText: post.text,
            }, {
                headers: {
                    'X-CSRFTOKEN': token,
                },
            }).then(response => {
                this.updatePost(post);
            })
        },
        doDelete: function(id) {
            const token = getToken();
            if (!token) return;
            axios.delete(`${URLs.posts(id)}`, {
                headers: {
                    'X-CSRFTOKEN': token,
                },
            }).then(response => {
                this.deletePost(id);
            })
        },
    },
};

const userViewsMixin = {
    methods: {
        updateUser: function(editedUser) {
            this.user = editedUser;
        },
        doFollow: function() {
            const token = getToken();
            if (!token) return;
            axios.post(`${URLs.users(this.user.username)}`, {
                follow: !this.user.following,
            }, {
                headers: {
                    'X-CSRFTOKEN': token,
                },
            }).then(response => {
                const user = {
                    ...this.user,
                    follower_count: this.user.following ? this.user.follower_count - 1 : this.user.follower_count + 1,
                    following: !this.user.following,
                }
                this.updateUser(user);
            })
        },
    },
};

export {
    URLs,
    SIGNALs,
    PLACEHOLDERs,
    printError,
    getToken,
    postsViewsMixin,
    userViewsMixin,
}