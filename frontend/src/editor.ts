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


const editorEL = document.getElementById("milkdownjs") as HTMLTextAreaElement | null;
if (editorEL) {

    // view mode radio buttons
    const radioSwitchPreview = editorEL.appendChild(document.createElement('fieldset'));
    radioSwitchPreview.innerHTML = 
        '<legend> View mode </legend>' +

        '<label for="markdownView">Markdown view</label>\n' + 
        '<input type="radio" name="viewMode" id="markdownView" value="markdownView" checked />\n' + 

        '<label for="htmlPreview">HTML preview</label>\n' + 
        '<input type="radio" name="viewMode" id="htmlPreview" value="htmlPreview" />'
    ;

    // on radio button change
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

    // textarea
    const textAreaEl = editorEL.appendChild(document.createElement('textarea'));
    textAreaEl.rows = 30;
    textAreaEl.cols = 90;

    const contentEL = document.getElementById("initial-id_content") as (HTMLInputElement | null);
    const initialContent = contentEL?.value || "# header !";

    textAreaEl.value = initialContent;

    // textAreaEl.oninput = (_) => {
    //     textAreaEl.innerHTML = hljs.highlight(textAreaEl.value, {language: 'markdown'}).value;
    // }

    // preview element
    const previewHtmlEl = editorEL.appendChild(document.createElement('div'));
    previewHtmlEl.setAttribute('hidden', '');

    // submit button
    const submit_form = <HTMLFormElement>document.getElementById("milkdown-save")?.parentElement;

    submit_form?.addEventListener('submit', async function (ev) {

        ev.preventDefault();

        const contentMARKDOWN = textAreaEl.value;

        const formData = new FormData(submit_form);
        formData.append('content', contentMARKDOWN);

        const response = await fetch(submit_form.action, {
            method: 'POST',
            body: formData,
        });


        if (response.redirected) {
            window.location.href = response.url;
        } else {
            const result = await response.text();
            console.log(result);
        }
    });
}