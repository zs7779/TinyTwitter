<template>
    <div :class="[hovering ? 'hover':'', 'p-sm-3 p-1 card']" @mouseover='hovering=true' @mouseout='hovering=false'>
        <router-link
            tag='div'
            :to='{name: "post", params: {username: post.author.username, postID: post.id}}'
        >
            <h6 class="card-title mb-1">
                <router-link :to="{ name: 'user', params: {username: post.author.username} }">
                    <img :src='post.author.avatar' class='avatar-small'>
                    {{ post.author.username }}
                </router-link>
                <span class="small text-muted">{{ noticeAction }}:</span>
            </h6>
            <p class="small text-muted">
                {{ post.text }}
            </p>
        </router-link>
    </div>
</template>

<script>

export default{
    props: ['post', 'type'],
    data() {
        return {
            hovering: false,
        }
    },
    computed: {
        noticeAction() {
            if (this.type === 'mentions') return 'mentioned you';
            if (this.type === 'replies') {
                if (this.post.is_comment) {
                    return 'replied';
                } else {
                    return 'retweeted';
                }
            }
        },
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
@media (max-width: 575.98px) {
    .card-title {
        font-size: 0.9em;
    }
    .post-mentions {
        font-size: 0.8em;
    }
    .card-text {
        font-size: 0.8em;
    }
    .card-text-primary {
        font-size: 1em;
    }
}
.card-grid {
    display: grid;
    grid-template-columns: 3.25em auto;
}
.avatar {
    width: 3em;
    height: 3em;
    border-radius: 50%;
}
.avatar-small {
    width: 1.25em;
    height: 1.25em;
    border-radius: 50%;
}
</style>