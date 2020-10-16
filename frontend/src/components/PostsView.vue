<template>
    <div>
        <post-feed v-bind:posts="posts" @action-like="doLike($event)" @action-edit="doEdit($event)" @action-delete="doDelete($event)">
        </post-feed>
    </div>
</template>

<script>
import PostFeed from './PostFeed.vue'
import { URLs, PLACEHOLDERs, getToken, postsViewsMixin } from './utils'

export default{
    name: "posts-view",
    props: ['all'],
    data: function () {
        return {
            posts: PLACEHOLDERs.posts,
        }
    },
    mixins: [postsViewsMixin],
    methods: {
        refreshView: function(query='') {
            const url = this.all ? `${URLs.posts()}`: `${URLs.posts('home')}`;
            axios.get(url, {
                params: {
                    json: true,
                    after: 0,
                    count: 20,
                },
            }).then(response => {
                console.log('posts',response)
                this.posts = response.data.posts;
            })
        },
    },
    mounted: function () {
        this.refreshView('');
    },
    components: {
        PostFeed
    },
}
</script>

<style scoped>
</style>