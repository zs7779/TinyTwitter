<template>
    <div class="card p-1 rounded-0">
        <div v-if='verbose && post.is_comment' class="list-group list-group-flush">
            <post-body v-if='post.root_post' :post='post.root_post' :buttons='true' class='list-group-item' 
                @action-comment="onComment(post.root_post)" @action-repost="onRepost(post.root_post)"
                @action-like="onLike(post.root_post)" @action-delete="onDelete(post.root_post)"
            />
        </div>
        <post-body class="border-bottom"
            :post='post' :buttons='true' :verbose='verbose'
            @action-comment="onComment(post)" @action-repost="onRepost(post)"
            @action-like="onLike(post)" @action-delete="onDelete(post)"
        >
            <post-body v-if='post.parent && !post.is_comment' :post='post.parent' :buttons='false' class='card p-3 mb-3 mr-2' />
        </post-body>
        <div v-if='verbose' class="list-group list-group-flush">
            <post-body 
                v-for='comment in post.comments' :key='comment.id' :post='comment' :buttons='true'
                @action-comment="onComment(comment)" @action-repost="onRepost(comment)"
                @action-like="onLike(comment)" @action-delete="onDelete(comment)"
                class="list-group-item"
            />
        </div>
    </div>
</template>

<script>
import PostBody from './PostBody.vue'
import { URLs, getToken } from './utils'

export default{
    name: "post-card",
    props: ['post', 'verbose'],
    methods: {
        onComment(post) {
            const postParams = {
                isComment: true,
                parentPost: post,
                rootPost: this.post.is_comment ? this.post.root_post : this.post,
            };
            this.$emit("action-post", postParams);
        },
        onRepost(post) {
            const postParams = {
                parentPost: post,
            };
            this.$emit("action-post", postParams);
        },
        onLike(post) {
            const token = getToken(this.$root.userAuth);
            if (!token) return;
            axios.post(`${URLs.posts(post.id)}`, {
                like: !post.liked,
            }, {
                headers: {
                    'X-CSRFTOKEN': token,
                },
            }).then(response => {
                this.$emit("like-ok", {
                    ...post,
                    like_count: post.liked ? post.like_count - 1 : post.like_count + 1,
                    liked: post.liked ? post.liked - 1 : post.liked + 1,
                });
            })
        },
        onDelete(post) {
            const token = getToken(this.$root.userAuth);
            if (!token) return;
            axios.delete(`${URLs.posts(post.id)}`, {
                headers: {
                    'X-CSRFTOKEN': token,
                },
            }).then(response => {
                this.$emit("delete-ok", post);
            })
        },
    },
    components: {
        PostBody
    }
}
</script>

<style scoped>
</style>