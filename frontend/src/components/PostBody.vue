<template>
    <div :class="[hovering ? 'hover':'', 'p-3']" @mouseover='hovering=true' @mouseout='hovering=false'>
        <router-link
            tag='div'
            :to='{name: "post", params: {username: post.author.username, postID: post.id}}'
            class="card-grid"
        >
            <router-link tag='div' :to="{ name: 'user', params: {username: post.author.username} }">
                <img :src='post.author.avatar' class='avatar'>
            </router-link>
            <div>
                <h6 class="card-title mb-1">
                    <router-link :to="{ name: 'user', params: {username: post.author.username} }">
                        {{ post.author.username }}
                    </router-link>
                    <span class="small text-muted"> {{ postTime }}:</span>
                </h6>
                <div v-if='post.is_comment' class="post-mentions">
                    <span class="small text-muted">Reply to</span>
                    <span class="small text-muted" v-for='m in mentions' :key="m.id">
                        <router-link :to="{ name: 'user', params: {username: m.username} }">@{{ m.username }}</router-link>
                        <span> </span>
                    </span>
                </div>
                <div :class="[verbose ? 'card-text-primary':'card-text-secondary', 'card-text']">
                    <p><span v-for="(part, index) in post.text.split(/([@#]\w+)/g)" :key=index>
                        <router-link v-if="part[0] == '@'" :to="`/${part.slice(1)}`">{{part}}</router-link>
                        <router-link v-else-if="part[0] == '#'" :to="`/hashtags/${part.slice(1)}`">{{part}}</router-link>
                        <template v-else>{{part}}</template>
                    </span></p>
                </div>
                <slot></slot>
            </div>
        </router-link>
        <div v-if='verbose' class="card-footer bg-transparent p-0 ">
            <span>{{ post.repost_count }} Reposts</span> <span>{{ post.like_count }} Likes</span>
        </div>
        <div v-if=buttons class="card-footer bg-transparent p-0">
            <div class="d-flex justify-content-around">
                <button type="button" v-b-modal.new-post class="btn btn-transparent px-1 py-0" title="Comment" @click="$emit('action-comment')">
                    <b-icon icon="chat" :class="[post.commented ? 'card-button-comment' : 'card-button']"></b-icon> {{ comment_count }}
                </button>
                <button type="button" v-b-modal.new-post class="btn btn-transparent px-1 py-0" title="Repost" @click="$emit('action-repost')">
                    <b-icon icon="arrow-repeat" :class="[post.reposted ? 'card-button-repost' : 'card-button']"></b-icon> {{ repost_count }}
                </button>
                <button type="button" class="btn btn-transparent px-1 py-0" title="Like" @click="$emit('action-like')">
                    <b-icon icon="heart" :class="[post.liked ? 'card-button-like' : 'card-button']"></b-icon> {{ like_count }}
                </button>
                <b-dropdown v-if="post.owner" id="dropdown-dropup" dropup variant="btn btn-transparent px-1 py-0" no-caret title="Options">
                    <template v-slot:button-content><b-icon icon="chevron-up" class="card-button"></b-icon></template>
                    <b-dropdown-item @click="$emit('action-delete')" title="Delete">
                        <b-icon icon="x" class="card-button"></b-icon>Delete
                    </b-dropdown-item>
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
        postTime() {
            if (this.post.create_time) {
                let formatTime = this.post.create_time.split(' '); // Hour:Minute ampm Month Day Year 
                let now = new Date();
                now = now.getTime() + now.getTimezoneOffset() * 6e4;
                let diff = now - new Date(this.post.create_time).getTime();
                let days = Math.floor(diff / 864e5);
                let hours = Math.floor(diff % 864e5 / 36e5);
                let minutes = Math.floor(diff % 36e5 / 6e4);
                if (days > 0) {
                    if (days <= 7) return parseInt(formatTime[3]) + 'd';
                    else if (days <= 180) return formatTime[2] + ' ' + parseInt(formatTime[3]);
                    else return this.post.create_time;
                } else if (hours > 0) {
                    return parseInt(hours) + 'h';
                } else if (minutes > 0) {
                    return parseInt(minutes) + 'm';
                } else {
                    return "now";
                }
            }
            return "";
        },
        mentions() {
            var receipants = {};
            if (this.post.mentions) {
                this.post.mentions.forEach(m => {
                    receipants[m.id] = m.username;
                })
            }
            return Object.entries(receipants).map(([k, v]) => {
                return { id: k, username: v, }
            });
        },
        comment_count() {
            return this.post.comment_count > 0 ? this.post.comment_count : ' ';
        },
        repost_count() {
            return this.post.repost_count > 0 ? this.post.repost_count : ' ';
        },
        like_count() {
            return this.post.like_count > 0 ? this.post.like_count : ' ';
        },
    },
}
</script>

<style scoped>
.hover {
    background-color: #f9f9f9;
}
.card-text {
    white-space: pre-line;
}
.card-text-primary {
    font-size: 1.5em;
}
.card-text-secondary {
    -webkit-line-clamp: 16;
    overflow : hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-box-orient: vertical;
}
.card-grid {
    display: grid;
    grid-template-columns: 3em auto;
}
.avatar {
    width: 3em;
    height: 3em;
    border-radius: 50%;
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