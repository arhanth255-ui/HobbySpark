const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("hobbySpark", {
    openProjectFolder: function () {
        return ipcRenderer.invoke("project:open-folder");
    },
    listFilesAndFolders: function (f) {
        return ipcRenderer.invoke("project:read-folder", f)
    }
});
