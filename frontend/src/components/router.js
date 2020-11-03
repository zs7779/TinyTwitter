import ProfileView from './ProfileView.vue'
import PostsView from './PostsView.vue'
import PostView from './PostView.vue'

const routes = [
    {
        path: '/', components: {
            posts: PostsView,
        }, name: "home"
    },
    {
        path: '/all', components: {
            posts: PostsView,
        }, props: {
            posts: {all: true},
        }, name: 'all'
    },
    {
        path: '/hashtags/:hashtag', components: {
            posts: PostsView,
        }, props: {
            posts: {all: true},
        }, name: 'hashtag'
    },
    {
        path: '/:username', components: {
            profile: ProfileView,
            posts: PostsView,
        }, props: {
            profile: true,
            posts: true
        }, name: 'user'
    },
    {
        path: '/:username/:postID', components: {
            profile: ProfileView,
            post: PostView,
        }, props: {
            profile: true,
            post: true
        }, name: 'post'
    },
]

export default routes;
