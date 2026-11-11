"""Read-only C++ source viewer with syntax highlighting and system theme detection."""

import sys
from pathlib import Path

from PySide6.QtCore import QRegularExpression, Qt
from PySide6.QtGui import QColor, QFont, QPalette, QSyntaxHighlighter, QTextCharFormat
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

SAMPLE_CPP = """#include <iostream>
#include <string>
#include <vector>

class Greeter {
public:
    explicit Greeter(std::string name) : name_(std::move(name)) {}

    void greet() const {
        std::cout << "Hello, " << name_ << '!\\\\n';
    }

private:
    std::string name_;
};

int main() {
    Greeter greeter{"HobbySpark"};
    greeter.greet();

    const int answer = 40 + 2;
    std::cout << "The answer is " << answer << '\\\\n';
    return 0;
}
"""


class CppHighlighter(QSyntaxHighlighter):
    def __init__(self, document, dark):
        super().__init__(document)
        palette = {
            "keyword": "#c792ea" if dark else "#7b2cbf",
            "type": "#82aaff" if dark else "#005cc5",
            "string": "#c3e88d" if dark else "#22863a",
            "comment": "#718096" if dark else "#6a737d",
            "number": "#f78c6c" if dark else "#d73a49",
            "preprocessor": "#89ddff" if dark else "#6f42c1",
            "function": "#ffcb6b" if dark else "#b05a00",
        }

        def make_format(color, bold=False, italic=False):
            fmt = QTextCharFormat()
            fmt.setForeground(QColor(color))
            if bold:
                fmt.setFontWeight(QFont.Weight.Bold)
            if italic:
                fmt.setFontItalic(True)
            return fmt

        self.rules = []
        keyword_format = make_format(palette["keyword"], bold=True)
        type_format = make_format(palette["type"])
        string_format = make_format(palette["string"])
        comment_format = make_format(palette["comment"], italic=True)
        number_format = make_format(palette["number"])
        preprocessor_format = make_format(palette["preprocessor"])
        function_format = make_format(palette["function"])

        keywords = [
            "alignas",
            "alignof",
            "asm",
            "auto",
            "bool",
            "break",
            "case",
            "catch",
            "char",
            "class",
            "const",
            "constexpr",
            "continue",
            "co_await",
            "co_return",
            "co_yield",
            "decltype",
            "default",
            "delete",
            "do",
            "double",
            "else",
            "enum",
            "explicit",
            "export",
            "extern",
            "false",
            "float",
            "for",
            "friend",
            "if",
            "inline",
            "int",
            "long",
            "mutable",
            "namespace",
            "new",
            "noexcept",
            "nullptr",
            "operator",
            "private",
            "protected",
            "public",
            "register",
            "reinterpret_cast",
            "return",
            "short",
            "signed",
            "sizeof",
            "static",
            "static_assert",
            "static_cast",
            "struct",
            "switch",
            "template",
            "this",
            "thread_local",
            "throw",
            "true",
            "try",
            "typedef",
            "typename",
            "union",
            "unsigned",
            "using",
            "virtual",
            "void",
            "volatile",
            "while",
        ]

        types = [
            "size_t",
            "string",
            "vector",
            "map",
            "set",
            "unordered_map",
            "unordered_set",
            "unique_ptr",
            "shared_ptr",
            "optional",
            "variant",
            "pair",
            "tuple",
            "array",
            "list",
            "deque",
            "stack",
            "queue",
            "iostream",
            "istream",
            "ostream",
            "exception",
        ]

        for word in keywords:
            self.rules.append((QRegularExpression(rf"\b{word}\b"), keyword_format))
        for word in types:
            self.rules.append((QRegularExpression(rf"\b{word}\b"), type_format))

        self.rules.extend(
            [
                (QRegularExpression(r'"([^"\\]|\\.)*"'), string_format),
                (QRegularExpression(r"'([^'\\]|\\.)*'"), string_format),
                (
                    QRegularExpression(
                        r"\b(?:0[xX][0-9A-Fa-f]+|\d+(?:\.\d*)?(?:[eE][+-]?\d+)?)[uUlLfF]*\b"
                    ),
                    number_format,
                ),
                (QRegularExpression(r"^\s*#\s*\w+.*$"), preprocessor_format),
                (QRegularExpression(r"\b[A-Za-z_]\w*(?=\s*\()"), function_format),
                (QRegularExpression(r"//[^\n]*"), comment_format),
            ]
        )
        self.comment_format = comment_format
        self.comment_start = QRegularExpression(r"/\*")
        self.comment_end = QRegularExpression(r"\*/")

    def highlightBlock(self, text):
        for expression, fmt in self.rules:
            matches = expression.globalMatch(text)
            while matches.hasNext():
                match = matches.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

        # Multi-line /* ... */ comments.
        self.setCurrentBlockState(0)
        start = 0
        if self.previousBlockState() != 1:
            match = self.comment_start.match(text)
            start = match.capturedStart() if match.hasMatch() else -1

        while start >= 0:
            end_match = self.comment_end.match(text, start)
            if end_match.hasMatch():
                end = end_match.capturedEnd()
                self.setFormat(start, end - start, self.comment_format)
                next_match = self.comment_start.match(text, end)
                start = next_match.capturedStart() if next_match.hasMatch() else -1
            else:
                self.setFormat(start, len(text) - start, self.comment_format)
                self.setCurrentBlockState(1)
                break


class MainWindow(QMainWindow):
    def __init__(self, filename=None):
        super().__init__()
        self.setWindowTitle("C++ Viewer")
        self.resize(1050, 720)

        # Detect the light/dark palette provided by the system or Qt platform theme.
        system_window = QApplication.palette().color(QPalette.ColorRole.Window)
        self.dark = system_window.lightness() < 128

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        toolbar = QHBoxLayout()
        self.filename_label = QLabel("C++ source viewer")
        self.filename_label.setStyleSheet("font-weight: 600;")
        open_button = QPushButton("Open C++ file")
        open_button.clicked.connect(self.open_file)
        toolbar.addWidget(self.filename_label)
        toolbar.addStretch()
        toolbar.addWidget(open_button)

        self.editor = QPlainTextEdit()
        self.editor.setReadOnly(True)
        self.editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.editor.setTabStopDistance(
            self.editor.fontMetrics().horizontalAdvance(" ") * 4
        )

        font = QFont("JetBrains Mono", 11)
        if not font.exactMatch():
            font = QFont("DejaVu Sans Mono", 11)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.editor.setFont(font)
        self.highlighter = CppHighlighter(self.editor.document(), self.dark)

        if self.dark:
            self.editor.setStyleSheet("""
                QPlainTextEdit {
                    background: #171a21; color: #d6deeb;
                    selection-background-color: #39465c;
                    border: 1px solid #303746; border-radius: 8px;
                    padding: 10px;
                }
            """)
            self.setStyleSheet("""
                QMainWindow, QWidget { background: #20242e; color: #d6deeb; }
                QPushButton {
                    background: #303746; color: #e6edf3;
                    border: 1px solid #414b5d; border-radius: 7px;
                    padding: 8px 13px;
                }
                QPushButton:hover { background: #3b4659; }
                QStatusBar { color: #aab6c5; }
            """)
        else:
            self.editor.setStyleSheet("""
                QPlainTextEdit {
                    background: #ffffff; color: #24292f;
                    selection-background-color: #cce0ff;
                    border: 1px solid #d8dee4; border-radius: 8px;
                    padding: 10px;
                }
            """)
            self.setStyleSheet("""
                QMainWindow, QWidget { background: #f6f8fa; color: #24292f; }
                QPushButton {
                    background: #ffffff; color: #24292f;
                    border: 1px solid #d0d7de; border-radius: 7px;
                    padding: 8px 13px;
                }
                QPushButton:hover { background: #eef2f6; }
                QStatusBar { color: #57606a; }
            """)

        layout.addLayout(toolbar)
        layout.addWidget(self.editor)
        self.setCentralWidget(central)
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage(
            f"System {'dark' if self.dark else 'light'} theme detected · Read-only"
        )
        self.editor.setPlainText(SAMPLE_CPP)

        if filename:
            self.load_file(filename)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open C++ source",
            str(Path.home()),
            "C++ files (*.cpp *.cc *.cxx *.c++ *.h *.hpp *.hh *.hxx);;All files (*)",
        )
        if filename:
            self.load_file(filename)

    def load_file(self, filename):
        path = Path(filename)
        try:
            source = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            QMessageBox.critical(self, "Could not open file", str(exc))
            return
        self.editor.setPlainText(source)
        self.filename_label.setText(path.name)
        self.setWindowTitle(f"{path.name} — C++ Viewer")
        self.statusBar().showMessage(
            f"{path} · {self.editor.blockCount()} lines · Read-only"
        )


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("C++ Viewer")
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    window = MainWindow(None)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
