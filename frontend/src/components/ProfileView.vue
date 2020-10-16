<template>
    <div>
        <user-profile :user="user" @user-ok="updateUser($event)"></user-profile>
        <router-view :posts="posts" :username="username" :id="post_id" @edit-ok="updatePost($event)" @delete-ok="deletePost($event)" name="post"></router-view>
        <router-view :posts="posts" @edit-ok="updatePost($event)" @delete-ok="deletePost($event)" name="posts"></router-view>
    </div>
</template>

<script>
import UserProfile from './UserProfile.vue'
import { URLs, viewsMixin } from './utils'

export default{
    name: "profile-view",
    props: ['username', 'post_id'],
    data: function () {
        return {
            user: {},
            posts: [],
        }
    },
    mixins: [viewsMixin],
    methods: {
        refreshView: function(query) {
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
    },
    components: {
        UserProfile        
    },
}
</script>

<style scoped>
</style>