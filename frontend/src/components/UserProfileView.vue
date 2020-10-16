<template>
    <div>
        <user-profile :user="user" @action-follow="doFollow()"></user-profile>
        <router-view :post="post" @action-like="doLike($event)" @action-edit="doEdit($event)" @action-delete="doDelete($event)" name="post" />
        <router-view :posts="posts" @action-like="doLike($event)" @action-edit="doEdit($event)" @action-delete="doDelete($event)" name="posts" />
    </div>
</template>

<script>
import UserProfile from './UserProfile.vue'
import { URLs, PLACEHOLDERs, getToken, postsViewsMixin, userViewsMixin } from './utils'

export default{
    name: "profile-view",
    props: ['username', 'postID'],
    data: function () {
        return {
            user: PLACEHOLDERs.user,
            posts: PLACEHOLDERs.posts,
            post: PLACEHOLDERs.post,
        }
    },
    mixins: [postsViewsMixin, userViewsMixin],
    methods: {
        refreshView: function(query='') {
            axios.get(`${URLs.usersPosts(this.username)}`, {
                params: {
                    json: true,
                    after: 0,
                    count: 20,
                },
            }).then(response => {
                console.log('profile',response)
                this.user = response.data.user;
                this.posts = response.data.posts;
            })
        },
        getPost: function(id) {
            const posts = this.posts.filter(p => p.id == id);
            if (posts.length !== 1) {
                axios.get(`${URLs.usersPosts(this.username, id)}`, {
                    params: {
                        json: true,
                    },
                }).then(response => {
                    console.log('getPost',response)
                    this.user = response.data.user
                    this.post = response.data.post;
                })
            } else {
                this.post = posts[0];
            }
        }
    },
    watch: {
        postID: function() {
            if (this.postID) {
                this.getPost(this.postID);
            }
        },
    },
    mounted: function() {
        if (this.postID) {
            this.getPost(this.postID);
        } else {
            this.refreshView('');
        }
    },
    components: {
        UserProfile
    },
}
</script>

<style scoped>
</style>