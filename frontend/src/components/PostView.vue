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
        updatePost(editID, post) {
            if (this.post.id === editID) {
                this.post = post;
            } else this.updateComments(editID, post);
        },
        deletePost(post) {
            if (this.post.id === post.id) this.$router.push({name: 'home'});
            else this.deleteComment(post);
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
            } : p);
        },
        deleteComment(comment) {
            this.post.comments = this.post.comments.filter(p => p.id !== comment.id);
            this.post.comment_count = this.post.comments.length;
            this.post.commented = this.post.comments.filter(p => p.owner).length;
            
            this.post.comments = this.post.comments.map(p => p.id === comment.parent.id ? {
                ...p,
                comment_count: p.comment_count - 1,
                commented: p.commented - 1,
            } : p);
        },
        addRepost(post) {
            if (post.parent && post.parent.id == this.post.id) {
                this.post.repost_count++;
                this.post.posted++;
            }
        },
        // delete repost not possible in this view,
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