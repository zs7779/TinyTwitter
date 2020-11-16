import { routes, routeNames } from './components/router'
import NewPost from './components/NewPost.vue'
import TrendsView from './components/TrendsView.vue'
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
      userAuth: document.getElementById('userauth') ? true : false, // slightly more reliable check
      trending: {
        users: [],
        posts: [],
        hashtags: [],
      }
  },
  computed: {
    pageTitle() {
      let title = routeNames[this.$route.name];
      if (this.$route.name === 'hashtag')
        title += ' #' + this.$route.params.hashtag;
      return title;
    },
  },
  methods: {
    clearPost() {
      this.postParams = PLACEHOLDERS.postParams();
    },
    updateUser(user) {
      if (this.$refs.profile) this.$refs.profile.updateUser(user);
      this.trending.users = this.trending.users.map(u => u.id === user.id ? user : u);
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
        if (response.data.trends) {
          this.trending.users = response.data.trends.users;
          this.trending.posts = response.data.trends.posts;
          this.trending.hashtags = response.data.trends.hashtags;
        }
      });
    }
  },
  watch: {
    $route() {
      axios.get(URLS.currentUser()).then(response => {
        this.getCurrentUser();
      });
    },
  },
  mounted() {
    this.getCurrentUser();
  },
  components: {
    NewPost,
    TrendsView,
  },
  delimiters: ['[[', ']]'],
})
