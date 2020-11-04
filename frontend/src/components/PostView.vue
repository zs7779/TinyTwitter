<template>
    <div>
        <post-card :post="post" :verbose=true
            @like-ok="updatePost($event.id, $event)"
            @delete-ok="deletePost($event)" v-on="$listeners"></post-card>
    </div>
</template>

<script>
import axios from 'axios'
import PostCard from './PostCard.vue'
import { URLs, PLACEHOLDERs } from './utils'

export default{
    name: "user-post-view",
    props: ['username', 'postID'],
    data() {
        return {
            post: PLACEHOLDERs.post(),
            after: 0,
            count: 20,
        }
    },
    methods: {
        getUserPost() {
            axios.get(`${URLs.usersPosts(this.username, this.postID)}`, {
                params: {
                    after: this.after < this.post.comments.length ? 0 : this.after,
                    count: this.after < this.post.comments.length ? 0 : this.count,
                },
            }).then(response => {
                this.post = {
                    ...response.data.post,
                    comments: this.post.comments,
                }
                this.appendComments(response.data.comments);
                this.after += this.count;
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
        appendComments(comments) {
            comments.forEach(c => {
                this.post.comments.push(c);
            })
        },
        updateComments(editID, comment) {
            this.post.comments = this.post.comments.map(p => p.id === editID ? comment : p);    
        },
        addComment(comment) {
            this.prependComments(comment.root_post.id, [comment]);
            this.post.commented = this.post.commented + 1;
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
            if (post.parent) {
                if (post.parent.id == this.post.id) {
                    this.post.repost_count++;
                    this.post.reposted++;
                } else {
                    this.post.comments = this.post.comments.map(p => p.id === post.parent.id ? {
                        ...p,
                        repost_count: p.repost_count + 1,
                        reposted: p.reposted + 1,
                    } : p);
                }
            }
        },
        // delete repost not possible in this view,
        scroll () {
            window.onscroll = () => {
                let bottomOfWindow = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight;
                if (this.post.comments.length > 0 && bottomOfWindow) {
                    this.getUserPost();
                }
            };
        },
        resetView() {
            this.post = PLACEHOLDERs.post();
            this.after = 0;
            this.count = 20;
        },
    },
    watch: {
        $route() {
            this.resetView()
            this.getUserPost();
        },
    },
    created() {
        this.getUserPost();
    },
    mounted() {
        this.scroll();
    },
    components: {
        PostCard
    },
}
</script>

<style scoped>
</style>