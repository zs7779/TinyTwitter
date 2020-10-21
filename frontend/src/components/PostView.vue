<template>
    <div>
        <post-card :post="post" :verbose=true @like-ok="updatePost($event.id, $event)" @delete-ok="deletePost($event)" v-on="$listeners"></post-card>
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
                this.post = {
                    ...response.data.post,
                    comments: response.data.comments,
                }
            })
        },
        updatePost(editID, editedPost) {
            if (this.post.id === editID) {
                this.post = editedPost;
            } else this.updateComments(editID, editedPost);
        },
        deletePost(deleteID) {
            if (this.post.id === deleteID) this.$router.push({name: 'home'});
            else this.deleteComment(deleteID);
        },
        prependComments(editID, comments) {
            if (this.post.id === editID) {
                comments.forEach(comment => {
                    this.post.comments.unshift(comment);
                    this.post.comment_count = this.post.comments.length;
                });
            }
        },
        appendComments() {},
        updateComments(editID, comment) {
            this.post.comments = this.post.comments.map(p => p.id === editID ? comment : p);    
        },
        addComment(comment) {
            this.prependComments(comment.root_post.id, [comment]);
            this.post.commented = true;
            this.post.comments = this.post.comments.map(p => p.id === comment.parent.id ? {
                ...p,
                comment_count: p.comment_count + 1,
                commented: p.commented + 1,
            } : p)
        },
        deleteComment(deleteID) {
            const comments = this.post.comments.filter(p => p.id === deleteID);
            this.post.comments = this.post.comments.filter(p => p.id !== deleteID);
            this.post.comment_count = this.post.comments.length;
            this.post.commented = this.post.comments.filter(p => p.owner).length;
            console.log(this.post.comments);
            if (comments.length == 1) {
                const comment = comments[0];
                console.log(comment)
                this.post.comments = this.post.comments.map(p => p.id === comment.parent.id ? {
                    ...p,
                    comment_count: p.comment_count - 1,
                    commented: p.commented - 1,
                } : p)
            }
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