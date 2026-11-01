console.log("tree.js loaded!");
export class Tree {
    constructor(element, editorTabs, root_name = "UnSelected") {
        if (typeof element === "string") {
            element = document.querySelector(element);
        }

        if (!element) {
            throw new Error("Tree element was not found");
        }

        this.element = element;

        this.element.addEventListener("click", async (event) => {
            await this.handleClick(event);
        });
        this.root_name = root_name;
        this.addFolder(root_name, null, true)
        this.editorTabs = editorTabs;
        this.tabsAndPaths = {};

    }

    async handleClick(event) {
        const label = event.target.closest(".tree-folder-label");

        const file = event.target.closest(".tree-file")

        if (file && this.element.contains(file)) {
            // Do something with the clicked file
            console.log("File clicked:", file.dataset.name);

            await this.openFile(file.dataset.name)

            return;
        }

        if (!label || !this.element.contains(label)) {
            return;
        }

        const folder = label.parentElement;
        const contents = folder.querySelector(":scope > .tree-children");

        if (!contents) {
            return;
        }

        const isExpanded = label.getAttribute("aria-expanded") === "true";
        const shouldExpand = !isExpanded;

        label.setAttribute("aria-expanded", String(shouldExpand));
        contents.hidden = !shouldExpand;

        const chevron = label.querySelector(".tree-chevron");
        chevron.textContent = shouldExpand ? "▾" : "▸";
    }

    async openFile(name) {
        await this.editorTabs.add(name, this.tabsAndPaths[name])
    }

    addFolder(name, parentName = null, special = false) {
        // Create the tree's root folder.
        if (special) {
            let folder = document.createElement("div");
            folder.className = "tree-folder";
            folder.dataset.name = name;

            let label = document.createElement("button");
            label.className = "tree-folder-label";
            label.type = "button";
            label.setAttribute("aria-expanded", "true");

            let chevron = document.createElement("span");
            chevron.className = "tree-chevron";
            chevron.textContent = "▾";

            let title = document.createElement("span");
            title.textContent = "📂 " + name;

            label.append(chevron, title);

            let rootChildren = document.createElement("div");
            rootChildren.className = "tree-children";

            folder.append(label, rootChildren);
            this.element.appendChild(folder);
            return;
        }

        // Find the parent folder.
        if (parentName === null) {
            parentName = this.root_name;
        }

        const folders = this.element.querySelectorAll(".tree-folder");

        let rootParent = Array.from(folders).find(
            function (folder) {
                return folder.dataset.name === parentName;
            }
        );

        if (!rootParent) {
            throw new Error(`Parent folder "${parentName}" not found`);
        }

        // Find or create the parent's children container.
        let children = rootParent.querySelector(":scope > .tree-children");

        if (!children) {
            children = document.createElement("div");
            children.className = "tree-children";
            rootParent.appendChild(children);
        }

        // Create the new folder.
        const folder = document.createElement("div");
        folder.className = "tree-folder";
        folder.dataset.name = name;

        const label = document.createElement("button");
        label.className = "tree-folder-label";
        label.type = "button";
        label.setAttribute("aria-expanded", "true");

        const chevron = document.createElement("span");
        chevron.className = "tree-chevron";
        chevron.textContent = "▾";

        const title = document.createElement("span");
        title.textContent = `📂 ${name}`;

        label.append(chevron, title);

        const folderChildren = document.createElement("div");
        folderChildren.className = "tree-children";

        folder.append(label, folderChildren);
        children.appendChild(folder);
    }


    addFile(name, path, parentName = null) {
        this.tabsAndPaths[name] = path;
        if (parentName === null) {
            parentName = this.root_name;
        }

        const folders = this.element.querySelectorAll(".tree-folder");

        const folder = Array.from(folders).find(
            function (folder) {
                return folder.dataset.name === parentName;
            }
        );

        if (!folder) {
            throw new Error(`Parent folder "${parentName}" not found`);
        }

        const parent = folder.querySelector(":scope > .tree-children");

        if (!parent) {
            throw new Error(`Children container for "${parentName}" not found`);
        }

        const file = document.createElement("div");
        file.className = "tree-file";
        file.dataset.name = name;

        const icon = document.createElement("span");
        icon.textContent = this.getFileIcon(name);

        const label = document.createElement("span");
        label.textContent = name;

        file.append(icon, label);
        parent.appendChild(file);
    }


    getFileIcon(name) {
        if (name.endsWith(".hsp") || name.endsWith(".py")) return "🐍";
        if (name.endsWith(".json")) return "📋";
        if (name.endsWith(".md")) return "📄";
        if (name.endsWith(".cpp") || name.endsWith(".h")) return "⚙️";
        return "📄";
    }

    closeAllFolders() {
        const root = Array.from(
            this.element.querySelectorAll(".tree-folder")
        ).find(folder => folder.dataset.name === this.root_name);

        if (!root) return;

        const folders = root.querySelectorAll(".tree-folder");

        folders.forEach((folder) => {
            const label = folder.querySelector(":scope > .tree-folder-label");
            const children = folder.querySelector(":scope > .tree-children");

            if (!label || !children) return;

            label.setAttribute("aria-expanded", "false");
            children.hidden = true;

            const chevron = label.querySelector(".tree-chevron");


            if (chevron !== null) {
                chevron.textContent = "▸";
            }
        });

        // Keep the root expanded
        const rootLabel = root.querySelector(":scope > .tree-folder-label");
        const rootChildren = root.querySelector(":scope > .tree-children");

        console.log(rootChildren)

        if (rootLabel) rootLabel.setAttribute("aria-expanded", "true");
        rootChildren.hidden = false;

        if (rootLabel) {
            console.log(rootLabel)
            rootLabel.querySelector(".tree-chevron").textContent = "▾";
        }
    }


}