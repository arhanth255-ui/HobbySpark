import { notifyWarning } from "./toasts";
window.hobbySpark.onNewFileWarning(notifyWarning)

export const recent = await window.hobbySpark.getRecent()
console.log(recent)

export function writeData(extra, data) {
    window.hobbySpark.writeJSONToConfigFile(extra, data)
}

export async function readFile(extra) {
    console.log("Path run.js", extra)
    const output = await window.hobbySpark.getJSObjectFromConfigFile(extra);
    console.log("Output is from app, ", output)
    return output;
}

export function debugPrint(message) {
    window.hobbySpark.debugPrint(message)
}