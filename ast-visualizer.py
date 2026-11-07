import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTreeWidget,
    QTreeWidgetItem,
)

from nodes import *


def visualize_ast(parsed):
    print("[1] Creating window")

    window = QMainWindow()
    window.setWindowTitle("HobbySpark AST Visualizer")
    window.resize(900, 650)

    tree = QTreeWidget()
    tree.setHeaderHidden(True)
    window.setCentralWidget(tree)

    print("[2] Building AST")

    def add_node(parent, name, value):
        if isinstance(value, Node):
            item = QTreeWidgetItem(
                parent, [f"{name}: {type(value).__name__}"]
            )

            for field, child in vars(value).items():
                add_node(item, field, child)

        elif isinstance(value, dict):
            item = QTreeWidgetItem(parent, [f"{name}: dict"])

            for key, child in value.items():
                add_node(item, repr(key), child)

        elif isinstance(value, (list, tuple, set)):
            item = QTreeWidgetItem(
                parent, [f"{name}: {type(value).__name__}"]
            )

            for i, child in enumerate(value):
                add_node(item, f"[{i}]", child)

        else:
            QTreeWidgetItem(parent, [f"{name} = {value!r}"])

    root = QTreeWidgetItem(tree, [type(parsed).__name__])

    for field, value in vars(parsed).items():
        add_node(root, field, value)

    tree.expandAll()

    print("[3] Showing window")
    window.show()

    return window


if __name__ == "__main__":
    app = QApplication(sys.argv)

    parsed = ProgramNode(
        ForLoopNode(
            ListNode([
                NumberNode("1"),
                NumberNode("2")
            ]),
            [
                CallNode(
                    VariableNameNode("asd"),
                    ["a", "b", "c"],
                    {"abd": "asd", "as": "as"}
                )
            ],
            VariableNameNode("asd")
        )
    )

    window = visualize_ast(parsed)

    print("[4] Entering Qt event loop")
    sys.exit(app.exec())