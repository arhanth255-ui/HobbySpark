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
    }
});
