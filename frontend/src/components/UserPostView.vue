<template>
    <div>
        <post-card :post="post" v-on="$listeners"></post-card>
    </div>
</template>

<script>
import PostCard from './PostCard.vue'

export default{
    name: "user-post-view",
    props: ['posts', 'username', 'id'],
    data: function() {
        return {
            post: {
                author: {id: null, username: 'username'},
                id: -1,
                text: "",
                create_time: null,
                like_count: null,
            },
        };
    },
    watch: {
        posts: function(posts) {
            posts = posts.filter(p => p.id == this.id);
            if (posts.length !== 1) {
                axios.get(`/users/${this.username}/${this.id}`, {
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
        },
    },
    components: {
        PostCard
    },
}
</script>

<style scoped>
</style>