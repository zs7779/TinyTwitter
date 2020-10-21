<template>
    <div :class="[hovering ? 'hover':'', 'p-3']" @mouseover='hovering=true' @mouseout='hovering=false'>
        <router-link :to='{name: "post", params: {username: post.author.username, postID: post.id}}' tag='div' :class="[verbose ? 'card-view':'', 'card-text']">
            <h6 class="card-title mb-1">
                <router-link :to="{ name: 'user', params: {username: post.author.username} }">{{ post.author.username }}</router-link>
                <span class="small text-muted">at {{ post.create_time }}:</span>
            </h6>
            <div v-if='post.is_comment'>
                <span class="small text-muted">Reply to</span>
                <span class="small text-muted" v-for='m in mentions' :key="m.id">
                    <router-link :to="{ name: 'user', params: {username: m.username} }">@{{ m.username }}</router-link>
                    <span> </span>
                </span>
            </div>
            <div>
                <p>{{ post.text }}</p>
            </div>
            <slot></slot>
        </router-link>
        <div v-if=buttons class="card-footer bg-transparent p-0">
            <div class="d-flex justify-content-around">
                <button type="button" v-b-modal.new-post class="btn btn-transparent px-1 py-0" title="Comment" @click="$emit('action-comment')">
                    <b-icon icon="chat" :class="[post.commented ? 'card-button-comment' : 'card-button']"></b-icon> {{ post.comment_count }}
                </button>
                <button type="button" v-b-modal.new-post class="btn btn-transparent px-1 py-0" title="Repost" @click="$emit('action-repost')">
                    <b-icon icon="arrow-repeat" :class="[post.reposted ? 'card-button-repost' : 'card-button']"></b-icon> {{ post.repost_count }}
                </button>
                <button type="button" class="btn btn-transparent px-1 py-0" title="Like" @click="$emit('action-like')">
                    <b-icon icon="heart" :class="[post.liked ? 'card-button-like' : 'card-button']"></b-icon> {{ post.like_count }}
                </button>
                <b-dropdown id="dropdown-dropup" dropup variant="btn btn-transparent px-1 py-0" no-caret title="Options">
                    <template v-slot:button-content><b-icon icon="chevron-up" class="card-button"></b-icon></template>
                    <b-dropdown-item v-if="post.owner" @click="$emit('action-delete')"><b-icon icon="x" class="card-button"></b-icon> Delete</b-dropdown-item>
                    <b-dropdown-item v-b-modal.new-post v-if="post.owner" @click="$emit('action-edit')"><b-icon icon="pencil" class="card-button"></b-icon> Edit</b-dropdown-item>
                    <b-dropdown-item><b-icon icon="share" class="card-button"></b-icon> Share</b-dropdown-item>
                </b-dropdown>
            </div>
        </div>
    </div>
</template>

<script>
export default{
    props: ['post', 'buttons', 'verbose'],
    data() {
        return {
            hovering: false,
        }
    },
    computed: {
        mentions() {
            var receipants = {};
            if (this.post.root_post) {
                receipants[this.post.root_post.author.id] = this.post.root_post.author.username;
            }
            if (this.post.parent) {
                receipants[this.post.parent.author.id] = this.post.parent.author.username;
            }
            if (this.post.mentions) {
                this.post.mentions.forEach(m => {
                    receipants[m.id] = m.username;
                })
            }
            return Object.entries(receipants).map(([k, v]) => {
                return { id: k, username: v, }
            });
        },
    }
}
</script>

<style scoped>
.hover {
    background-color: #f9f9f9;
}
.card-button {
    color: #909090;
}

.card-button-comment {
    color: darkturquoise;
}
.card-button-repost {
    color: limegreen;
}
.card-button-like {
    color: red;
}
</style>