<template>
    <div>
        <transition-group name="fade">
            <post-card
                v-for="post in posts"
                :key="post.id" :post="post"
                @like-ok="updatePosts($event.id, $event)" @delete-ok="deletePost($event)"
                v-on="$listeners">
            </post-card>
        </transition-group>
    </div>
</template>

<script>
import PostCard from './PostCard.vue'
import { URLS, PLACEHOLDERS } from './utils'

export default{
    name: "posts-view",
    props: ['all', 'username', 'hashtag'],
    data () {
        return {
            posts: PLACEHOLDERS.posts(),
            after: 0,
            count: 20,
        }
    },
    methods: {
        getPosts() {
            if (this.after < this.posts.length) {
                this.after = this.posts.length;
                return;
            }
            var url = this.all ? `${URLS.posts()}` : `${URLS.posts('home')}`;
            if (this.username) url = `${URLS.usersPosts(this.username)}`;
            if (this.hashtag) url = `${URLS.hashtags(this.hashtag)}`;
            const path_now = this.all + '|' + this.username + '|' + this.hashtag;
            axios.get(url, {
                params: {
                    after: this.after,
                    count: this.count,
                },
            }).then(response => {
                if (path_now === this.all + '|' + this.username + '|' + this.hashtag) {
                    this.appendPosts(response.data.posts);
                    this.after += this.count;
                }
            })
        },
        prependPosts(posts) {
            posts.forEach(p => {
                if (!this.username || this.username == p.author.username) this.posts.unshift(p);
            });
        },
        appendPosts(posts) {
            posts.forEach(p => {
                this.posts.push(p);
            })
        },
        updatePosts(editID, post, addBefore=true) {
            this.posts = this.posts.map(p => p.id === editID ? post : p);
        },
        addPost(post) {
            this.prependPosts([post]);
            if (post.parent) {
                this.addRepost(post.parent.id);
            }
        },
        deletePost(post) {
            this.posts = this.posts.filter(p => p.id !== post.id);
            if (post.parent) {
                this.deleteRepost(post.parent.id);
            }
        },
        addComment(id) {
            this.posts = this.posts.map(p => p.id === id ? {...p, comment_count: p.comment_count+1, commented: p.commented+1} : p);
        },
        //delete comment not possible in this view,
        addRepost(id) {
            this.posts = this.posts.map(p => p.id === id ? {...p, repost_count: p.repost_count+1, reposted: p.reposted+1} : p);
        },
        deleteRepost(id) {
            this.posts = this.posts.map(p => p.id === id ? {...p, repost_count: p.repost_count-1, reposted: p.reposted-1} : p);
        },
        scroll() {
            window.onscroll = () => {
                let bottomOfWindow = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight;
                if (this.posts.length > 0 && bottomOfWindow) {
                    this.getPosts();
                }
            };
        },
        resetView() {
            this.posts = PLACEHOLDERS.posts();
            this.after = 0;
            this.count = 20;
        },
    },
    watch: {
        $route() {
            this.resetView();
            this.getPosts();
        },
    },
    created() {
        this.getPosts();
    },
    mounted() {
        this.scroll();
    },
    components: {
        PostCard,
    },
}
</script>

<style scoped>
</style>