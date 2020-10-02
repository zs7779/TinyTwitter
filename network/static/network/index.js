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
            <post-card v-for="post in posts" v-bind:key="post.index" v-bind:post="post"></post-card>
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
    </li>
    `,
})

Vue.component("new-post", {
    template: `
    <div>
        <form v-on:submit.prevent="onSubmitPost">
            <slot></slot>
            <textarea rows=3 class="form-control border-0" v-model="newPostText" placeholder="Say something..." v-on:keypress="onTextInput"></textarea>
            <div class="d-flex justify-content-end">
            <span class="mx-1">{{ charRemaining }}</span>
            <button type="submit" class="btn btn-primary rounded-pill new-post-button">Post</button>
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
        onTextInput: function (event) {
            if (this.newPostText.length >= 140) {
                event.preventDefault()
            }
        },
        onSubmitPost: function (event) {
            if (this.newPostText.length == 0) {
                return
            }
            axios.post(endpoint_post, {
                newPostText: this.newPostText,
            }, {
                headers: {
                    'X-CSRFTOKEN': event.target.elements.csrfmiddlewaretoken.value,
                },
            }).then(response => {
                this.newPostText = ""
                this.$emit("new-post-ok")
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
                console.log("armed")
            })
        },
    },
    created: function () {
        this.getPosts()
    },
    delimiters: ['[[', ']]'],
})
