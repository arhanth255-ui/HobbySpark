import { connectPyright } from "./lsp-client.js";
import { editorTabs } from "./app.js";
import * as monaco from "monaco-editor";
import EditorWorker from "../node_modules/monaco-editor/esm/vs/editor/editor.worker.js?worker";
import { Parser, Language, Query } from "web-tree-sitter";
import pythonWasmUrl from "tree-sitter-wasm/python/tree-sitter-python.wasm?url";
import highlightsQuery from "tree-sitter-wasm/python/highlights.scm?raw";

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
        { token: "comment", foreground: "777D8A", fontStyle: "italic" },

        // Keywords: lavender
        { token: "keyword", foreground: "C792EA" },
        { token: "keyword.control", foreground: "C792EA" },
        { token: "keyword.operator", foreground: "89DDFF" },

        // Ordinary names: warm ivory, not blue
        { token: "identifier", foreground: "E5E1D8" },

        // Functions: golden yellow
        { token: "function", foreground: "FFD580" },
        { token: "support.function", foreground: "FFD580" },

        // Types and classes: green
        { token: "type.identifier", foreground: "5F9B70" },
        { token: "type", foreground: "5F9B70" },
        { token: "class", foreground: "5F9B70" },

        // Strings: soft green
        { token: "string", foreground: "C3E88D" },
        { token: "string.escape", foreground: "89DDFF" },

        // Numbers: coral
        { token: "number", foreground: "F78C6C" },

        // Punctuation and operators: cyan
        { token: "delimiter", foreground: "89DDFF" },
        { token: "operator", foreground: "89DDFF" },

        { token: "regexp", foreground: "F07178" }
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
monacoEditor.addCommand(
    monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS,
    async function () {
        console.log("Saving")
        await editorTabs.saveCurrentFile()
    }
);


function collectDeclaredClasses(node, classNames) {
    if (node.type === "class_definition") {
        var nameNode = node.childForFieldName("name");

        if (nameNode) {
            classNames.add(nameNode.text);
        }
    }

    for (var child of node.namedChildren) {
        collectDeclaredClasses(child, classNames);
    }
}

function collectClassReferences(node, classNames, references) {
    if (
        node.type === "identifier" &&
        classNames.has(node.text)
    ) {
        references.push({
            start: node.startPosition,
            end: node.endPosition
        });
    }

    for (var child of node.namedChildren) {
        collectClassReferences(child, classNames, references);
    }
}


var treeSitterParser;
var treeSitterQuery;
var treeSitterDecorations = [];
var treeSitterReady = false;
var highlightingInProgress = false;

var captureColors = {
    keyword: "hs-keyword",
    variable: "hs-variable",
    function: "hs-function",
    constructor: "hs-constructor",
    operator: "hs-operator"
};

async function initializeTreeSitter() {
    await Parser.init();

    var wasmResponse = await fetch(pythonWasmUrl);
    var wasmBytes = new Uint8Array(await wasmResponse.arrayBuffer());

    var pythonLanguage = await Language.load(wasmBytes);

    treeSitterParser = new Parser();
    treeSitterParser.setLanguage(pythonLanguage);

    treeSitterQuery = new Query(pythonLanguage, highlightsQuery);
    treeSitterReady = true;

    highlightPython();
}

function highlightPython() {
    if (!treeSitterReady || highlightingInProgress) {
        return;
    }

    var model = monacoEditor.getModel();

    if (!model || model.getLanguageId() !== "python") {
        return;
    }

    highlightingInProgress = true;

    try {
        var source = model.getValue();
        var tree = treeSitterParser.parse(source);
        var captures = treeSitterQuery.captures(tree.rootNode);

        var declaredClasses = new Set();
        collectDeclaredClasses(tree.rootNode, declaredClasses);

        var classReferences = [];
        collectClassReferences(
            tree.rootNode,
            declaredClasses,
            classReferences
        );

        function collectClassNames(node, names) {
            if (node.type === "class_definition") {
                var nameNode = node.childForFieldName("name");

                if (nameNode) {
                    names.push({
                        start: nameNode.startPosition,
                        end: nameNode.endPosition
                    });
                }
            }

            for (var child of node.namedChildren) {
                collectClassNames(child, names);
            }
        }

        var classNames = [];
        collectClassNames(tree.rootNode, classNames);

        var selected = new Map();

        var priorities = {
            variable: 1,
            keyword: 2,
            operator: 3,
            function: 4,
            constructor: 5
        };

        for (var capture of captures) {
            var className = captureColors[capture.name];

            if (!className) {
                continue;
            }

            var start = capture.node.startPosition;
            var end = capture.node.endPosition;

            var key = start.row + ":" + start.column + ":" +
                end.row + ":" + end.column;

            var previous = selected.get(key);

            if (
                !previous ||
                priorities[capture.name] > priorities[previous.name]
            ) {
                selected.set(key, {
                    name: capture.name,
                    start: start,
                    end: end
                });
            }
        }

        var decorations = [];

        for (var item of selected.values()) {
            decorations.push({
                range: new monaco.Range(
                    item.start.row + 1,
                    item.start.column + 1,
                    item.end.row + 1,
                    item.end.column + 1
                ),
                options: {
                    inlineClassName: captureColors[item.name]
                }
            });
        }


        for (var className of classNames) {
            decorations.push({
                range: new monaco.Range(
                    className.start.row + 1,
                    className.start.column + 1,
                    className.end.row + 1,
                    className.end.column + 1
                ),
                options: {
                    inlineClassName: "hs-constructor"
                }
            });
        }

        for (var reference of classReferences) {
            decorations.push({
                range: new monaco.Range(
                    reference.start.row + 1,
                    reference.start.column + 1,
                    reference.end.row + 1,
                    reference.end.column + 1
                ),
                options: {
                    inlineClassName: "hs-constructor"
                }
            });
        }


        treeSitterDecorations = monacoEditor.deltaDecorations(
            treeSitterDecorations,
            decorations
        );

        tree.delete();
    } catch (error) {
        console.error("Tree-sitter highlighting error:", error);
    } finally {
        highlightingInProgress = false;
    }
}

monacoEditor.onDidChangeModelContent(function () {
    highlightPython();
    editorTabs.fileContents[editorTabs.active] = monacoEditor.getValue();
});

initializeTreeSitter().catch(function (error) {
    console.error("Failed to initialize Tree-sitter:", error);
});

connectPyright(monaco, monacoEditor);

export async function openFile(filepath) {
    const content = await window.hobbySpark.readFile(filepath);
    monacoEditor.setValue(content)
}
export async function clearEditor() {
    monacoEditor.setValue("# No file currently open")
}
export async function saveFile(filepath) {
    const content = monacoEditor.getValue()
    return await window.hobbySpark.writeFile(filepath, content)
}

export function writeData(data) {
    monacoEditor.setValue(data)
}
