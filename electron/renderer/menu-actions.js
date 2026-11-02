import { startup, projectTree } from "./app";

export async function onClickOfOpenFolder(event) {
    projectTree.clear()
    await startup();
    console.log("Switched")
}