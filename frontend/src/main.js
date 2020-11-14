import { routes, routeNames } from './components/router'
import NewPost from './components/NewPost.vue'
import { URLS, PLACEHOLDERS } from './components/utils'

Vue.config.productionTip = false

const router = new VueRouter({
  mode: 'history',
  routes: routes,
  scrollBehavior (to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { x: 0, y: 0 };
    }
  }
})

var vm = new Vue({
  el: '#app',
  router,
  data: {
      postParams: PLACEHOLDERS.postParams(),
      user: PLACEHOLDERS.user(),
      userAuth: document.getElementById('userauth') ? true : false,
  },
  computed: {
    pageTitle() {
      return routeNames[this.$route.name];
    },
  },
  methods: {
    clearPost() {
      this.postParams = PLACEHOLDERS.postParams();
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
      this.clearPost();
    },
    getCurrentUser() {
      axios.get(URLS.currentUser()).then(response => {
        this.user = response.data.user;
      });
    }
  },
  watch: {
    $route() {
      axios.get(URLS.currentUser()).then(response => {
        this.user = response.data.user;
      });
    },
  },
  mounted() {
    this.getCurrentUser();
  },
  components: {
    NewPost,
  },
  delimiters: ['[[', ']]'],
})
