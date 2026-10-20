
let socket;
let requestId = 0;
let pendingRequests = {};
let documentVersion = 1;
let connected = false;
let activeModel;
let monacoApi;

function sendMessage(message) {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify(message));
    }
}

function request(method, params) {
    return new Promise(function (resolve, reject) {
        const id = ++requestId;

        pendingRequests[id] = {
            resolve: resolve,
            reject: reject
        };

        sendMessage({
            jsonrpc: "2.0",
            id: id,
            method: method,
            params: params
        });
    });
}

function notify(method, params) {
    sendMessage({
        jsonrpc: "2.0",
        method: method,
        params: params
    });
}

function getPosition(position) {
    return {
        line: position.lineNumber - 1,
        character: position.column - 1
    };
}

function getRange(range) {
    return new monacoApi.Range(
        range.start.line + 1,
        range.start.character + 1,
        range.end.line + 1,
        range.end.character + 1
    );
}

function handleMessage(message) {
    if (message.id !== undefined && pendingRequests[message.id]) {
        const pending = pendingRequests[message.id];
        delete pendingRequests[message.id];

        if (message.error) {
            pending.reject(message.error);
        } else {
            pending.resolve(message.result);
        }

        return;
    }

    if (message.method === "textDocument/publishDiagnostics") {
        const diagnostics = message.params.diagnostics.map(
            function (diagnostic) {
                return {
                    severity: diagnostic.severity === 1
                        ? monacoApi.MarkerSeverity.Error
                        : diagnostic.severity === 2
                            ? monacoApi.MarkerSeverity.Warning
                            : diagnostic.severity === 3
                                ? monacoApi.MarkerSeverity.Info
                                : monacoApi.MarkerSeverity.Hint,
                    message: diagnostic.message,
                    startLineNumber: diagnostic.range.start.line + 1,
                    startColumn: diagnostic.range.start.character + 1,
                    endLineNumber: diagnostic.range.end.line + 1,
                    endColumn: diagnostic.range.end.character + 1,
                    source: diagnostic.source || "Pyright"
                };
            }
        );

        const model = monacoApi.editor.getModels().find(
            function (candidate) {
                return candidate.uri.toString() === message.params.uri;
            }
        );

        if (model) {
            monacoApi.editor.setModelMarkers(
                model,
                "pyright",
                diagnostics
            );
        }

        return;
    }

    if (message.id !== undefined && message.method) {
        let result = null;

        if (message.method === "workspace/configuration") {
            result = (message.params.items || []).map(function () {
                return {};
            });
        } else if (message.method === "workspace/workspaceFolders") {
            result = [];
        }

        sendMessage({
            jsonrpc: "2.0",
            id: message.id,
            result: result
        });
    }
}


function synchronizeDocument(model) {
    activeModel = model;
    documentVersion = 1;

    notify("textDocument/didOpen", {
        textDocument: {
            uri: model.uri.toString(),
            languageId: "python",
            version: documentVersion,
            text: model.getValue()
        }
    });
}


function registerProviders(monaco) {
    monaco.languages.registerCompletionItemProvider("python", {
        triggerCharacters: ["."],

        provideCompletionItems: async function (model, position) {
            if (!connected || model !== activeModel) {
                return { suggestions: [] };
            }

            const result = await request("textDocument/completion", {
                textDocument: {
                    uri: model.uri.toString()
                },
                position: getPosition(position)
            });

            const items = Array.isArray(result)
                ? result
                : result && result.items
                    ? result.items
                    : [];

            return {
                suggestions: items.map(function (item) {
                    return {
                        label: item.label,
                        insertText: item.insertText || item.label,
                        detail: item.detail,
                        documentation: item.documentation,
                        sortText: item.sortText,
                        filterText: item.filterText,
                        kind: item.kind
                            ? item.kind + 0
                            : monaco.languages.CompletionItemKind.Text
                    };
                })
            };
        }
    });

    monaco.languages.registerHoverProvider("python", {
        provideHover: async function (model, position) {
            if (!connected || model !== activeModel) {
                return null;
            }

            const result = await request("textDocument/hover", {
                textDocument: {
                    uri: model.uri.toString()
                },
                position: getPosition(position)
            });

            if (!result || !result.contents) {
                return null;
            }

            let contents = result.contents;

            if (!Array.isArray(contents)) {
                contents = [contents];
            }

            return {
                contents: contents.map(function (item) {
                    if (typeof item === "string") {
                        return { value: item };
                    }

                    if (item.kind === "markdown" || item.language) {
                        return {
                            value: item.value || item.language || ""
                        };
                    }

                    return {
                        value: item.value || String(item)
                    };
                }),
                range: result.range
                    ? getRange(result.range)
                    : undefined
            };
        }
    });

    monaco.languages.registerSignatureHelpProvider("python", {
        signatureHelpTriggerCharacters: ["(", ","],
        signatureHelpRetriggerCharacters: [",", ")"],

        provideSignatureHelp: async function (
            model,
            position,
            token,
            context
        ) {
            if (!connected || model !== activeModel) {
                return null;
            }

            const result = await request(
                "textDocument/signatureHelp",
                {
                    textDocument: {
                        uri: model.uri.toString()
                    },
                    position: getPosition(position),
                    context: {
                        triggerKind: context.isRetrigger
                            ? 3
                            : context.triggerKind === 2
                                ? 2
                                : 1,
                        isRetrigger: context.isRetrigger,
                        triggerCharacter: context.triggerCharacter
                    }
                }
            );

            if (!result || !result.signatures ||
                result.signatures.length === 0) {
                return null;
            }

            return {
                value: result,
                dispose: function () {}
            };
        }
    });

}


function registerSemanticTokensProvider(monaco, legend) {
    monaco.languages.registerDocumentSemanticTokensProvider(
        "python",
        {
            getLegend: function () {
                return {
                    tokenTypes: legend.tokenTypes,
                    tokenModifiers: legend.tokenModifiers
                };
            },

            provideDocumentSemanticTokens: async function (
                model,
                lastResultId,
                token
            ) {
                if (!connected) {
                    return { data: new Uint32Array(0) };
                }

                try {
                    const result = await request(
                        "textDocument/semanticTokens/full",
                        {
                            textDocument: {
                                uri: model.uri.toString()
                            }
                        }
                    );

                    if (!result || !result.data) {
                        return { data: new Uint32Array(0) };
                    }

                    return {
                        data: new Uint32Array(result.data),
                        resultId: result.resultId
                    };
                } catch (error) {
                    console.error(
                        "Semantic token request failed:",
                        error
                    );

                    return { data: new Uint32Array(0) };
                }
            },

            releaseDocumentSemanticTokens: function () {}
        }
    );
}


export function connectPyright(monaco, editor) {
    if (socket) {
        return;
    }

    monacoApi = monaco;
    activeModel = editor.getModel();

    registerProviders(monaco);

    socket = new WebSocket("ws://127.0.0.1:3001");

    socket.addEventListener("open", async function () {
        console.log("Connected to Pyright bridge");

        socket.addEventListener("message", function (event) {
            try {
                handleMessage(JSON.parse(event.data));
            } catch (error) {
                console.error("Invalid LSP message:", error);
            }
        });

        try {
            await request("initialize", {
                processId: null,
                rootUri: null,
                capabilities: {
                    textDocument: {
                        completion: {
                            completionItem: {
                                snippetSupport: false
                            }
                        },
                        hover: {
                            contentFormat: ["markdown", "plaintext"]
                        },
                        publishDiagnostics: {
                            relatedInformation: true
                        },
                        semanticTokens: {
                            requests: {
                                range: false,
                                full: true
                            },
                            tokenTypes: [
                                "namespace", "type", "class", "enum", "interface",
                                "struct", "typeParameter", "parameter", "variable",
                                "property", "enumMember", "event", "function",
                                "method", "macro", "keyword", "modifier", "comment",
                                "string", "number", "regexp", "operator", "decorator"
                            ],
                            tokenModifiers: [
                                "declaration", "definition", "readonly", "static",
                                "deprecated", "abstract", "async", "modification",
                                "documentation", "defaultLibrary"
                            ],
                            formats: ["relative"]
                        }
                    },
                    workspace: {
                        configuration: true,
                        workspaceFolders: true
                    }
                },
                initializationOptions: {}
            });

            
            notify("initialized", {});
            connected = true;

            

            synchronizeDocument(activeModel);

            activeModel.onDidChangeContent(function () {
                if (!connected) {
                    return;
                }

                documentVersion++;

                notify("textDocument/didChange", {
                    textDocument: {
                        uri: activeModel.uri.toString(),
                        version: documentVersion
                    },
                    contentChanges: [
                        { text: activeModel.getValue() }
                    ]
                });
            });

            console.log("Pyright LSP initialized");
        } catch (error) {
            console.error("Pyright initialization failed:", error);
        }
    });

    socket.addEventListener("error", function (error) {
        console.error("Pyright WebSocket error:", error);
    });
}
