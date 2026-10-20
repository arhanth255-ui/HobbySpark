
import { Parser, Language, Query } from "web-tree-sitter";
import { getWasmPath, getQueryPath } from "tree-sitter-wasm";
import fs from "node:fs";


async function main() {
    await Parser.init();

    const language = await Language.load(getWasmPath("python"));
    const parser = new Parser();

    parser.setLanguage(language);

    const source = [
        "class ArduinoNano:",
        "    def move(self, angle):",
        "        position = angle",
        "        return position"
    ].join("\n");

    const tree = parser.parse(source);

    console.log("Syntax tree:");
    console.log(tree.rootNode.toString());

    const querySource = fs.readFileSync(
        getQueryPath("python", "highlights"),
        "utf8"
    );

    const query = new Query(language, querySource);

    const captures = query.captures(tree.rootNode);

    for (const capture of captures) {
        console.log({
            name: capture.name,
            text: capture.node.text,
            startRow: capture.node.startPosition.row,
            startColumn: capture.node.startPosition.column,
            endRow: capture.node.endPosition.row,
            endColumn: capture.node.endPosition.column
        });
    }

    query.delete();
    tree.delete();
    parser.delete();
}

main().catch(function (error) {
    console.error(error);
    process.exitCode = 1;
});
