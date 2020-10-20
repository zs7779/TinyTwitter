<template>
    <div :class="[hovering ? 'hover':'', 'card p-3']" @mouseover='hovering=true' @mouseout='hovering=false'>
        <post-body :post='post'><post-body v-if='post.parent' :post='post.parent' class='card p-3' /></post-body>
        <div class="card-footer bg-transparent p-0">
            {{ post.like_count }} likes
        </div>
        <div class="card-footer bg-transparent p-0">
            <div class="d-flex justify-content-around">
                <button type="button" v-b-modal.new-post class="btn btn-transparent px-1 py-0" title="Comment" @click="onComment">
                    <b-icon icon="chat" class="card-button"></b-icon>
                </button>
                <button type="button" class="btn btn-transparent px-1 py-0" title="Repost">
                    <b-icon icon="arrow-repeat" class="card-button"></b-icon>
                </button>
                <button type="button" class="btn btn-transparent px-1 py-0" title="Like" @click="onLike">
                    <b-icon icon="heart" :class="[post.liked ? 'card-button-active' : 'card-button', '']"></b-icon> {{ post.like_count }}
                </button>
                <b-dropdown id="dropdown-dropup" dropup variant="btn btn-transparent px-1 py-0" no-caret title="Options">
                    <template v-slot:button-content><b-icon icon="chevron-up" class="card-button"></b-icon></template>
                    <b-dropdown-item v-if="post.owner" @click="onDelete"><b-icon icon="x" class="card-button"></b-icon> Delete</b-dropdown-item>
                    <b-dropdown-item v-b-modal.new-post v-if="post.owner" @click="onEdit"><b-icon icon="pencil" class="card-button"></b-icon> Edit</b-dropdown-item>
                    <b-dropdown-item><b-icon icon="share" class="card-button"></b-icon> Share</b-dropdown-item>
                </b-dropdown>
            </div>
        </div>
    </div>
</template>

<script>
import PostBody from './PostBody.vue'
import { URLs, getToken } from './utils'

export default{
    name: "post-card",
    props: ['post'],
    data() {
        return {
            hovering: false,
        }
    },
    methods: {
        onComment(event) {
            const postParams = {
                isComment: true,
                parentPost: this.post,
                rootPost: this.post.is_comment ? this.post.root_post : this.post,
            };
            this.$emit("action-post", postParams);
        },
        onRepost(event) {
            const postParams = {
                parentPost: this.post,
            };
            this.$emit("action-post", postParams);
        },
        onEdit(event) {
            const postParams = {
                oldPost: this.post,
            };
            this.$emit("action-post", postParams);
        },
        onLike(event) {
            const token = getToken();
            if (!token) return;
            axios.post(`${URLs.posts(this.post.id)}`, {
                like: !this.post.liked,
            }, {
                headers: {
                    'X-CSRFTOKEN': token,
                },
            }).then(response => {
                const post = {
                    ...this.post,
                    like_count: this.post.liked ? this.post.like_count - 1 : this.post.like_count + 1,
                    liked: !this.post.liked,
                };
                this.$emit("like-ok", post);
            })
        },
        onDelete(event) {
            const token = getToken();
            if (!token) return;
            axios.delete(`${URLs.posts(this.post.id)}`, {
                headers: {
                    'X-CSRFTOKEN': token,
                },
            }).then(response => {
                this.$emit("delete-ok", this.post.id);
            })
        },
    },
    components: {
        PostBody
    }
}
</script>

<style scoped>
.hover {
    background-color: #f9f9f9;
}
</style>