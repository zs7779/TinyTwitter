Vue.component('post', {
  template: '\
    <li>\
      {{ title }}\
      <button v-on:click="$emit(\'remove\')">Remove</button>\
    </li>\
  ',
  props: ['title'],
})

Vue.component("new_post", {
    props: [],
    template: '\
        <div class="class_new_post_input_area">\
            <form>\
                <textarea class="form-control" v-model="new_post_text" placeholder="Say something..." v-on:keypress="onTextInput"></textarea>\
                <span>{{ char_remaining }} characters remaining</span>\
                <button type="button" class="btn btn-outline-primary float-right mt-1">Post</button>\
            </form>\
        </div>\
    ',
    data: function () {
        return {
            new_post_text: "",
            char_remaining: 140,
        }
    },
    methods: {
        onTextInput: function (event) {
            if (this.char_remaining > 0) {
                this.char_remaining--
            } else {
                event.preventDefault()
            }
        },
    },
})

new Vue({
  el: '#project4',
  data: {
    posts: [],
  },
  methods: {
    get_posts: function () {
        axios.get(posts_endpoint).then(response => {
            posts = response.json().data
        })
    }
  }
})