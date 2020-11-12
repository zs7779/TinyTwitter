<template>
    <div>
        <slot></slot>
        <b-modal id='new-post' title=''
            @ok.prevent="doSubmitPost"
            @show="checkToken"
            @hidden="doClear"
        >
            <textarea rows=4 class="form-control border-0" v-model="postText" placeholder="Say something..."></textarea>
            <input type="file" name="file" ref='fileUpload' @change="onFileUpload($event.target.files)" class="d-none" />
            <template v-slot:modal-footer="{ ok }">
                <button type='button' title='Upload image' class="btn btn-transparent" @click="$refs.fileUpload.click()">
                    <b-icon icon="image"></b-icon>{{filename}}
                </button>
                <span class="mx-1">{{ charRemaining }}</span>
                <b-button size="sm" variant="primary" @click="ok()" :disabled="!postIsValid" class="rounded-pill py-0">
                    Post
                </b-button>
            </template>
        </b-modal>
    </div>
</template>

<script>
import { URLs, getToken, printError } from './utils'

export default{
    name: "new-post",
    props: ['postParams'],
    data() {
        return {
            postText: '',
            postMedia: null,
            fileList: [],
            token: null,
        };
    },
    computed: {
        filename() {
            if (this.fileList.length === 0) return "";
            return this.fileList[0].name;
        },
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
        onFileUpload(fileList) {
            if (fileList.length == 0) return;
            
            this.fileList = fileList;
        },
        doSendFile() {
            if (this.fileList.length == 0) return;

            return axios.get(URLs.upload())
                .then(response => response.data)
                .then(s3 => {
                    let formData = new FormData();
                    formData.append('key', s3.fields.key);
                    formData.append('AWSAccessKeyId', s3.fields.AWSAccessKeyId);
                    formData.append('policy', s3.fields.policy);
                    formData.append('signature', s3.fields.signature);
                    formData.append('file', this.fileList[0], this.fileList[0].name);
                    
                    axios.post(s3.url, formData, {
                        headers: {
                            'content-type': "multipart/form-data",
                        }
                    }).then(response => {
                        this.postMedia = s3.url + s3.fields.key;
                        this.doSendText();
                    });
                });
        },
        doSendText() {
            this.postMethod(this.postURL, {
                text: this.postText,
                media: this.postMedia,
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
                this.$bvModal.hide('new-post');
            })
        },
        doSubmitPost() {
            if (this.postText.length == 0 || this.postText.length >= 140) return;

            if (this.fileList.length > 0) {
                this.doSendFile();
            } else {
                this.doSendText();
            }
        },
        doClear() {
            this.$emit('action-clear');
            this.postText = "";
            this.postMedia = null;
            this.fileList = [];
            this.token = null;
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