import './post.css'

import hljs from 'highlight.js/lib/core';

import bash from 'highlight.js/lib/languages/bash';
import c from 'highlight.js/lib/languages/c';
import cmake from 'highlight.js/lib/languages/cmake';
import cpp from 'highlight.js/lib/languages/cpp';
import csharp from 'highlight.js/lib/languages/csharp';
import css from 'highlight.js/lib/languages/css';
import diff from 'highlight.js/lib/languages/diff';
import dockerfile from 'highlight.js/lib/languages/dockerfile';
import glsl from 'highlight.js/lib/languages/glsl';
import go from 'highlight.js/lib/languages/go';
import java from 'highlight.js/lib/languages/java';
import javascript from 'highlight.js/lib/languages/javascript';
import latex from 'highlight.js/lib/languages/latex';
import markdown from 'highlight.js/lib/languages/markdown';
import nginx from 'highlight.js/lib/languages/nginx';
import python from 'highlight.js/lib/languages/python';
import rust from 'highlight.js/lib/languages/rust';
import typescript from 'highlight.js/lib/languages/typescript';
import yaml from 'highlight.js/lib/languages/yaml';

export function registerLanguages() {
    hljs.registerLanguage('bash', bash);
    hljs.registerLanguage('c', c);
    hljs.registerLanguage('cpp', cpp);
    hljs.registerLanguage('cmake', cmake);
    hljs.registerLanguage('csharp', csharp);
    hljs.registerLanguage('css', css);
    hljs.registerLanguage('diff', diff);
    hljs.registerLanguage('dockerfile', dockerfile);
    hljs.registerLanguage('glsl', glsl);
    hljs.registerLanguage('go', go);
    hljs.registerLanguage('java', java);
    hljs.registerLanguage('javascript', javascript);
    hljs.registerLanguage('latex', latex);
    hljs.registerLanguage('markdown', markdown);
    hljs.registerLanguage('nginx', nginx);
    hljs.registerLanguage('python', python);
    hljs.registerLanguage('rust', rust);
    hljs.registerLanguage('typescript', typescript);
    hljs.registerLanguage('yaml', yaml);
}
registerLanguages();
hljs.highlightAll();