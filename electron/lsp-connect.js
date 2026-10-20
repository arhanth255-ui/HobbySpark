
const WebSocket = require("ws");
const {
    createServerProcess,
    createWebSocketConnection,
    forward
} = require("vscode-ws-jsonrpc/server");

let websocketServer;

function startLanguageServer() {
    websocketServer = new WebSocket.Server({
        host: "127.0.0.1",
        port: 3001
    });

    websocketServer.on("connection", function (socket) {
        console.log("Monaco connected to the LSP bridge");

        socket.dispose = function () {
            socket.close();
        };

        const clientConnection = createWebSocketConnection(socket);
        
        const serverConnection = createServerProcess(
            "Pyright",
            "pyright-langserver",
            ["--stdio"]
        );

        if (!serverConnection) {
            console.error("Failed to start Pyright");
            socket.close();
            return;
        }

        forward(clientConnection, serverConnection);

        socket.on("close", function () {
            serverConnection.dispose();
        });
    });

    websocketServer.on("listening", function () {
        console.log("Pyright bridge listening on 127.0.0.1:3001");
    });

    websocketServer.on("error", function (error) {
        console.error("LSP bridge error:", error);
    });
}

function stopLanguageServer() {
    if (websocketServer) {
        websocketServer.close();
        websocketServer = null;
    }
}

module.exports = {
    startLanguageServer: startLanguageServer,
    stopLanguageServer: stopLanguageServer
};
