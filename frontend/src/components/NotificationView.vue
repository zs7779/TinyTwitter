<template>
    <div class="info-panel border-left border-right">
        <ul class="nav nav-tabs">
            <li class="nav-item">
                <router-link :to="{ name: 'notificationsReplies' }" class="text-center nav-link">
                    Posts
                </router-link>
            </li>
            <li class="nav-item">
                <router-link :to="{ name: 'notificationsMentions' }" class="text-center nav-link">
                    Mentions
                </router-link>
            </li>
        </ul>
        <transition-group name="fade">
            <notice-card v-for='post in notices'
                :key="post.id" :post='post' :type='type'
            />
        </transition-group>
    </div>
</template>

<script>
import NoticeCard from './NoticeCard.vue'
import { URLs, PLACEHOLDERs } from './utils'

export default{
    name: "notification-view",
    props: ['path'],
    data () {
        return {
            notices: PLACEHOLDERs.posts(),
            after: {replies: 0, mentions: 0},
            count: 20,
        }
    },
    computed: {
        type() {
            if (this.path === 'mentions') {
                return this.path;
            } else {
                return 'replies';
            }
        },
    },
    methods: {
        getNotices() {
            if (this.after[this.type] < this.notices.length) {
                this.after[this.type] = this.notices.length;
                return;
            }
            const path_now = this.type;
            axios.get(URLs.currentUser(this.type), {
                params: {
                    after: this.after[this.type],
                    count: this.count,
                },
            }).then(response => {
                if (path_now === this.type) {
                    this.appendNotices(response.data.user.notices);
                    this.after[this.type] += this.count;
                }
            })
        },
        appendNotices(notices) {
            notices.forEach(n => {
                this.notices.push(n);
            })
        },
        scroll() {
            window.onscroll = () => {
                let bottomOfWindow = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight;
                if (this.notices.length > 0 && bottomOfWindow) {
                    this.getNotices();
                }
            };
        },
        resetView() {
            this.notices = PLACEHOLDERs.posts();
            this.after = {replies: 0, mentions: 0};
            this.count = 20;
        },
    },
    watch: {
        $route() {
            this.resetView();
            this.getNotices();
        },
    },
    created() {
        this.getNotices();
    },
    mounted() {
        this.scroll();
    },
    components: {
        NoticeCard,
    },
}
</script>

<style scoped>
.nav-item {
    width: 50%;
}
.nav-link {
    color: #808080;
    font-weight: 500;
}
.nav-link.router-link-exact-active {
    color: #00a2ff;
    border-bottom: 4px solid #60c5ff;
}
</style>