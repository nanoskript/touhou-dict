import { h, render } from "https://cdn.skypack.dev/preact@10.11.2?min";
import { useEffect, useState } from "https://cdn.skypack.dev/preact@10.11.2/hooks?min";
import htm from "https://cdn.skypack.dev/htm@3.1.1?min";

// Initialize htm with Preact.
const html = htm.bind(h);

// TODO: Improve filtering.
function filterEntries(data, term) {
    const entries = [];
    for (const [key, value] of Object.entries(data)) {
        if (!key.toLowerCase().includes(term.toLowerCase())) continue;
        const keywords = key.split("|");

        entries.push({
            score: keywords[0].length,
            __html: value,
        });
    }

    entries.sort((a, b) => a.score - b.score);
    return entries;
}

const TermSearchForm = ({ query, updateQuery }) => {
    const [string, setString] = useState(query.get("term") || "");
    return html`
        <form onsubmit=${(e) => {
            e.preventDefault();
            updateQuery("term", string);
        }}>
            <div class="term-search-form">
                <input type="text" value=${string} class="term-search-input"
                       placeholder="Search term" autocomplete="off"
                       autocapitalize="none" spellcheck="false"
                       oninput=${(e) => setString(e.target.value)}/>
                <input type="submit" value="Filter"/>
            </div>
        </form>
    `;
};

const EntryList = ({ query }) => {
    const [data, setData] = useState(null);
    const string = (query.get("term") || "").trim();

    useEffect(async () => {
        const response = await fetch("./data.json");
        setData(await response.json());
    }, []);

    if (!data) {
        return html`
            <h2 style="text-align: center; margin-top: 8rem;">
                Girls are preparing...
            </h2>
        `;
    }

    const entries = filterEntries(data, string);
    if (entries.length === 0) {
        return html`
            <h2 style="text-align: center; margin-top: 8rem;">
                No results found
            </h2>
        `;
    }

    return html`
        ${entries.map(
            ({ __html }) => html`<div
                class="entry"
                dangerouslySetInnerHTML=${{ __html }}
            />`
        )}
    `;
};

function Page() {
    const pageLoadQuery = new URL(window.location).searchParams;
    const [query, setQuery] = useState(pageLoadQuery);

    const updateQuery = (key, value) => {
        const url = new URL(window.location);
        url.searchParams.set(key, value);
        window.history.pushState(null, "", url.toString());
        setQuery(url.searchParams);
    };

    return html`
        <${TermSearchForm} query=${query} updateQuery=${updateQuery}/>
        <${EntryList} query=${query}/>
    `;
}

render(html`<${Page}/>`, document.querySelector("main"));
