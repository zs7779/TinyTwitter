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
import { URLS, PLACEHOLDERS } from './utils'

export default{
    name: "user-post-view",
    props: ['username', 'postID'],
    data() {
        return {
            post: PLACEHOLDERS.post(),
            after: 0,
            count: 20,
        }
    },
    methods: {
        getUserPost() {
            const path_now = this.username + '|' + this.postID;
            axios.get(`${URLS.usersPosts(this.username, this.postID)}`, {
                params: {
                    after: this.after < this.post.comments.length ? 0 : this.after,
                    count: this.after < this.post.comments.length ? 0 : this.count,
                },
            }).then(response => {
                if (path_now === this.username + '|' + this.postID) {
                    this.post = {
                        ...response.data.post,
                        comments: this.post.comments,
                    }
                    this.appendComments(response.data.comments);
                    this.after += this.count;
                }
            })
        },
        // Update post data (comment/repost/like count) on the post currently being displayed
        updatePost(editID, post) {
            if (this.post.id === editID) {
                this.post = post;
            } else if (this.post.parent && this.post.parent.id == editID) {
                this.post.parent = post;
            } else if (this.post.root_post && this.post.root_post.id == editID) {
                this.post.root_post = post;
            } else this.updateComments(editID, post);
        },
        // Update comment data (comment/repost/like count) of the post currently being displayed
        updateComments(editID, comment) {
            this.post.comments = this.post.comments.map(p => p.id === editID ? comment : p);    
        },
        // Used to add comments in front (refresh)
        prependComments(comments) {
            comments.forEach(comment => {
                if (this.post.id === comment.root_post.id || this.post.id === comment.parent.id) {
                    this.post.comments.unshift(comment);
                    this.post.comment_count = this.post.comments.length;
                    this.post.commented = this.post.commented + 1;
                }
            });
        },
        // Used to add a new comment I just posted
        addComment(comment) {
            // If commenting on current post
            this.prependComments([comment]);
            // If commenting on root of current post
            if (this.post.root_post &&
               (this.post.root_post.id === comment.root_post.id || this.post.root_post.id === comment.parent.id)) {
                this.post.root_post = {
                    ...this.post.root_post,
                    comment_count: this.post.root_post.comment_count + 1,
                    commented: this.post.root_post.commented + 1,
                };
            }
            // If commenting on a comment of current post
            this.post.comments = this.post.comments.map(
                p => (p.id === comment.root_post.id || p.id === comment.parent.id) ? {
                    ...p,
                    comment_count: p.comment_count + 1,
                    commented: p.commented + 1,
                } : p
            );
        },
        // Used to add comments after (infinite scroll)
        appendComments(comments) {
            comments.forEach(c => {
                this.post.comments.push(c);
            })
        },
        deletePost(post) {
            if (this.post.id === post.id || this.post.root_post && this.post.root_post.id === post.id)
                this.$router.push({name: 'home'});
            else
                this.deleteComment(post);
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
        // addrepost only updates numbers because new posts are not displayed in this view
        // delete repost not possible in this view
        addRepost(post) {
            if (post.parent) {
                if (this.post.id === post.parent.id) {
                    this.post.repost_count++;
                    this.post.reposted++;
                } else if(this.post.root_post && this.post.root_post.id === post.parent.id) {
                    this.post.root_post.repost_count++;
                    this.post.root_post.reposted++;
                } else {
                    this.post.comments = this.post.comments.map(p => p.id === post.parent.id ? {
                        ...p,
                        repost_count: p.repost_count + 1,
                        reposted: p.reposted + 1,
                    } : p);
                }
            }
        },
        scroll () {
            window.onscroll = () => {
                let bottomOfWindow = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight;
                if (this.post.comments.length > 0 && bottomOfWindow) {
                    this.getUserPost();
                }
            };
        },
        resetView() {
            this.post = PLACEHOLDERS.post();
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