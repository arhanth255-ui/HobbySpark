import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from nodes import *


def visualize_ast(parsed):
    window = QMainWindow()
    window.setWindowTitle("HobbySpark — AST Explorer")
    window.resize(1100, 750)

    # --------------------------------------------------
    # Main layout
    # --------------------------------------------------

    central = QWidget()
    layout = QVBoxLayout(central)

    window.setCentralWidget(central)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    # --------------------------------------------------
    # Compact search toolbar
    # --------------------------------------------------

    search_toolbar = QFrame()
    search_toolbar.setObjectName("SearchToolbar")
    search_toolbar.setFixedHeight(36)

    search_layout = QHBoxLayout(search_toolbar)
    search_layout.setContentsMargins(0, 0, 0, 0)
    search_layout.setSpacing(0)

    search_input = QLineEdit()
    search_input.setPlaceholderText("Search AST...")
    search_input.setClearButtonEnabled(True)
    search_input.setMinimumWidth(0)
    search_input.setFixedHeight(36)

    previous_button = QPushButton("↑")
    previous_button.setFixedSize(36, 36)
    previous_button.setToolTip("Previous match")

    next_button = QPushButton("↓")
    next_button.setFixedSize(36, 36)
    next_button.setToolTip("Next match")

    search_status = QLabel("0 matches")
    search_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
    search_status.setFixedWidth(80)

    search_layout.addWidget(search_input, 1)
    search_layout.addWidget(search_status)
    search_layout.addWidget(previous_button)
    search_layout.addWidget(next_button)

    layout.addWidget(search_toolbar, 0)

    # --------------------------------------------------
    # Splitter
    # --------------------------------------------------

    splitter = QSplitter(Qt.Orientation.Horizontal)

    tree = QTreeWidget()
    tree.setHeaderHidden(True)
    tree.setAlternatingRowColors(True)
    tree.setAnimated(True)
    tree.setIndentation(22)

    inspector = QPlainTextEdit()
    inspector.setReadOnly(True)
    inspector.setPlaceholderText("Select an AST node to inspect it.")

    splitter.addWidget(tree)
    splitter.addWidget(inspector)

    splitter.setSizes([600, 500])

    layout.addWidget(splitter)

    # --------------------------------------------------
    # Object storage
    # --------------------------------------------------

    objects = {}

    def safe_repr(value):
        try:
            return repr(value)
        except Exception as exc:  # noqa: BLE001
            return f"<repr failed: {exc}>"

    def get_fields(value):
        try:
            return vars(value)
        except TypeError:
            return {}

    def get_kind(value):
        if isinstance(value, Node):
            return "AST Node"

        if isinstance(value, dict):
            return "Dictionary"

        if isinstance(value, list):
            return "List"

        if isinstance(value, tuple):
            return "Tuple"

        if isinstance(value, set):
            return "Set"

        return type(value).__name__

    # --------------------------------------------------
    # AST traversal
    # --------------------------------------------------

    def add_value(parent, name, value, visited=None):
        if visited is None:
            visited = set()

        composite = isinstance(value, (Node, list, dict, tuple, set))

        label = (
            f"{name}: {type(value).__name__}"
            if composite
            else f"{name} = {safe_repr(value)}"
        )

        item = QTreeWidgetItem(parent, [label])
        objects[id(item)] = value

        if composite and id(value) in visited:
            item.setText(0, f"{label} <circular reference>")
            return item

        if not composite:
            return item

        visited.add(id(value))

        try:
            if isinstance(value, Node):
                for field, child in get_fields(value).items():
                    add_value(item, field, child, visited)

            elif isinstance(value, dict):
                for key, child in value.items():
                    add_value(item, f"[{safe_repr(key)}]", child, visited)

            else:
                for index, child in enumerate(value):
                    add_value(item, f"[{index}]", child, visited)

        finally:
            visited.remove(id(value))

        return item

    # --------------------------------------------------
    # Build tree
    # --------------------------------------------------

    root = QTreeWidgetItem(tree, [f"Program: {type(parsed).__name__}"])

    objects[id(root)] = parsed

    for field, value in get_fields(parsed).items():
        add_value(root, field, value)

    tree.expandToDepth(2)

    # --------------------------------------------------
    # Inspector
    # --------------------------------------------------

    def inspect_item():
        item = tree.currentItem()

        if item is None:
            return

        if id(item) not in objects:
            return

        value = objects[id(item)]

        lines = []

        lines.append("=" * 45)
        lines.append("OBJECT INSPECTOR")
        lines.append("=" * 45)

        lines.append(f"\nType: {type(value).__name__}")
        lines.append(f"Category: {get_kind(value)}")
        lines.append(f"ID: {id(value)}")

        lines.append("\n--- REPRESENTATION ---")
        lines.append(safe_repr(value))

        lines.append("\n--- PARENT RELATIONSHIP ---")

        parent = item.parent()

        if parent:
            parent_value = objects.get(id(parent))
            lines.append(f"Parent: {type(parent_value).__name__}")
            lines.append(f"Parent field: {parent.text(0)}")
        else:
            lines.append("Parent: None (root)")

        lines.append("\n--- CHILDREN ---")

        if item.childCount():
            for i in range(item.childCount()):
                child = item.child(i)
                child_value = objects.get(id(child))

                lines.append(f"{i}. {child.text(0)}  [{type(child_value).__name__}]")
        else:
            lines.append("No children.")

        lines.append("\n--- ATTRIBUTES ---")

        fields = get_fields(value)

        if fields:
            for name, field_value in fields.items():
                lines.append(f"{name} = {safe_repr(field_value)}")
        elif isinstance(value, dict):
            for key, val in value.items():
                lines.append(f"{safe_repr(key)} = {safe_repr(val)}")
        elif isinstance(value, (list, tuple, set)):
            for index, val in enumerate(value):
                lines.append(f"[{index}] = {safe_repr(val)}")
        else:
            lines.append("No attributes.")

        lines.append("\n--- FULL TREE PATH ---")

        path = []
        current = item

        while current is not None:
            path.append(current.text(0))
            current = current.parent()

        for part in reversed(path):
            lines.append("  " + part)

        inspector.setPlainText("\n".join(lines))

    tree.itemSelectionChanged.connect(inspect_item)

    # --------------------------------------------------
    # Search
    # --------------------------------------------------

    matches = []
    match_index = -1

    def collect_matches(item, query):
        if query in item.text(0).casefold():
            matches.append(item)

        for i in range(item.childCount()):
            collect_matches(item.child(i), query)

    def update_search():
        nonlocal match_index

        matches.clear()
        match_index = -1

        query = search_input.text().strip().casefold()

        if not query:
            search_status.setText("0 matches")
            return

        collect_matches(tree.invisibleRootItem(), query)

        search_status.setText(f"{len(matches)} matches")

        if matches:
            match_index = 0
            select_match()

    def select_match():
        if not matches:
            return

        item = matches[match_index]

        # Expand ancestors so the selected result is visible.
        parent = item.parent()

        while parent is not None:
            parent.setExpanded(True)
            parent = parent.parent()

        tree.setCurrentItem(item)
        tree.scrollToItem(item)

    def next_match():
        nonlocal match_index

        if matches:
            match_index = (match_index + 1) % len(matches)
            select_match()

    def previous_match():
        nonlocal match_index
        if matches:
            match_index = (match_index - 1) % len(matches)
            select_match()

    search_input.textChanged.connect(update_search)
    search_input.returnPressed.connect(next_match)

    next_button.clicked.connect(next_match)
    previous_button.clicked.connect(previous_match)

    # --------------------------------------------------
    # Display
    # --------------------------------------------------

    tree.setCurrentItem(root)

    window.show()

    return window


# ------------------------------------------------------
# Standalone test
# ------------------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)

    parsed = ProgramNode(
        ForLoopNode(
            ListNode([NumberNode("1"), NumberNode("2")]),
            [
                CallNode(
                    VariableNameNode("asd"), ["a", "b", "c"], {"abd": "asd", "as": "as"}
                )
            ],
            VariableNameNode("asd"),
        )
    )

    window = visualize_ast(parsed)

    sys.exit(app.exec())
