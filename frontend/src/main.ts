import './style.css'

import { setupCounter } from './counter.ts'

import EditorJS from '@editorjs/editorjs';

import type { BlockToolConstructable } from '@editorjs/editorjs';

import Header from '@editorjs/header';
import List from '@editorjs/list';
import Quote from '@editorjs/quote';
import Warning from '@editorjs/warning'
import Paragraph from '@editorjs/paragraph';

document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
  <div>
    <h1>Vite + TypeScript</h1>
    <div class="card">
      <button id="counter" type="button"></button>
    </div>
    <div id="editorjs">
    </div>
  </div>
`
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

setupCounter(document.querySelector<HTMLButtonElement>('#counter')!)

try {
  await editor.isReady;
  console.log('Editor.js is ready to work!')
  /** Do anything you need after editor initialization */
} catch (reason) {
  console.log(`Editor.js initialization failed because of ${reason}`)
}