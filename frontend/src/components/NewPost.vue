<template>
    <div class="card p-3">
        <form @submit.prevent="onSubmitPost">
            <textarea rows=4 class="form-control border-0" v-model="postText" placeholder="Say something..."></textarea>
            <div class="d-flex justify-content-end mt-2">
                <span class="mx-1">{{ charRemaining }}</span>
                <button type="submit" class="btn btn-primary rounded-pill py-0" :disabled="!postIsValid">Post</button>
                <slot></slot>
            </div>
        </form>
    </div>
</template>

<script>
import { URLs, getToken } from './utils'

export default{
    name: "new-post",
    props: {
        oldPost: {
            type: Object,
            default: function() {
                return {
                    id: null,
                    text: "",
                }
            },
        },
        noPost: {
            type: Boolean,
            default: function() {
                return false;
            },
        },
    },
    data() {
        return {
            postText: this.oldPost.text,
        };
    },
    computed: {
        charRemaining() {
            this.postText = this.postText.substr(0, 140);
            return `${this.postText.length}/140`;
        },
        postIsValid() {
            return (this.postText.length > 0) && (this.postText.length <= 140);
        }
    },
    methods: {
        onSubmitPost(event) {
            if (this.postText.length == 0) return;
            const token = getToken();
            if (!token) return;
            if (this.noPost) {
                this.$emit("action-post", this.postText);
            } else {
                axios.post(`${URLs.posts()}`, {
                    text: this.postText,
                }, {
                    headers: {
                        'X-CSRFTOKEN': token,
                    },
                }).then(response => {
                    this.postText = "";
                    this.$emit("action-post");
                })
            }
        },
    },
}
</script>

<style scoped>
</style>