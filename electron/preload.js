const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("hobbySpark", {
    openProjectFolder: function () {
        return ipcRenderer.invoke("project:open-folder");
    },
    listFilesAndFolders: function (f) {
        return ipcRenderer.invoke("project:read-folder", f)
    },
    readFile: function (filePath) {
        return ipcRenderer.invoke("file:read", filePath);
    },

    writeFile: function (filePath, contents) {
        return ipcRenderer.invoke("file:write", filePath, contents);
    },

    startTerminal: function () {
        ipcRenderer.send("terminal:start");
    },

    writeTerminal: function (data, root = false) {
        ipcRenderer.send("terminal:write", data, root);
    },

    resizeTerminal: function (size) {
        ipcRenderer.send("terminal:resize", size);
    },

    onTerminalData: function (callback) {
        function listener(event, data) {
            callback(data);
        }

        ipcRenderer.on("terminal:data", listener);

        return function () {
            ipcRenderer.removeListener("terminal:data", listener);
        };
    },

    onTerminalExit: function (callback) {
        function listener(event, code) {
            callback(code);
        }

        ipcRenderer.on("terminal:exit", listener);

        return function () {
            ipcRenderer.removeListener("terminal:exit", listener);
        };
    },
    // onHobbySparkCommand: function (callback) {
    // return ipcRenderer.invoke("project:change-callback")
    // },
    // runHobbySparkCommand: function (input) {
    //     return ipcRenderer.invoke("project:run-command-hobbyspark")
    // },
    getPorts: function () {
        return ipcRenderer.invoke("project:get-com-ports")
    },

    assignHobbySparkCommand: function (func) {
        console.log("PRELOAD: Registering listener");

        ipcRenderer.on("the-end", function (event, exitCode) {
            console.log("PRELOAD: Received:", exitCode);
            func(exitCode);
        });
    },
    newFile: (startPath) => ipcRenderer.invoke("menu:new-file", startPath),

    onNewFileWarning: (callback) => {
        ipcRenderer.on("menu:new-file-warning", (event, message) => {
            callback(message);
        });
    }

});
