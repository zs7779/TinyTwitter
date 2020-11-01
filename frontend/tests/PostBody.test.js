import { mount } from '@vue/test-utils'
import PostBody from '../src/components/PostBody'
import mockData from './mock_data'


const factory = (post={}, buttons=false, verbose=false) => {
    return mount(PostBody, {
        stubs: ['router-link', 'b-icon', 'b-modal', 'b-dropdown', 'b-dropdown-item'],
        directives: {
            'b-modal': function() {},
        },
        propsData: {
            post: {
                ...mockData.posts[0],
                ...post,
            },
            buttons,
            verbose
        }
    });
}


describe('PostBody render', () => {
    it('Render default', () => {
        const wrapper = factory();
        expect(wrapper.html()).toMatchSnapshot();
    });
    it('Render buttons', () => {
        const wrapper = factory({}, true, false);
        expect(wrapper.html()).toMatchSnapshot();
    });
    it('Render verbose', () => {
        const wrapper = factory({}, true, false);
        expect(wrapper.html()).toMatchSnapshot();
    });
    it('Render comment', () => {
        const wrapper = factory({
            is_comment: true,
            root_post: mockData.posts[1],
            parent: mockData.comments[1],
        });
        expect(wrapper.html()).toMatchSnapshot();
    });
    it('Render repost', () => {
        const wrapper = factory({
            parent: mockData.posts[1],
        });
        expect(wrapper.html()).toMatchSnapshot();
    });
})

describe('PostBody comments', () => {
    it('Reply root', () => {
        const wrapper = factory({
            is_comment: true,
            root_post: mockData.posts[1],
        });
        expect(wrapper.find('.post-mentions').text()).toMatch(new RegExp(mockData.posts[1].author.username));
    });
    it('Reply parent', () => {
        const wrapper = factory({
            is_comment: true,
            parent: mockData.comments[1],
        }, false, false);
        expect(wrapper.find('.post-mentions').text()).toMatch(new RegExp(mockData.posts[1].author.username));
    });
    it('Not comment', () => {
        const wrapper = factory({
            parent: mockData.posts[1],
        }, false, false);
        expect(wrapper.find('.post-mentions').exists()).toBeFalsy();
    });
})