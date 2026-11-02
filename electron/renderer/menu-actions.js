import { startup } from "./app";

export async function onClickOfOpenFolder(event){
    await startup();
    console.log("Switched")
}