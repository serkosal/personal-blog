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
    
    initialContent = defaultVal.value;
    console.log("Default value", defaultVal)
}
else {
    let el = new HTMLDivElement()
    el.innerText = "Hello, from milfdown!"
    initialContent = {
        type: "html",
        dom: el
    } satisfies DefaultValue;
    console.log("Default value", el);
}

const crepe = new Crepe({
  root: "#milkdownjs",
  defaultValue: initialContent,
});

crepe.create().then(() => {
    console.log('Milfdown is ready to work!')
}).catch(reason => {
    console.log(`Milfdown editor initialization failed because of ${reason}`)
});

// To destroy the editor
// crepe.destroy();