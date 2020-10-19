<template>
    <div>
        <post-card :post="post" @like-ok="updatePost($event.id, $event)" @delete-ok="deletePost($event)" v-on="$listeners"></post-card>
    </div>
</template>

<script>
import PostCard from './PostCard.vue'
import { URLs, PLACEHOLDERs } from './utils'

export default{
    name: "user-post-view",
    props: ['username', 'postID'],
    data() {
        return {
            post: PLACEHOLDERs.post,
        }
    },
    methods: {
        getUserPost() {
            axios.get(`${URLs.usersPosts(this.username, this.postID)}`, {
                params: {
                },
            }).then(response => {
                console.log('getPost',response)
                this.post = response.data.post;
            })
        },
        updatePost(editID, editedPost) {
            if (this.post.id === editID) this.post = editedPost;
        },
        deletePost(deleteID) {
            if (this.post.id === deleteID) this.$router.push({name: 'home'});
        },
    },
    watch: {
        username() {
            this.getUserPost();
        },
        postID() {
            this.getUserPost();
        }
    },
    created() {
        this.getUserPost();
    },
    components: {
        PostCard
    },
}
</script>

<style scoped>
</style>