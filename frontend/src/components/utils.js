const URLs = {
    posts: (postID='') => `/api/posts/${postID}`,
    users: (userID='') => `/api/users/${userID}`,
    usersPosts: (userID='', postID='') => `/api/users/${userID}/posts/${postID}`,
};


const SIGNALs = {
    updatePost: 'edit-ok',
    deletePost: 'delete-ok',
    fetchPosts: 'post-ok',
    updateUser: 'user-ok',
};


const PLACEHOLDERs = {
    user: {id: -1, username: 'username'},
    post: {
        author: {id: -1, username: 'username'},
        id: -1,
        text: "",
        create_time: null,
        like_count: null,
    },
    posts: [],
    postParams: {
        isComment: false,
        oldPost: null,
        parentPost: null,
        parentComment: null,
    },
}


function printError(error) {
    if (error.response) {
      console.log(error.response.data);
      console.log(error.response.status);
      console.log(error.response.headers);
    } else if (error.request) {
      console.log(error.request);
    } else {
      console.log('Error', error.message);
    }
}


function getToken() {
    const csrftoken = Cookies.get('csrftoken');
    if (csrftoken) {
        return csrftoken;
    }
    window.location.href = "/login/";
    return false;
}


export {
    URLs,
    SIGNALs,
    PLACEHOLDERs,
    printError,
    getToken,
}