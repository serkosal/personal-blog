import './editor-style.css'

import EditorJS from '@editorjs/editorjs';

import type { BlockToolConstructable } from '@editorjs/editorjs';

import Paragraph from '@editorjs/paragraph';
import Header from '@editorjs/header';
import List from '@editorjs/list';
import Quote from '@editorjs/quote';
import Warning from '@editorjs/warning';

// const Header = (await import('@editorjs/header')).default
// const List = (await import('@editorjs/list')).default
// const Quote = (await import('@editorjs/quote')).default
// const Warning = (await import('@editorjs/warning')).default
// const Paragraph = (await import('@editorjs/paragraph')).default



const editor = new EditorJS({

  /**
   * Id of Element that should contain Editor instance
   */
  holder: 'editorjs',
  autofocus: true,
  placeholder: 'Let`s write an awesome story!',

  tools: { 
    header: {
      class: Header as unknown as BlockToolConstructable, 
      inlineToolbar: true 
    }, 
    list: { 
      class: List, 
      inlineToolbar: true 
    },
    quote: {
      class: Quote,
      inlineToolbar: true
    },
    warning: {
      class: Warning,
      inlineToolbar: true,
      config: {
        titlePlaceholder: 'Warning title',
        messagePlaceholder: 'warning message warning',
      },
    },
    paragraph: {
      class: Paragraph as unknown as BlockToolConstructable,
      inlineToolbar: true
    }
  }, 
});

try {
  await editor.isReady;
  console.log('Editor.js is ready to work!')
  /** Do anything you need after editor initialization */
} catch (reason) {
  console.log(`Editor.js initialization failed because of ${reason}`)
}