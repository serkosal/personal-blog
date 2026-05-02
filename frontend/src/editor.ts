import './editor.css'
import './post.css'

import hljs from 'highlight.js/lib/core';
import markdownit from 'markdown-it';

import {registerLanguages} from './post.ts';

registerLanguages();
const md = markdownit('default', {
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(str, {language: lang}).value;
      }
      catch (__) {}
    }

    return '';
  },
  html: false,
  breaks: true
});

function initEditor(editor: HTMLTextAreaElement) {
    if (!editor) return;

    // textarea
    const textAreaEl = editor.querySelector('textarea') as HTMLTextAreaElement | null;
    if (!textAreaEl) return;
    textAreaEl.rows = 30;
    textAreaEl.cols = 90;

    // initial value
    const initialContentEL = editor.querySelector("#initial-id_content") as HTMLInputElement | null;
    const initialContent = initialContentEL?.value || "# header !";
    textAreaEl.value = initialContent;

    const radioSwitchPreview = editor.querySelector('fieldset');
    const previewHtmlEl = editor.querySelector('#HTMLPreview');

    if (!radioSwitchPreview || !previewHtmlEl) return;

    radioSwitchPreview.onchange = (_) => {
        const htmlPreviewRadioButton = radioSwitchPreview.querySelector<HTMLInputElement>('#htmlPreview');

        if (htmlPreviewRadioButton && htmlPreviewRadioButton.checked) {
            previewHtmlEl.removeAttribute('hidden');
            textAreaEl.setAttribute('hidden', '');
            previewHtmlEl.innerHTML = md.render(textAreaEl.value);
        }
        else {
            previewHtmlEl.setAttribute('hidden', '');
            textAreaEl.removeAttribute('hidden');
            textAreaEl.innerHTML = hljs.highlight(textAreaEl.value, {language: 'markdown'}).value;
        }
    }
}

interface IFormErrors {
    "title": Array<string>,
    "slug": Array<string>,
    "id_tags": Array<string>
};
interface IFormResponse {
    "success": "true" | "false",
    "errors": IFormErrors
};

function handleErrors(form: HTMLFormElement, errors: IFormErrors) {
    // fields: 'title', 'slug', 'tags'

    for (let key in errors) {
        const typedKey = key as keyof IFormErrors;

        const el = form.querySelector(`#id_${key}`)?.parentElement;
        const errorsSelector = `id_${key}_errors`;

        if (el && el.querySelector('#' + errorsSelector) === null) {
            const errors_el = document.createElement('div');
            errors_el.id = errorsSelector;
            errors_el.style = 'color: red;';
            el.appendChild(errors_el);
        }

        let errors_el = <HTMLDivElement>el?.querySelector('#' + errorsSelector);
        if (errors_el) {
            
            errors_el.innerText = errors[typedKey][0];
        }
    }
}

function handleSave(editor: HTMLTextAreaElement) {

    const submit_form = <HTMLFormElement>editorEL?.parentElement?.parentElement;
    const textAreaEl = editor.querySelector('textarea') as HTMLTextAreaElement | null;

    submit_form?.addEventListener('submit', async function (ev) {

        ev.preventDefault();

        const contentMARKDOWN = textAreaEl?.value;

        const formData = new FormData(submit_form);
        formData.append('content', contentMARKDOWN ?? "");

        const response = await fetch(submit_form.action, {
            method: 'POST',
            body: formData,
        });

        if (response.redirected) {
            window.location.href = response.url;
        } else {
            const result: IFormResponse = await response.json();
            if (result.success == "false") {
                handleErrors(submit_form, result.errors);
            }
        }
    });

}


const editorEL = document.getElementById("GFM-Editor") as HTMLTextAreaElement | null;
if (editorEL) {

    initEditor(editorEL);
    handleSave(editorEL);

    // doesn't work on textarea thus it escapes html
    // textAreaEl.oninput = (_) => {
    //     textAreaEl.innerHTML = hljs.highlight(textAreaEl.value, {language: 'markdown'}).value;
    // }
    
}