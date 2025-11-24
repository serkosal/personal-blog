import './style.css'

import { setupCounter } from './counter.ts'

import EditorJS from '@editorjs/editorjs';


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
  holder: 'editorjs'
});

setupCounter(document.querySelector<HTMLButtonElement>('#counter')!)

try {
  await editor.isReady;
  console.log('Editor.js is ready to work!')
  /** Do anything you need after editor initialization */
} catch (reason) {
  console.log(`Editor.js initialization failed because of ${reason}`)
}