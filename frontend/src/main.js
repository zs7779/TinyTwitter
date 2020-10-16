import Vue from 'vue'
import VueRouter from 'vue-router'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import routes from './components/router'
import NewPost from './components/NewPost.vue'

Vue.config.productionTip = false
Vue.use(VueRouter)
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)


const router = new VueRouter({
  mode: 'history',
  routes: routes,
})


var vm = new Vue({
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
  components: {
    NewPost,
  },
  delimiters: ['[[', ']]'],
})
