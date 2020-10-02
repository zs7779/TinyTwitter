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
    <div>
        <ul class="list-group mt-2">
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
            <textarea class="form-control" v-model="newPostText" placeholder="Say something..." v-on:keypress="onTextInput"></textarea>
            <span>{{ charRemaining }} characters remaining</span>
            <button type="submit" class="btn btn-outline-primary float-right btn-sm mt-1">Post</button>
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
            return 140 - this.newPostText.length
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
