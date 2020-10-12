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
    <div class="post-feed mt-2">
        <slot></slot>
        <transition-group name="list">
            <post-card
                v-for="(post, index) in posts"
                v-bind:key="post.id" v-bind:post="post"
                v-on="$listeners">
            </post-card>
        </transition-group>
    </div>
    `,
})


Vue.component('post-card', {
    props: ['post'],
    template: `
    <div class="card p-3">
        <new-post v-if="editMode" v-bind:oldPost="post" v-bind:noPost="true" v-on:post-ok="onEdit($event)">
            <button type="button" class="btn btn-outline-secondary rounded-pill py-0" v-on:click.prevent="editMode=false">Cancel</button>
        </new-post>
        <div v-else class="card-text card-view">
            <h6 class="card-title mb-1">
                <router-link :to="{ name: 'user', params: {username: post.author.username} }">{{ post.author.username }}</router-link>
                <span class="small text-muted">at {{ post.create_time }} said:</span>
            </h6>
            <p>{{ post.text }}</p>
        </div>
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
                this.post.like_count = this.post.liked ? this.post.like_count - 1 : this.post.like_count + 1;
                this.post.liked = !this.post.liked;
                this.$emit("edit-ok", this.post);
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
                this.post.text = postText;
                this.$emit("edit-ok", this.post);
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
})


Vue.component("user-profile", {
    props: ["user"],
    template: `
    <div class="card p-3">
        <h5 class="card-title">{{ user.username }}</h5>
        <div class="row justify-content-between mx-1">
            <div>
                <span class="small text-muted">@{{ user.id }}</span>
            </div>
            <div v-if="!user.owner">
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
                this.user.follower_count = this.user.following ? this.user.follower_count - 1 : this.user.follower_count + 1;
                this.user.following = !this.user.following;
                this.$emit("user-ok", this.user);
            }, printError)
        }
    }
})


const viewsMixin = {
    methods: {
        updatePost: function(editedPost) {
            for (var i=0; i<this.posts.length; i++) {
                if (this.posts[i].id == editedPost.id) {
                    this.posts[i] = editedPost;
                }
            }
        },
        deletePost: function(delete_id) {
            for (var i=0; i<this.posts.length; i++) {
                if (this.posts[i].id == delete_id) {
                    this.posts.splice(i, 1);
                    break;
                }
            }
        },
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


const posts_view = {
    props: ['all'],
    template: `
        <div>
        posts view {{all}}
        <post-feed v-bind:posts="posts" v-on:edit-ok="updatePost($event)" v-on:delete-ok="deletePost($event)">
        </post-feed>
        </div>
    `,
    mixins: [viewsMixin],
    data: function () {
        return {
            posts: [],
        }
    },
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
};

const profile_view = {
    props: ['username'],
    template: `
        <div>
        profile view {{username}}
        <user-profile v-bind:user="user"></user-profile>
        <post-feed v-bind:posts="posts" v-on:edit-ok="updatePost($event)" v-on:delete-ok="deletePost($event)">
        </post-feed>
        </div>
    `,
    mixins: [viewsMixin],
    data: function () {
        return {
            user: {},
            posts: [],
        }
    },
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
};


const router = new VueRouter({
    mode: 'history',
    routes: [
        {path: '/', component: posts_view, name: "home"},
        {path: '/all', name: "all", component: posts_view, props: {all: true}},
        {path: '/:username', component: profile_view, name: "user", props: true},
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