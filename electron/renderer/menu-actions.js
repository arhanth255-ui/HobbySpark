import { startup, projectTree, editorTabs } from "./app";

export async function onClickOfOpenFolder(event) {
    projectTree.clear()
    await startup();
    console.log("Switched")
}

export async function onClickOfNewFile(event) {
    editorTabs.add("Untitled", "Unknown")
}