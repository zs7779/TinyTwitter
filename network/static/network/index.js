function printError (error) {
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

Vue.component("post-feed", {
    props: ['posts'],
    template: `
    <div class="post-feed">
        <slot></slot>
        <ul class="list-group">
            <transition-group name="list" tag="p">
                <post-card
                    v-for="(post, index) in posts"
                    v-bind:key="post.id" v-bind:post="post"
                    v-on="$listeners">
                </post-card>
            </transition-group>
        </ul>
    </div>
    `,
})

Vue.component('post-card', {
    props: ['post'],
    template: `
    <li class="list-group-item">
        <div class="card-text">
            <p>{{ post.author }} <span class="small text-muted">at {{ post.timestamp }} said:</span></p>
            <p> {{ post.text }} </p>
        </div>
        <div class="card-footer bg-transparent p-0">
            {{ post.likes }} likes
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
                    <b-icon icon="heart" class="card-button"></b-icon> {{ post.likes }}
                </button>
                <b-dropdown id="dropdown-dropup" dropup variant="btn btn-transparent px-1 py-0" no-caret title="Options">
                    <template v-slot:button-content><b-icon icon="chevron-up" class="card-button"></b-icon></template>
                    <b-dropdown-item-button><b-icon icon="x" class="card-button"></b-icon> Delete</b-dropdown-item-button>
                    <b-dropdown-item-button><b-icon icon="pencil" class="card-button"></b-icon> Edit</b-dropdown-item-button>
                    <b-dropdown-item-button><b-icon icon="share" class="card-button"></b-icon> Share</b-dropdown-item-button>
                </b-dropdown>
            </div>
        </div>
    </li>
    `,
    methods: {
        onLike: function(event) {
            axios.put(endpoint_post+this.post.id, {
                like: !this.post.liked,
            }, {
                headers: {
                    'X-CSRFTOKEN': document.getElementsByName('csrfmiddlewaretoken')[0].value,
                },
            }).then(response => {
                this.post.likes = this.post.liked ? this.post.likes - 1 : this.post.likes + 1
                this.post.liked = !this.post.liked
                this.$emit("post-ok", this.post)
            }, printError)
        },
        onEdit: function(event) {
        },
        onDelete: function(event) {
        },
    },
})

Vue.component("new-post", {
    template: `
    <div>
        <form v-on:submit.prevent="onSubmitPost">
            <slot></slot>
            <textarea rows=3 class="form-control border-0" v-model="newPostText" placeholder="Say something..."></textarea>
            <div class="d-flex justify-content-end">
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
            this.newPostText = this.newPostText.substr(0, 140)
            return `${this.newPostText.length}/140`
        },
    },
    methods: {
        onSubmitPost: function (event) {
            if (this.newPostText.length == 0) {
                return
            }
            axios.post(endpoint_post, {
                newPostText: this.newPostText,
            }, {
                headers: {
                    'X-CSRFTOKEN': document.getElementsByName('csrfmiddlewaretoken')[0].value,
                },
            }).then(response => {
                this.newPostText = ""
                this.$emit("post-ok")
            }, printError)
        },
    },
})

var app = new Vue({
    el: '#project4',
    data: {
        posts: [],
    },
    methods: {
        getPosts: function () {
            axios.get(endpoint_posts).then(response => {
                this.posts = response.data
            })
        },
        insertPost: function(newPost) {
            this.posts.unshift(newPost)
        },
        updatePost: function(editedPost) {
            for (var i=0; i<this.posts.length; i++) {
                if (this.posts[i].id == editedPost.id) {
                    this.posts[i] = editedPost
                }
            }
        },
    },
    created: function () {
        this.getPosts()
    },
    delimiters: ['[[', ']]'],
})
