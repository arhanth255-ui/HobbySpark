import sys

from PySide6.QtCore import Qt

# from PySide6.QtGui import QAction
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

AST_NODES = {
    "BiNopNode": {
        "sm": "Represents a binary operation between two operands.",
        "lo": """A binary operation node represents an expression involving
two operands and an operator.

The node stores a left operand, an operator, and a right operand.
The transpiler visits both operands and combines their generated
representations using the corresponding operator.

Examples:
    5 + 3
    x * y
    a == b
    temperature >= 30

The operator may represent arithmetic, comparison, or logical
operations, depending on the operator tokens supported by the lexer.""",
        "params": {
            "a": "The left operand of the binary operation.",
            "op": "The operator connecting the two operands.",
            "b": "The right operand of the binary operation.",
        },
    },
    "UnaryOpNode": {
        "sm": "Represents an operation involving a single operand.",
        "lo": """A unary operation node represents an operation that acts
on one operand instead of two.

The transpiler generates the operator followed by the translated
operand.

Examples:
    -x
    +number
    not condition""",
        "params": {
            "op": "The unary operator being applied.",
            "a": "The operand on which the operation is performed.",
        },
    },
    "NumberNode": {
        "sm": "Represents a numeric literal.",
        "lo": """A number node represents a numeric value directly written
in the source code.

It may represent an integer or a floating-point number.
The transpiler converts the stored value into its output
representation.

Examples:
    10
    3.14
    0
    -5""",
        "params": {"value": "The numeric value represented by the node."},
    },
    "StringNode": {
        "sm": "Represents a string literal.",
        "lo": """A string node represents text written as a string literal
in the source program.

The transpiler converts the stored text into a C++ string
representation by surrounding it with quotation marks.

Example:
    \"Hello, HobbySpark!\"""",
        "params": {"value": "The text contained inside the string literal."},
    },
    "BoolNode": {
        "sm": "Represents a Boolean literal.",
        "lo": """A Boolean node represents one of the two logical values:
TRUE or FALSE.

The transpiler converts these values into their corresponding
C++ Boolean literals:

    TRUE  -> true
    FALSE -> false

Boolean nodes are commonly used in conditions and logical
expressions.""",
        "params": {"value": "The Boolean value represented by the node."},
    },
    "VariableNameNode": {
        "sm": "Represents the name of a variable or identifier.",
        "lo": """A variable name node represents a reference to a named
identifier in the source program.

It does not itself declare or assign a variable. Instead, it
identifies an existing or expected name that may be used in
expressions, assignments, function calls, and other constructs.

Example:
    temperature
    counter
    motor_speed""",
        "params": {"name": "The name of the identifier."},
    },
    "VariableAssignNode": {
        "sm": "Represents the assignment of a value to a variable.",
        "lo": """A variable assignment node represents assigning an
expression or value to a target.

The transpiler examines the left-hand side, right-hand side,
and type information to generate the corresponding C++ code.

It also tracks variable declarations and types during
transpilation.

Examples:
    x = 10
    name = \"HobbySpark\"
    result = a + b""",
        "params": {
            "left": "The assignment target, usually a variable or attribute.",
            "right": "The expression or value being assigned.",
            "type": "The type information associated with the assignment.",
        },
    },
    "ListNode": {
        "sm": "Represents a list containing multiple elements.",
        "lo": """A list node represents a collection of elements enclosed
in square brackets in the source language.

Each element is represented by another AST node and is
translated individually by the transpiler.

The transpiler generates a collection initializer and uses
the element types when determining the corresponding C++
container type.

Example:
    numbers = [1, 2, 3]
    names = [\"Alice\", \"Bob\"]""",
        "params": {
            "items": "A collection of AST nodes representing the list elements."
        },
    },
    "TupleNode": {
        "sm": "Represents a tuple containing multiple elements.",
        "lo": """A tuple node represents an ordered collection of elements.

Its elements are stored as AST nodes and translated individually.
The transpiler uses tuple type information to generate an
appropriate C++ tuple representation.

Example:
    coordinates = (10, 20)
    data = (\"sensor\", 25, True)

The transpiler currently rejects empty tuples without
additional type information.""",
        "params": {
            "items": "A collection of AST nodes representing the tuple elements."
        },
    },
    "IfConditionNode": {
        "sm": "Represents an if statement with optional elif and else branches.",
        "lo": """An if condition node represents conditional execution.

It contains a condition that is evaluated to determine whether
its associated body should execute.

The node can also contain multiple elif branches and an
optional else branch.

The transpiler generates an if statement followed by the
corresponding else-if and else blocks.

Example:
    if temperature > 30:
        print(\"Hot\")
    elif temperature < 10:
        print(\"Cold\")
    else:
        print(\"Normal\")""",
        "params": {
            "condition": "The condition evaluated by the if statement.",
            "body": "The AST nodes executed when the condition is true.",
            "elifs": "A collection of ElifConditionNode branches.",
            "else_": "An optional ElseNode representing the final alternative branch.",
        },
    },
    "ElifConditionNode": {
        "sm": "Represents an else-if conditional branch.",
        "lo": """An elif condition node represents an additional conditional
branch attached to an if statement.

Its condition is evaluated when the preceding if or elif
conditions have not been satisfied.

The transpiler generates an else-if block containing the
translated body.

Example:
    elif temperature < 10:
        print(\"Cold\")""",
        "params": {
            "condition": "The condition evaluated by this branch.",
            "body": "The AST nodes executed when the condition is true.",
        },
    },
    "WhileLoopNode": {
        "sm": "Represents a while loop.",
        "lo": """A while loop node represents repeated execution of a body
while a specified condition remains true.

The transpiler translates the condition and generates a
corresponding C++ while loop.

The body contains the AST nodes executed during each
iteration.

Example:
    while counter < 10:
        counter = counter + 1""",
        "params": {
            "condition": "The condition evaluated before each iteration.",
            "body": "The AST nodes executed during each iteration.",
        },
    },
    "ForLoopNode": {
        "sm": "Represents a for loop over an iterable or range.",
        "lo": """A for loop node represents iteration using a loop variable
and an iterable expression.

The transpiler supports specific iterable forms in the
inspected implementation, including range calls, list literals,
and variables previously associated with supported lists
or range expressions.

It generates either a traditional indexed-style loop or
a C++ range-based loop.

Examples:
    for i in range(10):
        print(i)

    for item in numbers:
        print(item)""",
        "params": {
            "var": "The name of the loop variable.",
            "iterable": "The expression or collection being iterated over.",
            "body": "The AST nodes executed during each iteration.",
        },
    },
    "ElseNode": {
        "sm": "Represents an else block.",
        "lo": """An else node represents the alternative branch of a
conditional statement.

Its body is executed when the preceding if and elif
conditions are not satisfied.

The transpiler generates an else block containing
the translated body.

Example:
    else:
        print(\"No condition matched\")""",
        "params": {"body": "The AST nodes executed inside the else block."},
    },
    "FunctionDefineNode": {
        "sm": "Represents a function definition.",
        "lo": """A function definition node represents the declaration
of a function.

It contains the function name, its arguments, its body,
and optional return type information.

The transpiler generates a corresponding C++ function.
When the function is defined inside a class, it is handled
as a class method instead.

Example:
    def add(a: int, b: int) -> int:
        return a + b""",
        "params": {
            "name": "The name of the function.",
            "args": "A collection of ArgNode objects describing its arguments.",
            "body": "The AST nodes forming the function body.",
            "return_type": "The declared return type, if provided.",
        },
    },
    "ArgNode": {
        "sm": "Represents a function or method argument.",
        "lo": """An argument node represents a parameter in a function
or method definition.

It stores the parameter name, its type information,
and an optional default value.

The transpiler uses this information to generate the
corresponding C++ function parameter.

Example:
    def greet(name: str, count: int = 1):
        pass""",
        "params": {
            "name": "The name of the argument.",
            "type_": "The declared type of the argument.",
            "default": "An optional AST node representing the default value.",
        },
    },
    "ReturnNode": {
        "sm": "Represents a return statement.",
        "lo": """A return node represents the termination of a function
execution by returning a value.

The transpiler translates the return expression and
generates a corresponding C++ return statement.

Example:
    return result

    return a + b""",
        "params": {"value": "The AST node representing the value being returned."},
    },
    "CallNode": {
        "sm": "Represents a function or constructor call.",
        "lo": """A call node represents invoking a named callable with
positional and keyword arguments.

The transpiler translates the callable name and its
arguments, then generates the corresponding call expression.

It also handles special cases such as set_board calls
and calls to supported HobbySpark hardware classes.

Examples:
    print(\"Hello\")
    digitalWrite(13, HIGH)
    Motor(speed=100)""",
        "params": {
            "name": "The AST node identifying the callable.",
            "args": "A collection of positional argument AST nodes.",
            "kwargs": "A mapping of keyword argument names to AST nodes.",
        },
    },
    "MethodCallNode": {
        "sm": "Represents calling a method on an object.",
        "lo": """A method call node represents invoking a method associated
with an object or instance.

It stores the object being accessed, the method name,
and its positional and keyword arguments.

The transpiler generates a method call using the object's
translated representation.

It also handles special hardware-related update behaviour
for certain supported objects.

Examples:
    motor.start()
    sensor.read()
    display.print(\"Hello\")""",
        "params": {
            "obj": "The AST node representing the object on which the method is called.",
            "name": "The name of the method being called.",
            "args": "A collection of positional argument AST nodes.",
            "kwargs": "A mapping of keyword argument names to AST nodes.",
        },
    },
    "ClassDefineNode": {
        "sm": "Represents a class definition.",
        "lo": """A class definition node represents declaring a class
containing attributes, methods, and other supported members.

It stores the class name, parent information, and class body.

The transpiler generates a C++ class with a public section
and translates its body.

The inspected implementation also contains special handling
for classes inheriting from Board.

Example:
    class Robot:
        def move(self):
            pass""",
        "params": {
            "name": "The name of the class.",
            "parents": "The parent classes or base-class identifiers.",
            "body": "The AST nodes contained inside the class definition.",
        },
    },
    "GetItemNode": {
        "sm": "Represents retrieving an element using indexing.",
        "lo": """A get-item node represents accessing an element from
a collection or another indexable object.

It stores the object being accessed and the index expression.

The transpiler generates an indexed access expression.

Examples:
    numbers[0]
    matrix[row]
    values[index]""",
        "params": {
            "obj": "The AST node representing the object being accessed.",
            "index": "The AST node representing the index or key.",
        },
    },
    "SetItemNode": {
        "sm": "Represents assigning a value to an indexed element.",
        "lo": """A set-item node represents modifying an element of
a collection through indexed access.

It contains a get-item expression identifying the target
element and a value to assign to it.

The transpiler generates an assignment to that indexed
location.

Example:
    numbers[0] = 100""",
        "params": {
            "getitem": "The GetItemNode identifying the target element.",
            "val": "The AST node representing the value being assigned.",
        },
    },
    "PassNode": {
        "sm": "Represents a pass statement.",
        "lo": """A pass node represents an intentional empty statement.

It can be used as a placeholder where a statement is
syntactically required but no operation needs to be performed.

The inspected transpiler emits an empty line for this node.

Example:
    def unfinished_function():
        pass""",
        "params": {},
    },
    "AttributeAccessNode": {
        "sm": "Represents accessing an attribute of an object.",
        "lo": """An attribute access node represents accessing a named
attribute or property belonging to another object.

It stores the object being accessed and the attribute name.

The transpiler normally generates member access using
the C++ dot operator. Inside certain class methods,
it handles access to the current instance using this->.

Examples:
    robot.speed
    sensor.value
    self.position""",
        "params": {
            "obj": "The AST node representing the object.",
            "name": "The name of the attribute being accessed.",
        },
    },
    "FromImportNode": {
        "sm": "Represents an import-from statement.",
        "lo": """A from-import node represents importing selected
names from a module.

It is part of the AST representation of import syntax.

In the inspected transpiler implementation, this node
currently produces an empty output string. Therefore,
its presence in the AST does not imply that import
translation is fully implemented.

The exact fields of this node are not exposed by the
inspected transpiler visitor.""",
        "params": {
            "_note": "Exact parameter names are not visible in the inspected transpiler source."
        },
    },
    "BreakNode": {
        "sm": "Represents a break statement.",
        "lo": """A break node represents an instruction to immediately
terminate the nearest enclosing loop.

The transpiler generates the corresponding C++ break
statement.

Example:
    while True:
        if finished:
            break""",
        "params": {},
    },
    "ContinueNode": {
        "sm": "Represents a continue statement.",
        "lo": """A continue node represents an instruction to skip
the remaining statements in the current loop iteration
and proceed to the next iteration.

The transpiler generates the corresponding C++ continue
statement.

Example:
    for i in range(10):
        if i == 5:
            continue""",
        "params": {},
    },
    "no": {
        "sm": "This is probably a ast argument. There is no description provided.",
        "lo": "This is probably a ast argument. There is no description provided.",
    },
    "ProgramNode": {
        "sm": "Represents the root node of a program's Abstract Syntax Tree (AST).",
        "lo": """
The ProgramNode is the root node of the Abstract Syntax Tree.

It represents the entire source program and acts as the container
for all top-level statements and declarations.

The parser typically creates one ProgramNode after successfully
parsing the source code. Its body contains the statements that
make up the program, such as variable assignments, function
definitions, class declarations, loops, and conditional statements.

Example:
    x = 10
    print(x)

The AST may be represented as:

    ProgramNode
    └── body
        ├── VariableAssignNode
        └── CallNode
""",
        "params": {
            "body": "A collection of top-level AST nodes representing the program's statements."
        },
    },
}


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

        lines.append("=" * 45)
        lines.append("SMALL DESCRIPTION")
        lines.append("=" * 45)

        lines.append(
            AST_NODES.get(type(value).__name__, {}).get(
                "sm", "No documentation available."
            )
        )

        lines.append("=" * 45)
        lines.append("LONG DESCRIPTION")
        lines.append("=" * 45)

        lines.append(
            "\n"
            + AST_NODES.get(type(value).__name__, {}).get(
                "lo", "No documentation available."
            )
        )

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
