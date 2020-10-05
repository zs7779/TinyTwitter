const URLS = {
    read_posts: "/posts/",
    read_post: "/post/",
    read_user: "/user/",
    write_posts: "/posts_new/",
    write_post: "/post_mod/",
    write_user: "/user_mid/",
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
        <div class="card-text card-view">
            <h6 class="card-title mb-1">
                <a v-bind:href='${URLS.read_user}+post.author.id' v-on:click.prevent="goProfile">{{ post.author.username }}</a>
                <span class="small text-muted">at {{ post.timestamp }} said:</span>
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
                    <b-dropdown-item v-if="post.owner"><b-icon icon="pencil" class="card-button"></b-icon> Edit</b-dropdown-item>
                    <b-dropdown-item><b-icon icon="share" class="card-button"></b-icon> Share</b-dropdown-item>
                </b-dropdown>
            </div>
        </div>
    </div>
    `,
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
        onEdit: function(event) {
            token = getToken();
            if (!token) {return;}
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
        goProfile: function(event) {
            this.$emit("go-profile", this.post.author.id);
        },
    },
})


Vue.component("new-post", {
    template: `
    <div class="card p-3">
        <form v-on:submit.prevent="onSubmitPost">
            <slot></slot>
            <textarea rows=4 class="form-control border-0" v-model="newPostText" placeholder="Say something..."></textarea>
            <div class="d-flex justify-content-end mt-2">
                <span class="mx-1">{{ charRemaining }}</span>
                <button type="submit" class="btn btn-primary rounded-pill py-0">Post</button>
            </div>
        </form>
    </div>
    `,
    data: function () {
        return {
            newPostText: "",
        }
    },
    computed: {
        charRemaining: function() {
            this.newPostText = this.newPostText.substr(0, 140);
            return `${this.newPostText.length}/140`;
        },
    },
    methods: {
        onSubmitPost: function (event) {
            if (this.newPostText.length == 0) {return;}
            axios.post(`${URLS.write_posts}`, {
                newPostText: this.newPostText,
            }, {
                headers: {
                    'X-CSRFTOKEN': getToken(),
                },
            }).then(response => {
                this.newPostText = "";
                this.$emit("post-ok");
            }, printError)
        },
    },
})


Vue.component("user-profile", {
    props: ["user"],
    template: `
    <div class="card p-3">
        <h5 class="card-title">
            {{ user.username }}
            <span class="small text-muted">@{{ user.id }}</span>
            <button class="btn btn-outline-primary rounded-pill float-right">Follow</button>
        </h5>

        <div class="card-footer bg-transparent p-0">
            <p class="mx-1">{{ user.bio }}</p>
            <span class="mx-1"><span class="font-weight-bold">{{user.following_count}}</span> Following</span>
            <span class="mx-1"><span class="font-weight-bold">{{user.follower_count}}</span> Followers</span>
        </div>
    </div>
    `,
})


var app = new Vue({
    el: '#project4',
    data: {
        posts: [],
        user: {},
    },
    methods: {
        pushHistory: function(url) {
            history.pushState({
                user: this.user,
                posts: this.posts,
            }, "", url)
        },
        getJSON: function(endpoint, url) {
            axios.get(endpoint, {
                params: {
                    json: true,
                    after: 0,
                    count: 20,
                },
            }).then(response => {
                this.user = response.data.user;
                this.posts = response.data.posts;
                this.pushHistory(url);
            })
        },
        getPosts: function() {
            this.getJSON(`${URLS.read_posts}`, '/');
        },
        getProfile: function(user_id) {
            profile_url = `${URLS.read_user}${user_id}`;
            this.getJSON(profile_url, profile_url);
        },
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
        this.getPosts();
    },
    delimiters: ['[[', ']]'],
})

window.addEventListener('popstate', function(event) {
    app.user = event.state.user;
    app.posts = event.state.posts;
});