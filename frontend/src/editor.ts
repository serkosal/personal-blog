import './editor.css'
import { Crepe } from "@milkdown/crepe";
// import type { DefaultValue } from "@milkdown/core";

// import "../node_modules/@milkdown/crepe/src/theme/common/style.css";
// import "@milkdown/crepe/theme/common/style.css";
/**
 * Available themes:
 * frame, classic, nord
 * frame-dark, classic-dark, nord-dark
 */
// import "@milkdown/crepe/theme/nord-dark.css";
// import "../node_modules/@milkdown/crepe/src/theme/nord-dark/style.css";

const contentEL = document.getElementById("initial-id_content") as
    (HTMLInputElement | null);
const initialContent = contentEL?.value || "Hello, from milfdown!";


const crepe = new Crepe({
    root: "#milkdownjs",
    defaultValue: initialContent
});


crepe.create().then(() => {
    console.log('Milfdown is ready to work!')

    let submit_form = <HTMLFormElement>document.getElementById("milkdown-save")?.parentElement;
    submit_form?.addEventListener('submit', async function (ev) {

        ev.preventDefault();

        const contentMARKDOWN = crepe.getMarkdown();

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

}).catch(reason => {
    console.log(`Milfdown editor initialization failed because of ${reason}`)
});

// To destroy the editor
// crepe.destroy();