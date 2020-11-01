import { shallowMount } from '@vue/test-utils'
import PostView from '../src/components/PostView'
import mockData from './mock_data'


const factory = () => {
    return shallowMount(PostView, {
        data() {
            return {post: mockData.posts[0]}
        },
        // mocks: {
        //     'post-card': function() {},
        // },
    });
}


describe('PostView render', () => {
    let wrapper;
    afterEach(() => {
        wrapper.destroy();
    });
    it('Render default', () => {
        wrapper = factory();
        console.log(wrapper.vm.$data);
        // wrapper.setData({post: mockData.posts[0]});
        expect(wrapper.html()).toMatchSnapshot();
    });
})

describe('PostView Events', () => {
    // let wrapper;
    // beforeEach(() => {
    //     wrapper = wrapper = factory({});
    // });
    // afterEach(() => {
    //     wrapper.destroy();
    // });
    // it('Action comment', () => {
    //     wrapper.findComponent(PostBody).vm.$emit('action-comment');
    //     expect(wrapper.emitted('action-post').length).toBe(1);
    // });
})