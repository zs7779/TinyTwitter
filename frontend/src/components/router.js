import ProfileView from './ProfileView.vue'
import PostsView from './PostsView.vue'
import PostView from './PostView.vue'
import NotificationView from './NotificationView.vue'

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
            posts: true,
        }, name: 'hashtag'
    },
    {
        path: '/notifications/', components: {
            infos: NotificationView,
        }, name: 'notificationsReplies'
    },
    {
        path: '/notifications/mentions', components: {
            infos: NotificationView,
        }, props: {
            infos: {path: 'mentions'},
        }, name: 'notificationsMentions'
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

const routeNames = {
    'all': 'All Posts',
    'home': 'Home',
    'user': 'Profile',
    'post': 'Thread',
    'hashtag': 'Hashtag',
    'notificationsReplies': 'Notifications',
    'notificationsMentions': 'Notifications',
};

export { routes, routeNames };
