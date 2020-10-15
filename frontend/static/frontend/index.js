const URLS = {
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


Vue.component("refresh-button", {
    template: `
    <div class="my-2 text-center">
        <button class="btn btn-outline-primary btn-sm border-transparent" type="button" v-on:click="$emit('refresh')">
            <b-icon icon="arrow-clockwise"></b-icon>
        </button>
    </div>
    `,
})


Vue.component("post-feed", {
    props: ['posts'],
    template: `
    <div class="post-feed">
        <slot></slot>
        <transition-group name="list">
            <post-card
                v-for="(post, index) in posts"
                v-bind:key="post.id" v-bind:post="post"
                v-on="$listeners" v-on:edit-ok="$emit('edit!')">
            </post-card>
        </transition-group>
    </div>
    `,
})


Vue.component('post-card', {
    props: ['post'],
    data: function() {
        return {
            editMode: false,
        };
    },
    methods: {
        onLike: function(event) {
            token = getToken();
            if (!token) {return;}
            axios.put(`${URLS.write_post}${this.post.id}`, {
                like: !this.post.liked,
            }, {
                headers: {
                    'X-CSRFTOKEN': token,
                },
            }).then(response => {
                const post = {
                    ...this.post,
                    like_count: this.post.liked ? this.post.like_count - 1 : this.post.like_count + 1,
                    liked: !this.post.liked,
                }
                this.$emit("edit-ok", post);
            }, printError)
        },
        onEdit: function(postText) {
            token = getToken();
            if (!token) {return;}
            axios.put(`${URLS.write_post}${this.post.id}`, {
                postText: postText,
            }, {
                headers: {
                    'X-CSRFTOKEN': token,
                },
            }).then(response => {
                const post = {
                    ...this.post,
                    text: postText,
                }
                this.$emit("edit-ok", post);
                this.editMode = false;
            }, printError)
        },
        onDelete: function(event) {
            token = getToken();
            if (!token) {return;}
            axios.delete(`${URLS.write_post}${this.post.id}`, {
                headers: {
                    'X-CSRFTOKEN': token,
                },
            }).then(response => {
                this.$emit("delete-ok", this.post.id);
            }, printError)
        },
    },
    template: `
    <div class="card p-3">
        <new-post v-if="editMode" v-bind:oldPost="post" v-bind:noPost="true" v-on:post-ok="onEdit($event)">
            <button type="button" class="btn btn-outline-secondary rounded-pill py-0" v-on:click.prevent="editMode=false">Cancel</button>
        </new-post>
        <router-link :to='{name: "post", params: {username: post.author.username, post_id: post.id}}' tag='div' class="card-text card-view" v-else>
            <h6 class="card-title mb-1">
                <router-link :to="{ name: 'user', params: {username: post.author.username} }">{{ post.author.username }}</router-link>
                <span class="small text-muted">at {{ post.create_time }} said:</span>
            </h6>
            <p>{{ post.text }}</p>
        </router-link>
        <div class="card-footer bg-transparent p-0">
            {{ post.like_count }} likes
        </div>
        <div class="card-footer bg-transparent p-0">
            <div class="d-flex justify-content-around">
                <button type="button" class="btn btn-transparent px-1 py-0" title="Comment">
                    <b-icon icon="chat" class="card-button"></b-icon>
                </button>
                <button type="button" class="btn btn-transparent px-1 py-0" title="Repost">
                    <b-icon icon="arrow-repeat" class="card-button"></b-icon>
                </button>
                <button type="button" class="btn btn-transparent px-1 py-0" title="Like" v-on:click="onLike">
                    <b-icon icon="heart" v-bind:class="[post.liked ? 'card-button-active' : 'card-button', '']"></b-icon> {{ post.like_count }}
                </button>
                <b-dropdown id="dropdown-dropup" dropup variant="btn btn-transparent px-1 py-0" no-caret title="Options">
                    <template v-slot:button-content><b-icon icon="chevron-up" class="card-button"></b-icon></template>
                    <b-dropdown-item v-if="post.owner" v-on:click="onDelete"><b-icon icon="x" class="card-button"></b-icon> Delete</b-dropdown-item>
                    <b-dropdown-item v-if="post.owner" v-on:click="editMode=true"><b-icon icon="pencil" class="card-button"></b-icon> Edit</b-dropdown-item>
                    <b-dropdown-item><b-icon icon="share" class="card-button"></b-icon> Share</b-dropdown-item>
                </b-dropdown>
            </div>
        </div>
    </div>
    `,
})


Vue.component("new-post", {
    props: {
        oldPost: {
            type: Object,
            default: function() {
                return {
                    id: null,
                    text: "",
                }
            },
        },
        noPost: {
            type: Boolean,
            default: function() {
                return false;
            },
        },
    },
    data: function() {
        return {
            postID: this.oldPost.id,
            postText: this.oldPost.text,
        };
    },
    computed: {
        charRemaining: function() {
            this.postText = this.postText.substr(0, 140);
            return `${this.postText.length}/140`;
        },
    },
    methods: {
        onSubmitPost: function (event) {
            if (this.postText.length == 0) {return;}
            token = getToken();
            if (!token) {return;}
            if (this.noPost) {
                this.$emit("post-ok", this.postText);
            } else {
                axios.post(`${URLS.write_posts}`, {
                    postText: this.postText,
                }, {
                    headers: {
                        'X-CSRFTOKEN': token,
                    },
                }).then(response => {
                    this.postText = "";
                    this.$emit("post-ok");
                }, printError)
            }
        },
    },
    template: `
    <div class="card p-3">
        <form v-on:submit.prevent="onSubmitPost">
            <textarea rows=4 class="form-control border-0" v-model="postText" placeholder="Say something..."></textarea>
            <div class="d-flex justify-content-end mt-2">
                <span class="mx-1">{{ charRemaining }}</span>
                <button type="submit" class="btn btn-primary rounded-pill py-0">Post</button>
                <slot></slot>
            </div>
        </form>
    </div>
    `,
})


Vue.component("user-profile", {
    props: ["user"],
    methods: {
        onFollow: function() {
            token = getToken();
            if (!token) {return;}
            axios.post(`${URLS.write_user}${this.user.username}`, {
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
                this.$emit("user-ok", user);
            }, printError)
        }
    },
    template: `
    <div class="card p-3 mb-2">
        <h5 class="card-title">{{ user.username }}</h5>
        <div class="row justify-content-between mx-1">
            <div>
                <span class="small text-muted">@{{ user.id }}</span>
            </div>
            <div v-if="user.owner===false">
                <button type="button" v-if="user.following" class="btn btn-primary rounded-pill" v-on:click="onFollow" v-on:hover="">Following</button>
                <button type="button" v-else class="btn btn-outline-primary rounded-pill" v-on:click="onFollow">Follow</button>
            </div>
        </div>

        <div class="card-footer bg-transparent p-0">
            <p class="mx-1">{{ user.bio }}</p>
            <span class="mx-1"><span class="font-weight-bold">{{user.following_count}}</span> Following</span>
            <span class="mx-1"><span class="font-weight-bold">{{user.follower_count}}</span> Followers</span>
        </div>
    </div>
    `,
})


const viewsMixin = {
    methods: {
        updatePost: function(editedPost) {
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


const userPostView = {
    props: ['posts', 'username', 'id'],
    template: `
        <div>
            <post-card :post="post"></post-card>
        </div>
    `,
    data: function() {
        return {
            post: {
                author: {id: null, username: 'username'},
                id: -1,
                text: "",
                create_time: null,
                like_count: null,
            },
        };
    },
    mounted: function() {
        let posts = this.posts.filter(p => p.id == this.id);
        if (posts.length !== 1) {
            axios.get(`/users/${this.username}/${this.id}`, {
                params: {
                    json: true,
                },
            }).then(response => {
                console.log(response)
                this.post = response.data;
            })
        } else {
            this.post = posts[0];
        }
    }
};

const userPostsView = {
    props: ['posts'],
    template: `
        <div>
            <post-feed v-bind:posts="posts" v-on="$listeners">
            </post-feed>
        </div>
    `,
}

const profileView = {
    props: ['username', 'post_id'],
    data: function () {
        return {
            user: {},
            posts: [],
        }
    },
    mixins: [viewsMixin],
    methods: {
        refreshView: function(query) {
            axios.get(`/users/${this.username}`, {
                params: {
                    json: true,
                    after: 0,
                    count: 20,
                },
            }).then(response => {
                console.log(response)
                this.user = response.data.user;
                this.posts = response.data.posts;
            })
        },
    },
    template: `
        <div>
            <user-profile v-bind:user="user" @user-ok="updateUser($event)"></user-profile>
            <router-view v-bind:posts="posts" :username="username" :id="post_id" name="post"></router-view>
            <router-view v-bind:posts="posts" v-on:edit-ok="updatePost($event)" v-on:delete-ok="deletePost($event)" name="posts"></router-view>
        </div>
    `,
};


const postsView = {
    props: ['all'],
    data: function () {
        return {
            posts: [],
        }
    },
    mixins: [viewsMixin],
    methods: {
        refreshView: function(query) {
            const url = this.all ? '/posts/all': '/posts/home';
            axios.get(url, {
                params: {
                    json: true,
                    after: 0,
                    count: 20,
                },
            }).then(response => {
                console.log(response)
                this.posts = response.data.posts;
            })
        },
    },
    template: `
        <div>
        <post-feed v-bind:posts="posts" v-on:edit-ok="updatePost($event)" v-on:delete-ok="deletePost($event)">
        </post-feed>
        </div>
    `,
};


const router = new VueRouter({
    mode: 'history',
    routes: [
        {path: '/', component: postsView, name: "home"},
        {path: '/all', component: postsView, props: {all: true}, name: "all"},
        {path: '/:username', component: profileView, props: true,
            children: [
                {path:'', components: {
                    posts: userPostsView,
                }, name: 'user'},
                {path:':post_id', components: {
                    post: userPostView,
                }, props:true, name: 'post'},
            ]
        },
    ]
})

const vm = new Vue({
    el: '#app',
    router,
    data: {
        pathname: window.location.pathname,
    },
    computed: {
        updatePath: function() {
            this.pathname = window.location.pathname;
        }
    },
    delimiters: ['[[', ']]'],
})