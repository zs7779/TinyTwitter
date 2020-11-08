<template>
    <div>
        <slot></slot>
        <b-modal id='new-post' title=''
            @ok.prevent="doSubmitPost"
            @show="checkToken"
            @hidden="doClear"
        >
            <textarea rows=4 class="form-control border-0" v-model="postText" placeholder="Say something..."></textarea>
            <template v-slot:modal-footer="{ ok }">
                <span class="mx-1">{{ charRemaining }}</span>
                <b-button size="sm" variant="primary" @click="ok()" :disabled="!postIsValid" class="rounded-pill py-0">
                    Post
                </b-button>
            </template>
        </b-modal>
    </div>
</template>

<script>
import { URLs, getToken } from './utils'

export default{
    name: "new-post",
    props: ['postParams'],
    data() {
        return {
            postText: '',
            token: null,
        };
    },
    computed: {
        charRemaining() {
            this.postText = this.postText.substr(0, 1400);
            return `${this.postText.length}/140`;
        },
        postIsValid() {
            return (this.postText.length > 0) && (this.postText.length <= 140);
        },
        postMethod() {
            if (this.postParams.oldPost) return axios.patch;
            return axios.post;
        },
        postURL() {
            if (this.postParams.oldPost) return `${URLs.usersPosts(this.postParams.oldPost.author.username, this.postParams.oldPost.id)}`;
            if (this.postParams.isComment) return `${URLs.usersPosts(this.postParams.rootPost.author.username, this.postParams.rootPost.id)}`;
            return `${URLs.posts()}`;
        },
    },
    methods: {
        doSubmitPost(event) {
            if (this.postText.length == 0 || this.postText.length >= 140) return;
            this.postMethod(this.postURL, {
                text: this.postText,
                parent_id: this.postParams.parentPost ? this.postParams.parentPost.id : null,
            }, {
                headers: {
                    'X-CSRFTOKEN': this.token,
                },
            }).then(response => {
                if (this.postParams.isComment) {
                    this.$emit('comment-ok', response.data.comment);
                } else if (this.postParams.oldPost) {
                    this.$emit('edit-ok', {
                        ...this.postParams.oldPost,
                        text: this.postText,
                    });
                }
                else this.$emit('post-ok', response.data.post);
                this.$bvModal.hide('new-post')
            })
        },
        doClear() {
            this.$emit('action-clear');
            this.postText = "";
        },
        checkToken(event) {
            if (!this.token) {
                this.token = getToken(this.$root.userAuth);
            }
        },
    },
    watch: {
        postParams() {
            if (this.postParams.oldPost) this.postText = this.postParams.oldPost.text;
        }
    },
    created() {
        if (this.postParams.oldPost) this.postText = this.postParams.oldPost.text;
    }
}
</script>

<style scoped>
</style>