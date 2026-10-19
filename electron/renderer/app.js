import { EditorTabs } from "./tabmanager.js";
import { Tree } from "./tree.js";
var filesAndFolders;
var folderPath;
const editorTabs = new EditorTabs("#editor-tabs");
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
    return path.split(/[\\/]/).pop();
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
    await add(folderPath, projectTree.root_name);
});

console.log("Type of files", typeof filesAndFolders)







