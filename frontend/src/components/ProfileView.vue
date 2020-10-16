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
            axios.get(`${URLs.users}${this.username}`, {
                params: {
                    json: true,
                    after: 0,
                    count: 20,
                },
            }).then(response => {
                console.log(response)
                this.user = response.data.user;
                this.posts = response.data.posts;
            })
        },
        doFollow: function() {
            const token = getToken();
            if (!token) return;
            axios.post(`${URLs.users}${this.user.username}`, {
                follow: !this.user.following,
            }, {
                headers: {
                    'X-CSRFTOKEN': token,
                },
            }).then(response => {
                const user = {
                    ...this.user,
                    follower_count: this.user.following ? this.user.follower_count - 1 : this.user.follower_count + 1,
                    following: !this.user.following,
                }
                this.updateUser(user);
            })
        },
        getPost: function(id) {
            const posts = this.posts.filter(p => p.id == id);
            if (posts.length !== 1) {
                axios.get(`${URLs.users}${this.username}/${id}`, {
                    params: {
                        json: true,
                    },
                }).then(response => {
                    console.log(response)
                    this.post = response.data;
                })
            } else {
                this.post = posts[0];
            }
        }
    },
    watch: {
        username: function() {
            this.refreshView();
        },
        postID: function() {
            if (this.postID) {
                this.getPost(this.postID);
            }
        },
        posts: function() {
            if (this.postID) {
                this.getPost(this.postID);
            }
        }
    },
    mounted: function() {
        if (this.postID) {
            this.getPost(this.postID);
        }
    },
    components: {
        UserProfile        
    },
}
</script>

<style scoped>
</style>