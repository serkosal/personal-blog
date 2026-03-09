import './editor-style.css'

import { Crepe } from "@milkdown/crepe";
import type { DefaultValue } from "@milkdown/core";
import "@milkdown/crepe/theme/common/style.css";
/**
 * Available themes:
 * frame, classic, nord
 * frame-dark, classic-dark, nord-dark
 */
import "@milkdown/crepe/theme/nord-dark.css";
let defaultVal = document.getElementById("initial-id_content") as 
    (HTMLInputElement | null);

let initialContent;
if (defaultVal) {
    const obj: {content: string} = JSON.parse(defaultVal.value)
    initialContent = obj.content; 
}
else {
    let el = new HTMLDivElement()
    el.innerText = "Hello, from milfdown!"
    initialContent = {
        type: "html",
        dom: el
    } satisfies DefaultValue;
}

const crepe = new Crepe({
  root: "#milkdownjs",
  defaultValue: initialContent,
});


crepe.create().then(() => {
    console.log('Milfdown is ready to work!')

    let submit_form  = <HTMLFormElement>document.getElementById("milkdown-save")?.parentElement;
    submit_form?.addEventListener('submit', async function (ev) {

        ev.preventDefault();

        const contentMARKDOWN = crepe.getMarkdown();

        // console.log(contentMARKDOWN);
        const contentJSON = {"content": contentMARKDOWN};
        

        const formData = new FormData(submit_form);
        formData.append('content', JSON.stringify(contentJSON));

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

}).catch(reason => {
    console.log(`Milfdown editor initialization failed because of ${reason}`)
});

// To destroy the editor
// crepe.destroy();