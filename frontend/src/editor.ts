import './editor-style.css'

import EditorJS from '@editorjs/editorjs';

import type { BlockToolConstructable, EditorConfig, OutputData } from '@editorjs/editorjs';

import Paragraph from '@editorjs/paragraph';
import Header from '@editorjs/header';
import List from '@editorjs/list';
import Quote from '@editorjs/quote';
import Warning from '@editorjs/warning';
import Table from '@editorjs/table'


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
        },
        table: {
            class: Table as unknown as BlockToolConstructable,
            inlineToolbar: true,
            config: {
                rows: 2,
                cols: 3,
                maxRows: 5,
                maxCols: 5,
            },
        }
    },
};

/*
 retrieve initial value from initial-id_content
*/
const initialContent = 
    document.getElementById("initial-id_content") as (HTMLInputElement | null);

if (initialContent) {
    try {
        const initialData: OutputData = JSON.parse(initialContent.value);
        editorConfig.data = initialData;
    }
    catch (error)
    {
        console.log(error)
    }
}

const editor = new EditorJS(editorConfig);

let submit_form  = <HTMLFormElement>document.getElementById("editorjs-save")?.parentElement;
submit_form?.addEventListener('submit', async function (ev) {

    ev.preventDefault();

    editor.save().then(async (outputData) =>  {
        const contentJSON = JSON.stringify(outputData);

        const formData = new FormData(submit_form);
        formData.append('content', contentJSON);

        const response = await fetch(submit_form.action, {
            method: 'POST',
            body: formData,
        });

        const result = await response.text();
        console.log(result);

    }).catch((error) => {
        console.log('Saving failed: ', error);
    })
});


try {
    await editor.isReady;
    console.log('Editor.js is ready to work!')
} catch (reason) {
    console.log(`Editor.js initialization failed because of ${reason}`)
}