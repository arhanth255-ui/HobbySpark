# HobbySpark Commit Format
**File:** `COMMIT_FORMAT.md`  
**Version:** 1.0

## 1. Introduction

HobbySpark uses a structured commit-message format to keep its Git history readable, consistent, and meaningful.

Instead of writing arbitrary commit messages, every commit follows a predictable structure that communicates:

- What kind of change was made.
- Which part of the project was affected.
- What the change actually does.
- Additional details about the implementation, when necessary.

## 2. General Syntax

A commit message follows this structure:

```text
<type>(<scope>): <description>

- <change 1>
- <change 2>
- <change 3>
```

The first line is the **commit header**. Everything following the blank line is the optional **commit body**.

### Header components

| Component | Description |
|---|---|
| `type` | Category of the change |
| `scope` | Component or area affected |
| `description` | Short explanation of the change |

The scope is optional.

Example:

```text
feat(parser): add dictionary parsing support
```

A commit without a scope:

```text
docs: update installation instructions
```

## 3. Commit Types

The following types describe the purpose of a commit.

| Type | Meaning |
|---|---|
| `feat` | Introduces a new feature |
| `fix` | Fixes a bug or incorrect behaviour |
| `refactor` | Restructures existing code without changing intended behaviour |
| `docs` | Changes documentation |
| `style` | Changes formatting or code style without affecting behaviour |
| `test` | Adds or modifies tests |
| `perf` | Improves performance |
| `build` | Changes build systems or dependencies |
| `chore` | Performs maintenance or other miscellaneous tasks |

## 4. Scopes

A scope identifies the part of the project affected by the commit.

Scopes should be short, descriptive, and preferably related to actual project components.

Examples:

```text
feat(lexer): add hexadecimal number support
fix(parser): correct operator precedence
refactor(transpiler): simplify expression generation
docs(cli): document the parse command
feat(ast-explorer): add node search
```

Possible HobbySpark scopes include:

- `lexer`
- `parser`
- `transpiler`
- `semantic`
- `cli`
- `ast-explorer`
- `electron`
- `pyside`
- `docs`
- `tests`

These are examples, not an exhaustive list.

## 5. Descriptions

The description should communicate the change directly.

Guidelines:

- Keep it concise.
- Use imperative wording where practical.
- Avoid unnecessary explanations.
- Do not end the header with a full stop.
- Describe what changed rather than how difficult it was.

Good:

```text
feat(lexer): support hexadecimal literals
```

Avoid:

```text
fixed some stuff in the lexer
```

## 6. Commit Body

The commit body provides additional information about the changes.

It is optional, but useful for commits involving multiple modifications.

Use hyphen-prefixed lines to describe individual changes.

Example:

```text
feat(ast-explorer): add interactive AST inspection

- Implement recursive AST visualization.
- Add support for nested collections.
- Introduce object inspection.
- Add AST search and navigation.
- Synchronize the inspector with tree selection.
```

Each bullet should describe a meaningful change.

## 7. Breaking Changes

A breaking change introduces a modification that may cause previously working code, APIs, or workflows to stop working.

Breaking changes should be explicitly declared using:

```text
BREAKING CHANGE: <description>
```

Example:

```text
feat(cli): redesign command-line arguments

BREAKING CHANGE: The old positional argument format is no longer supported.
```

## 8. Versioning Convention

Commit types can also communicate the likely Semantic Versioning impact.

| Change | Typical version impact |
|---|---|
| `fix` | Patch |
| `feat` | Minor |
| Breaking change | Major |

This is a convention, not an automatic guarantee.

## 9. Complete Examples

### Feature

```text
feat(lexer): support hexadecimal numbers

- Recognize hexadecimal number literals.
- Convert hexadecimal values into numeric tokens.
- Add invalid hexadecimal input handling.
```

### Bug fix

```text
fix(transpiler): correct boolean expression generation

- Fix incorrect boolean operator output.
- Preserve expression precedence.
```

### Refactoring

```text
refactor(parser): simplify expression parsing

- Reduce duplicated parsing logic.
- Improve parser readability.
```

### Documentation

```text
docs(cli): explain the lex command

- Describe token generation.
- Add token type explanations.
- Include command usage examples.
```

### Breaking change

```text
feat(api): redesign transpiler interface

- Introduce a unified transpilation entry point.
- Remove obsolete interface methods.

BREAKING CHANGE: Previous transpiler entry points have been removed.
```

## 10. General Rules

1. Every commit must have a valid type.
2. Scopes should identify the affected component when useful.
3. Descriptions should be concise and meaningful.
4. A blank line separates the header from the body.
5. Body entries use `-` as their bullet marker.
6. Breaking changes must be explicitly identified.
7. Commit messages should describe actual changes, not intended future work.

---

**The goal:** A commit history should tell the story of a project's development without requiring someone to inspect every individual code change.