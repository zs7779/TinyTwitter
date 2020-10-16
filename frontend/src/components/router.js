import PostsView from './PostsView.vue'
import ProfileView from './ProfileView.vue'
import UserPostsView from './UserPostsView.vue'
import UserPostView from './UserPostView.vue'

const routes = [
    {path: '/', component: PostsView, name: "home"},
    {path: '/all', component: PostsView, props: {all: true}, name: "all"},
    {path: '/:username', component: ProfileView, props: true,
        children: [
            {path:'', components: {
                posts: UserPostsView,
            }, name: 'user'},
            {path:':postID', components: {
                post: UserPostView,
            }, props:true, name: 'post'},
        ]
    },
]

export default routes;
