import './editor-style.css'

import EditorJS from '@editorjs/editorjs';

import type { BlockToolConstructable, EditorConfig } from '@editorjs/editorjs';

import Paragraph from '@editorjs/paragraph';
import Header from '@editorjs/header';
import List from '@editorjs/list';
import Quote from '@editorjs/quote';
import Warning from '@editorjs/warning';

import edjsHTML from "editorjs-html";

// const Header = (await import('@editorjs/header')).default
// const List = (await import('@editorjs/list')).default
// const Quote = (await import('@editorjs/quote')).default
// const Warning = (await import('@editorjs/warning')).default
// const Paragraph = (await import('@editorjs/paragraph')).default


let editorConfig: EditorConfig = {

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
};
const editor = new EditorJS(editorConfig);

const edjsParser = edjsHTML();

let submit_form = document.getElementById("editorjs-save")?.parentElement;
submit_form?.addEventListener('submit', function (ev) {
    ev.preventDefault();

    let csrfInput = submit_form?.querySelector<HTMLInputElement>('input[name="csrfmiddlewaretoken"]');
    let csrfStr = csrfInput?.value;

    editor.save().then((outputData) => {
        const outputHTML = edjsParser.parse(outputData);

        console.log('CSRF token: ', csrfStr);
        console.log('Article data: ', outputHTML);
    }).catch((error) => {
        console.log('Saving failed: ', error);
    })
});


try {
    await editor.isReady;
    console.log('Editor.js is ready to work!')
    /** Do anything you need after editor initialization */
} catch (reason) {
    console.log(`Editor.js initialization failed because of ${reason}`)
}