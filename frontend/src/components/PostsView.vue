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
            posts: PLACEHOLDERs.posts,
        }
    },
    methods: {
        getPosts(query='') {
            var url = this.all ? `${URLs.posts()}` : `${URLs.posts('home')}`;
            if (this.username) url = `${URLs.usersPosts(this.username)}`;
            axios.get(url, {
                params: {
                    after: 0,
                    count: 20,
                },
            }).then(response => {
                console.log('posts',response)
                this.posts = response.data.posts;
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
        updatePosts(editID, editedPost, addBefore=true) {
            this.posts = this.posts.map(p => p.id === editID ? editedPost : p);
        },
        deletePost(deleteID) {
            this.posts = this.posts.filter(p => p.id !== deleteID);
        },
        addComment(id) {
            this.posts = this.posts.map(p => p.id === id ? {
                ...p,
                comment_count: p.comment_count+1,
                commented: true,
            } : p);
        },
        deleteComment(id) {
            this.posts = this.posts.map(p => p.id === id ? {...p, comment_count: p.comment_count-1} : p);
        },
        addRepost(id) {
            this.posts = this.posts.map(p => p.id === id ? {...p, repost_count: p.repost_count+1} : p);
        },
        deleteRepost(id) {
            this.posts = this.posts.map(p => p.id === id ? {...p, repost_count: p.repost_count+1} : p);
        },
    },
    created: function () {
        this.getPosts('');
    },
    watch: {
        all() {
            this.getPosts();
        },
        username() {
            this.getPosts();
        },
    },
    components: {
        PostFeed,
    },
}
</script>

<style scoped>
</style>