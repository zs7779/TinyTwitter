// import Vue from 'vue'
// import VueRouter from 'vue-router'

import routes from './components/router'
import NewPost from './components/NewPost.vue'
import { PLACEHOLDERs } from './components/utils'

Vue.config.productionTip = false
// Vue.use(VueRouter)


const router = new VueRouter({
  mode: 'history',
  routes: routes,
})


var vm = new Vue({
  el: '#app',
  router,
  data: {
      pathname: window.location.pathname,
      postParams: PLACEHOLDERs.postParams,
  },
  computed: {
    updatePath() {
        this.pathname = window.location.pathname;
    },
  },
  methods: {
    log(e){console.log(e)},
    clearPost() {
      this.postParams = PLACEHOLDERs.postParams;
    },
    updateContent(post) {
      if (this.$refs.post) this.$refs.post.updatePost(post.id, post);
      if (this.$refs.posts) this.$refs.posts.updatePosts(post.id, post);
      this.clearPost();
    },
    addContent(post) {
      if (this.$refs.post) this.$refs.post.addRepost(post);
      if (this.$refs.posts) this.$refs.posts.addPost(post);
      this.clearPost();
    },
    addComment(post) {
      if (this.$refs.post) this.$refs.post.addComment(post);
      if (this.$refs.posts) this.$refs.posts.addComment(post.root_post.id, post);
      this.clearPost(); // not nessessary leave here so I don't dig it up
    },
  },
  components: {
    NewPost,
  },
  delimiters: ['[[', ']]'],
})
