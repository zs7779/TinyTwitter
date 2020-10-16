<template>
    <div class="card p-3">
        <new-post v-if="editMode" v-bind:oldPost="post" v-bind:noPost="true" v-on:post-ok="onEdit($event)">
            <button type="button" class="btn btn-outline-secondary rounded-pill py-0" v-on:click.prevent="editMode=false">Cancel</button>
        </new-post>
        <router-link :to='{name: "post", params: {username: post.author.username, post_id: post.id}}' tag='div' class="card-text card-view" v-else>
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
                <button type="button" class="btn btn-transparent px-1 py-0" title="Like" v-on:click="onLike">
                    <b-icon icon="heart" v-bind:class="[post.liked ? 'card-button-active' : 'card-button', '']"></b-icon> {{ post.like_count }}
                </button>
                <b-dropdown id="dropdown-dropup" dropup variant="btn btn-transparent px-1 py-0" no-caret title="Options">
                    <template v-slot:button-content><b-icon icon="chevron-up" class="card-button"></b-icon></template>
                    <b-dropdown-item v-if="post.owner" v-on:click="onDelete"><b-icon icon="x" class="card-button"></b-icon> Delete</b-dropdown-item>
                    <b-dropdown-item v-if="post.owner" v-on:click="editMode=true"><b-icon icon="pencil" class="card-button"></b-icon> Edit</b-dropdown-item>
                    <b-dropdown-item><b-icon icon="share" class="card-button"></b-icon> Share</b-dropdown-item>
                </b-dropdown>
            </div>
        </div>
    </div>
</template>

<script>
import NewPost from './NewPost.vue'
import { printError, getToken, viewsMixin } from './utils'


export default{
    name: "post-card",
    props: {
        post: Object,
    },
    data() {
        return {
            editMode: false,
        }
    },
    methods: {
        onLike: function(event) {
            const token = getToken();
            if (!token) {return;}
            axios.put(`/posts/${this.post.id}`, {
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
                }
                this.$emit("edit-ok", post);
            }, printError)
        },
        onEdit: function(postText) {
            const token = getToken();
            if (!token) {return;}
            axios.put(`/posts/${this.post.id}`, {
                postText: postText,
            }, {
                headers: {
                    'X-CSRFTOKEN': token,
                },
            }).then(response => {
                const post = {
                    ...this.post,
                    text: postText,
                }
                this.$emit("edit-ok", post);
                this.editMode = false;
            }, printError)
        },
        onDelete: function(event) {
            const token = getToken();
            if (!token) {return;}
            axios.delete(`/posts/${this.post.id}`, {
                headers: {
                    'X-CSRFTOKEN': token,
                },
            }).then(response => {
                this.$emit("delete-ok", this.post.id);
            }, printError)
        },
    },
    components: {
        NewPost
    }
}
</script>

<style scoped>
</style>