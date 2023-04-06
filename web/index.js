import { h, render } from "https://esm.sh/preact";
import { useEffect, useState } from "https://esm.sh/preact/hooks";
import htm from "https://esm.sh/htm";

const html = htm.bind(h);

function App() {
    const [dictionary, setDictionary] = useState({});

    useEffect(async () => {
        const response = await fetch("./data.json");
        const data = await response.json();
        setDictionary(data);
    }, []);

    return html`<div>
        ${Object.entries(dictionary).map(
            ([key, value]) => html`<div
                dangerouslySetInnerHTML=${{
                    __html: value,
                }}
            />`
        )}
    </div>`;
}

render(html`<${App} />`, document.querySelector("main"));
