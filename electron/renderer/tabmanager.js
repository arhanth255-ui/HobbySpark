
import { clearEditor, saveFile, writeData } from "./editor.js";

export class EditorTabs {
    constructor(element) {
        this.element = typeof element === "string"
            ? document.querySelector(element)
            : element;

        if (!this.element) {
            throw new Error("Editor tabs element not found");
        }

        this.openFiles = [];
        this.openFilesAndPaths = {};
        this.active = null;
        this.historyOfActive = [];
        this.fileContents = {};
        this.savedContents = {};
    }

    async add(name, path) {
        if (!name || !path) {
            throw new Error("A valid filename and path are required");
        }

        // If already open, switch to its existing tab.
        if (this.openFiles.includes(name)) {
            this.active = name;
            writeData(this.fileContents[name]);
            return;
        }

        // Load the file into memory only once.
        const content = await window.hobbySpark.readFile(path);

        this.fileContents[name] = content;
        this.savedContents[name] = content;
        this.openFilesAndPaths[name] = path;

        const tab = document.createElement("button");
        tab.className = "editor-tab";
        tab.type = "button";

        tab.addEventListener("click", async (event) => {
            await this.onClick(event);
        });

        const title = document.createElement("span");
        title.className = "tab-name";
        title.textContent = name;

        const close = document.createElement("span");
        close.className = "tab-close";
        close.textContent = "×";

        close.addEventListener("click", async (event) => {
            event.stopPropagation();
            await this.close(event);
        });

        tab.append(title, close);
        this.element.appendChild(tab);

        this.openFiles.push(name);
        this.active = name;

        this.historyOfActive = this.historyOfActive.filter(
            fileName => fileName !== name
        );
        this.historyOfActive.push(name);

        writeData(this.fileContents[name]);

        return tab;
    }

    async onClick(event) {
        const tab = event.target.closest(".editor-tab");

        if (!tab || !this.element.contains(tab)) {
            return;
        }

        const name = tab.querySelector(".tab-name").textContent;

        if (!this.openFiles.includes(name)) {
            return;
        }

        this.active = name;

        this.historyOfActive = this.historyOfActive.filter(
            fileName => fileName !== name
        );
        this.historyOfActive.push(name);

        writeData(this.fileContents[name]);
    }

    async close(event) {
        const tab = event.target.closest(".editor-tab");
        if (!tab) return;

        const name = tab.querySelector(".tab-name").textContent;

        const index = this.openFiles.indexOf(name);

        if (index !== -1) {
            this.openFiles.splice(index, 1);
        }

        delete this.openFilesAndPaths[name];
        delete this.fileContents[name];
        delete this.savedContents[name];

        this.historyOfActive = this.historyOfActive.filter(
            fileName => fileName !== name
        );

        const wasActive = this.active === name;

        tab.remove();

        if (wasActive) {
            const next = this.historyOfActive[
                this.historyOfActive.length - 1
            ];

            if (next) {
                this.active = next;
                writeData(this.fileContents[next]);
            } else {
                this.active = null;
                await clearEditor();
            }
        }
    }

    async saveCurrentFile() {
        if (!this.active) return null;

        const path = this.openFilesAndPaths[this.active];
        const content = this.fileContents[this.active];

        await saveFile(path, content);

        this.savedContents[this.active] = content;

        return path;
    }

    updateCurrentContent(content) {
        if (!this.active) return;

        this.fileContents[this.active] = content;
    }

    hasUnsavedChanges(name) {
        return this.fileContents[name] !== this.savedContents[name];
    }
}
