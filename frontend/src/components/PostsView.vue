<template>
    <div>
        <post-feed v-bind:posts="posts" v-on:edit-ok="updatePost($event)" v-on:delete-ok="deletePost($event)">
        </post-feed>
    </div>
</template>

<script>
import PostFeed from './PostFeed.vue'
import { printError, getToken, viewsMixin } from './utils'

export default{
    name: "posts-view",
    props: ['all'],
    data: function () {
        return {
            posts: [],
        }
    },
    mixins: [viewsMixin],
    methods: {
        refreshView: function(query) {
            const url = this.all ? '/posts/all': '/posts/home';
            axios.get(url, {
                params: {
                    json: true,
                    after: 0,
                    count: 20,
                },
            }).then(response => {
                console.log(response)
                this.posts = response.data.posts;
            })
        },
    },
    components: {
        PostFeed        
    },
}
</script>

<style scoped>
</style>