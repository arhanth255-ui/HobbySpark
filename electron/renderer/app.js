import { EditorTabs } from "./tabmanager.js";
import { Tree } from "./tree.js";
var filesAndFolders;
var folderPath;
export const editorTabs = new EditorTabs("#editor-tabs");
let projectTree;



async function startApp() {
    folderPath = await window.hobbySpark.openProjectFolder();

    if (folderPath === null) {
        console.log("No project folder selected.");
        return;
    }

    console.log("Selected project:", folderPath);
    
    filesAndFolders = await window.hobbySpark.listFilesAndFolders(folderPath);
    console.log("Received:", filesAndFolders);
    console.log("Type:", typeof filesAndFolders);
    console.log("Is array:", Array.isArray(filesAndFolders));
}
function getPathName(path) {
    if (typeof path !== "string" || path.length === 0) {
        return "";
    }

    return path.split("/").pop();
}

async function add(folderPath, root = null) {
    var items = await window.hobbySpark.listFilesAndFolders(folderPath);
    items.sort(function (a, b){
        if (a.isDirectory && !b.isDirectory){return -1}
        if (!a.isDirectory && b.isDirectory){return 1}
        return a.name.localeCompare(b.name)
    });

    for (var item of items) {
        if (!item.isDirectory) {
            projectTree.addFile(item.name, item.path, root);
        } else {
            projectTree.addFolder(item.name, root);
            await add(item.path, item.name);
        }
    }
    
}



document.addEventListener("DOMContentLoaded", async function () {
    await startApp();
    projectTree = new Tree("#project-tree", editorTabs, getPathName(folderPath));
    console.log(folderPath)
    if (folderPath!==null){window.hobbySpark.writeTerminal("cd \""+folderPath+"\"\n")}
    await add(folderPath, projectTree.root_name);
    projectTree.closeAllFolders()
});



console.log("Type of files", typeof filesAndFolders)
var portSelector = document.getElementById("port-selector");

async function loadPorts() {
    var result = await window.hobbySpark.getPorts();

    portSelector.innerHTML = "";

    for (const item of result.detected_ports ?? []) {
        var address = item.port.address;
        var option = document.createElement("option");

        option.value = address;
        option.textContent = address;

        portSelector.appendChild(option);
    }
}
loadPorts()










