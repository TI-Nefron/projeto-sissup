import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import DocumentViewer from '../DocumentViewer.vue';
import { createVuetify } from 'vuetify';
import 'resize-observer-polyfill';

// Mock Vuetify
const vuetify = createVuetify({});

describe('DocumentViewer.vue', () => {
  it('renders iframes with correct urls when dialog is opened', async () => {
    const wrapper = mount(DocumentViewer, {
      props: {
        modelValue: true, // Start with the dialog open
        doc1url: 'http://example.com/doc1.pdf',
        doc2url: 'http://example.com/doc2.pdf',
      },
      global: {
        plugins: [vuetify],
      },
    });

    // Wait for component to update
    await wrapper.vm.$nextTick();

    const iframes = wrapper.findAll('iframe');
    expect(iframes.length).toBe(2);
    expect(iframes[0].attributes('src')).toBe('http://example.com/doc1.pdf');
    expect(iframes[1].attributes('src')).toBe('http://example.com/doc2.pdf');
  });

  it('is not visible when modelValue is false', () => {
    const wrapper = mount(DocumentViewer, {
      props: {
        modelValue: false,
        doc1url: '',
        doc2url: '',
      },
      global: {
        plugins: [vuetify],
      },
    });

    // The dialog content is rendered but not visible.
    // We check if the dialog component's internal value is false.
    expect(wrapper.vm.dialog).toBe(false);
  });
});