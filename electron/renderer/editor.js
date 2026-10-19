
import * as monaco from "monaco-editor";
import EditorWorker from "../node_modules/monaco-editor/esm/vs/editor/editor.worker.js?worker";

self.MonacoEnvironment = {
    getWorker: function () {
        return new EditorWorker();
    }
};

var monacoEditor;



monaco.editor.defineTheme("hobbySpark-dark", {
    base: "vs-dark",
    inherit: true,
    rules: [
        {
            token: "comment",
            foreground: "777D8A",
            fontStyle: "italic"
        },
        {
            token: "keyword",
            foreground: "D8A7DF"
        },
        {
            token: "string",
            foreground: "E6B89C"
        },
        {
            token: "number",
            foreground: "B8D7A3"
        }
    ],
    colors: {
        // Main editor
        "editor.background": "#111216",
        "editor.foreground": "#E5E7EB",
        "editorLineNumber.foreground": "#555966",
        "editorLineNumber.activeForeground": "#FBBF24",
        "editorCursor.foreground": "#FBBF24",

        // Selection and current line
        "editor.selectionBackground": "#4B4024",
        "editor.inactiveSelectionBackground": "#302A20",
        "editor.lineHighlightBackground": "#191A20",

        // Gutter and indentation
        "editorGutter.background": "#111216",
        "editorIndentGuide.background1": "#252731",
        "editorIndentGuide.activeBackground1": "#454958",

        // Scrollbars
        "scrollbarSlider.background": "#45495566",
        "scrollbarSlider.hoverBackground": "#62677899",
        "scrollbarSlider.activeBackground": "#858B98BB",

        // Find and match highlights
        "editor.findMatchBackground": "#66521C",
        "editor.findMatchHighlightBackground": "#4A3C1C",

        // Widgets and popups
        "editorWidget.background": "#1B1D24",
        "editorWidget.border": "#383B45",
        "editorSuggestWidget.background": "#1B1D24",
        "editorSuggestWidget.selectedBackground": "#30343E"
    }
});

monaco.editor.setTheme("hobbySpark-dark");



var editorElement = document.getElementById("editor");

if (!editorElement) {
    throw new Error("Monaco editor container was not found");
}

monacoEditor = monaco.editor.create(editorElement, {
    value: "# No file currently open",
    language: "python",
    theme: "hobbySpark-dark",
    automaticLayout: true,
    minimap: {
        enabled: false
    },
    fontSize: 14,
    tabSize: 4,
    insertSpaces: true,
    scrollBeyondLastLine: false,
    wordWrap: "on"
});

export async function openFile(filepath) {
    const content = await window.hobbySpark.readFile(filepath);
    monacoEditor.setValue(content)
}
export async function clearEditor() {
    monacoEditor.setValue("# No file currently open")
}

