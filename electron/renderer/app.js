const editorTabs = new EditorTabs("#editor-tabs");

editorTabs.add("main.hsp");
editorTabs.add("boards.json");
editorTabs.add("README.md");
class Tree {
    constructor(element) {
        if (typeof element === "string") {
            element = document.querySelector(element);
        }

        if (!element) {
            throw new Error("Tree element was not found");
        }

        this.element = element;

        this.element.addEventListener("click", (event) => {
            this.handleClick(event);
        });
    }

    handleClick(event) {
        const label = event.target.closest(".tree-folder-label");

        const file = event.target.closest(".tree-file")

        if (file && this.element.contains(file)) {
            // Do something with the clicked file
            console.log("File clicked:", file.dataset.name);

            this.openFile(file.dataset.name)

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

    openFile(name){
        editorTabs.add(name)
    }


addFolder(name, parentName = null) {
    // Find the parent folder, or use the tree root.
    let parent = this.element;

    if (parentName !== null) {
        const folders = this.element.querySelectorAll(".tree-folder");

        parent = [...folders].find(
            folder => folder.dataset.name === parentName
        );

        if (!parent) {
            throw new Error(`Parent folder "${parentName}" not found`);
        }

        // Add the new folder inside the parent's children.
        let children = parent.querySelector(":scope > .tree-children");

        if (!children) {
            children = document.createElement("div");
            children.className = "tree-children";
            parent.appendChild(children);
        }

        parent = children;
    }

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

    const children = document.createElement("div");
    children.className = "tree-children";

    folder.append(label, children);
    parent.appendChild(folder);
}

addFile(name, parentName = null) {
    let parent = this.element;

    if (parentName !== null) {
        const folders = this.element.querySelectorAll(".tree-folder");

        const folder = [...folders].find(
            folder => folder.dataset.name === parentName
        );

        if (!folder) {
            throw new Error(`Parent folder "${parentName}" not found`);
        }

        let children = folder.querySelector(":scope > .tree-children");

        if (!children) {
            children = document.createElement("div");
            children.className = "tree-children";
            folder.appendChild(children);
        }

        parent = children;
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


}

const projectTree = new Tree("#project-tree");
projectTree.addFolder(".src")
projectTree.addFile("arc.py", ".src")


const folders = document.querySelectorAll(".tree-item.folder");

