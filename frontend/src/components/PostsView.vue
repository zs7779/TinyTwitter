<template>
    <div>
        <post-feed :posts="posts" @like-ok="updatePosts($event.id, $event)" @delete-ok="deletePost($event)" v-on="$listeners">
        </post-feed>
    </div>
</template>

<script>
import PostFeed from './PostFeed.vue'
import { URLs, PLACEHOLDERs } from './utils'

export default{
    name: "posts-view",
    props: ['all', 'username'],
    data () {
        return {
            posts: PLACEHOLDERs.posts(),
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
            var url = this.all ? `${URLs.posts()}` : `${URLs.posts('home')}`;
            if (this.username) url = `${URLs.usersPosts(this.username)}`;
            axios.get(url, {
                params: {
                    after: this.after,
                    count: this.count,
                },
            }).then(response => {
                this.appendPosts(response.data.posts);
                this.after += this.count;
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
            this.posts = PLACEHOLDERs.posts();
            this.after = 0;
            this.count = 20;
        },
    },
    watch: {
        all() {
            this.resetView();
            this.getPosts();
        },
        username() {
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
        PostFeed,
    },
}
</script>

<style scoped>
</style>