<template>
    <div class="card p-1">
        <post-body
            :post='post' :buttons='true' :verbose='verbose'
            @action-comment="onComment(post)" @action-like="onLike(post)" @action-delete="onDelete(post)" @action-edit="onEdit(post)"
        >
            <post-body v-if='post.parent' :post='post.parent' :buttons='false' class='card p-3' />
            <div v-if='verbose' class="card-footer bg-transparent p-0 ">
                <span>{{ post.repost_count }} Reposts</span> <span>{{ post.like_count }} Likes</span>
            </div>
        </post-body>
        <div v-if='verbose' class="list-group list-group-flush border-top">
            <post-body 
                v-for='comment in post.comments' :key='comment.id' :post='comment' :buttons='true'
                @action-comment="onComment(comment)" @action-like="onLike(comment)" @action-delete="onDelete(comment)" @action-edit="onEdit(comment)"
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
        onEdit(post) {
            const postParams = {
                oldPost: post,
            };
            this.$emit("action-post", postParams);
        },
        onLike(post) {
            const token = getToken();
            if (!token) return;
            axios.post(`${URLs.posts(post.id)}`, {
                like: !this.post.liked,
            }, {
                headers: {
                    'X-CSRFTOKEN': token,
                },
            }).then(response => {
                this.$emit("like-ok", {
                    ...post,
                    like_count: post.liked ? post.like_count - 1 : post.like_count + 1,
                    liked: 1 - post.liked,
                });
            })
        },
        onDelete(post) {
            const token = getToken();
            if (!token) return;
            axios.delete(`${URLs.posts(post.id)}`, {
                headers: {
                    'X-CSRFTOKEN': token,
                },
            }).then(response => {
                this.$emit("delete-ok", post.id);
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