<template>
    <div :class="[hovering ? 'hover':'', 'card p-3']" @mouseover='hovering=true' @mouseout='hovering=false'>
        <new-post v-if="editMode" :oldPost="post" :noPost="true" @post-ok="onEdit($event)">
            <button type="button" class="btn btn-outline-secondary rounded-pill py-0" @click.prevent="editMode=false">Cancel</button>
        </new-post>
        <router-link v-else :to='{name: "post", params: {username: post.author.username, postID: post.id}}' tag='div' class="card-text card-view">
            <h6 class="card-title mb-1">
                <router-link :to="{ name: 'user', params: {username: post.author.username} }">{{ post.author.username }}</router-link>
                <span class="small text-muted">at {{ post.create_time }} said:</span>
            </h6>
            <p>{{ post.text }}</p>
        </router-link>
        <div class="card-footer bg-transparent p-0">
            {{ post.like_count }} likes
        </div>
        <div class="card-footer bg-transparent p-0">
            <div class="d-flex justify-content-around">
                <button type="button" class="btn btn-transparent px-1 py-0" title="Comment">
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
                    <b-dropdown-item v-if="post.owner" @click="editMode=true"><b-icon icon="pencil" class="card-button"></b-icon> Edit</b-dropdown-item>
                    <b-dropdown-item><b-icon icon="share" class="card-button"></b-icon> Share</b-dropdown-item>
                </b-dropdown>
            </div>
        </div>
    </div>
</template>

<script>
import NewPost from './NewPost.vue'

export default{
    name: "post-card",
    props: ['post'],
    data() {
        return {
            editMode: false,
            hovering: false,
        }
    },
    methods: {
        onLike: function(event) {
            const post = {
                ...this.post,
                like_count: this.post.liked ? this.post.like_count - 1 : this.post.like_count + 1,
                liked: !this.post.liked,
            }
            this.$emit("action-like", post);
        },
        onEdit: function(postText) {
            const post = {
                ...this.post,
                text: postText,
            }
            this.$emit("action-edit", post);
        },
        onDelete: function(event) {
            this.$emit("action-delete", this.post.id);
        },
    },
    watch: {
        post: function() {
            this.editMode = false;
        }
    },
    components: {
        NewPost
    }
}
</script>

<style scoped>
.hover {
    background-color: #f9f9f9;
}
</style>