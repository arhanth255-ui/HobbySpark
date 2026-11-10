import shutil
import subprocess
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from ast_visualizer import visualize_ast
from pager_helper import MainWindow, QApplication

# ── Terminal styling ──────────────────────────────────────────

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"


def banner():
    print(f"\n{BOLD}{MAGENTA}⚡ HobbySpark{RESET} {DIM}Arduino Transpiler{RESET}")
    print(f"{DIM}{'━' * 48}{RESET}")


def info(message):
    print(f"{CYAN}ℹ{RESET}  {message}")


def stage(number, message):
    print(f"\n{BOLD}{CYAN}[{number}]{RESET} {BOLD}{message}...{RESET}")


def success(message):
    print(f"{GREEN}✔{RESET}  {message}")


def warning(message):
    print(f"{YELLOW}⚠{RESET}  {message}")


def error(message):
    print(f"{RED}✖{RESET}  {BOLD}{message}{RESET}")


if len(sys.argv) < 2:
    banner()
    error("No command provided.")
    print(f"\n{BOLD}Usage:{RESET} hobbyspark <command> <arguments>")
    print(
        f"{DIM}Available commands: build, upload, transpile-test, run, lex, parse, boards, ports{RESET}\n"
    )
    sys.exit(1)

import lexer
import parser
import transpiler

WINDOWS_CREATION_FLAGS = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0

ALL_BOARDS = {
    # Arduino AVR
    "ArduinoUnoR3": "arduino:avr:uno",
    "ArduinoNano": "arduino:avr:nano",
    "ArduinoMega2560": "arduino:avr:mega",
    "ArduinoLeonardo": "arduino:avr:leonardo",
    "ArduinoMicro": "arduino:avr:micro",
    "ArduinoMini": "arduino:avr:mini",
    "ArduinoProMini": "arduino:avr:pro",
    "ArduinoLilyPad": "arduino:avr:lilypad",
    # Arduino megaAVR
    "ArduinoNanoEvery": "arduino:megaavr:nona4809",
    "ArduinoUnoWiFiRev2": "arduino:megaavr:uno2018",
    # Arduino SAM
    "ArduinoDue": "arduino:sam:arduino_due_x",
    # Arduino SAMD
    "ArduinoZero": "arduino:samd:arduino_zero",
    # Arduino GIGA
    "ArduinoGigaR1": "arduino:mbed_giga:giga",
    # ESP32
    "ESP32DevKit": "esp32:esp32:esp32",
    "ESP32C3": "esp32:esp32:esp32c3",
    "ESP32S2": "esp32:esp32:esp32s2",
    "ESP32S3": "esp32:esp32:esp32s3",
    "ArduinoNanoESP32": "esp32:esp32:nano_nora",
    "AdafruitFeatherESP32S2": "esp32:esp32:adafruit_feather_esp32s2",
    "SeeeduinoXIAOESP32C3": "esp32:esp32:XIAO_ESP32C3",
    # ESP8266
    "ESP8266NodeMCU": "esp8266:esp8266:nodemcuv2",
    "ESP8266D1Mini": "esp8266:esp8266:d1_mini",
    # RP2040
    "RaspberryPiPico": "rp2040:rp2040:rpipico",
    "RaspberryPiPicoW": "rp2040:rp2040:rpipicow",
    # STM32
    "STM32BluePill": "STMicroelectronics:stm32:GenF1",
    "STM32BlackPill": "STMicroelectronics:stm32:GenF4",
    # Teensy
    "Teensy40": "teensy:avr:teensy40",
    "Teensy41": "teensy:avr:teensy41",
    # Adafruit SAMD
    "AdafruitFeatherM0": "adafruit:samd:adafruit_feather_m0",
    # Seeed SAMD
    "SeeeduinoXIAO": "Seeeduino:samd:seeed_XIAO_m0",
}


def notify_command_finished(exit_code):
    print(f"\x1b]777;HOBBYSPARK;FINISHED;{exit_code}\x07", end="", flush=True)


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).resolve().parent

    return str(base / relative)


def show_help():
    banner()

    print(f"{BOLD}USAGE{RESET}")
    print(f"  {CYAN}hobbyspark{RESET} <command> [arguments]")

    print(f"\n{BOLD}COMMANDS{RESET}")
    print(
        f"  {CYAN}build{RESET} <file> <board>             Compile a HobbySpark program"
    )
    print(
        f"  {CYAN}upload{RESET} <file> <board> <port>    Compile and upload to a board"
    )
    print(f"  {CYAN}transpile-test{RESET} <file>           Test transpilation only")
    print(f"  {CYAN}boards{RESET}                           List supported boards")
    print(f"  {CYAN}ports{RESET}                            List serial ports")

    print(f"\n{BOLD}OPTIONS{RESET}")
    print(
        f"  {MAGENTA}--verbose{RESET}                         Show compiler debug output"
    )
    print(f"  {MAGENTA}--help, -h{RESET}                       Show this help message")
    print(f"  {MAGENTA}--version{RESET}                        Show the CLI version")

    print(f"\n{BOLD}EXAMPLES{RESET}")
    print(f"  {DIM}hobbyspark build main.py ArduinoUnoR3{RESET}")
    print(f"  {DIM}hobbyspark upload main.py ArduinoNano /dev/ttyUSB0(on linux){RESET}")
    print(f"  {DIM}hobbyspark transpile-test main.py{RESET}")

    print(f"\n{DIM}HobbySpark — From Python-like code to microcontrollers. ⚡{RESET}\n")
    print(
        "For more information, please go to HobbySpark's website, sites.google.com/view/hobbyspark."
    )


def run(file_in_question):
    banner()
    info("Run mode: run only — no transpilation.")
    python = shutil.which("python") or shutil.which("python3")

    if python is None:
        error(
            "Python was not found on your system. Please install python on your system to use HobbySpark."
        )
        raise RuntimeError("Python is not installed or could not be found.")

    QApplication(sys.argv)
    window = MainWindow()
    window.show()

    success_ = window.run(file_in_question, python)
    if success_ is False:
        info("The program will not compile due to an error.")
        raise RuntimeError("Program execution failed.")
    if success_ is None:
        warning(
            "You closed the run window before it finished running. The program will not compile."
        )
        raise RuntimeError("Program execution was cancelled.")

    success("Ran succesfully")


def build(file_in_question, board, verbose=False):
    banner()
    info("Build mode: compile only — no firmware upload.")
    cwd = Path.cwd()
    with open(file_in_question) as f:
        code = f.read()
    stage("checking stage", "Running your file")
    python = shutil.which("python") or shutil.which("python3")

    if python is None:
        error(
            "Python was not found on your system. Please install python on your system to use HobbySpark."
        )
        raise RuntimeError("Python is not installed or could not be found.")

    QApplication(sys.argv)
    window = MainWindow()
    window.show()

    success_ = window.run(file_in_question, python)
    if success_ is False:
        info("The program will not compile due to an error.")
        raise RuntimeError("Program execution failed.")
    if success_ is None:
        warning(
            "You closed the run window before it finished running. The program will not compile."
        )
        raise RuntimeError("Program execution was cancelled.")

    success("Ran succesfully")

    if verbose:
        lexer.verbose = parser.verbose = transpiler.verbose = True

    stage("1/4", "Lexing")
    try:
        lexed = lexer.Lexer(code).evaluate()
        success("Lexing completed")
    except Exception as e:
        error(f"Lexing failed: {e}")
        print(type(e).__name__)
        raise Exception(f"Failed to lex code: {e}")

    stage("2/4", "Parsing")
    try:
        parsed = parser.Parser(lexed).parse()
        success("Parsing completed")
    except Exception as e:
        error(f"Parsing failed: {e}")
        raise Exception(f"Failed to parse code: {e}")

    stage("3/4", "Transpiling")
    try:
        transpiled = transpiler.Transpiler(parsed).translate()
        success("Transpilation completed")
    except Exception as e:
        error(f"Transpilation failed: {e}")
        raise Exception(f"Failed to transpile code: {e}")

    stage("4/4", "Generating sketch")

    Path.mkdir(
        Path(cwd) / "COMPILATION" / file_in_question, exist_ok=True, parents=True
    )

    with open(
        Path(cwd) / "COMPILATION" / file_in_question / (file_in_question + ".ino"), "w"
    ) as f:
        f.write("\n".join(transpiled))

    with open(cwd / "COMPILATION" / "package.h", "w") as f:  # noqa: SIM117
        with open(resource_path("package.h"), "r") as f2:
            f.write(f2.read())

    success(f"Generated {file_in_question}.ino")

    fqbn = ALL_BOARDS[board]
    compilation_path = cwd / "COMPILATION" / file_in_question

    print(f"\n{DIM}Board: {board}{RESET}")
    print(f"{DIM}FQBN:  {fqbn}{RESET}")
    print(f"{DIM}Path:  {compilation_path}{RESET}")

    stage("4/4", "Compiling for Arduino")

    result = subprocess.run(
        [
            "arduino-cli",
            "compile",
            "--fqbn",
            fqbn,
            "--build-property",
            f"compiler.cpp.extra_flags=-I{cwd / 'COMPILATION'}",
            str(compilation_path),
        ],
        check=False,
        capture_output=True,
        text=True,
        creationflags=WINDOWS_CREATION_FLAGS,
    )

    if result.returncode != 0:
        error("Compilation failed")
        if result.stderr:
            print(f"{RED}{result.stderr}{RESET}")
        raise Exception(f"Error during compilation: {result.stderr}")

    success("Compilation completed successfully!")
    print(f"\n{BOLD}{GREEN}⚡ Build successful!{RESET}")
    print(f"{DIM}Your sketch is ready in COMPILATION/{file_in_question}/{RESET}\n")


def lex(file_in_question, verbose=False):
    banner()

    with open(file_in_question) as f:
        code = f.read()
    stage("checking stage", "Running your file")
    python = shutil.which("python") or shutil.which("python3")

    if python is None:
        error(
            "Python was not found on your system. Please install python on your system to use HobbySpark."
        )
        raise RuntimeError("Python is not installed or could not be found.")

    QApplication(sys.argv)
    window = MainWindow()
    window.show()

    success_ = window.run(file_in_question, python)
    if success_ is None:
        warning(
            "You closed the run window before it finished running. The program will not compile."
        )
        raise RuntimeError("Program execution was cancelled.")
    if success_ is False:
        info("The program will not compile due to an error.")
        raise RuntimeError("Program execution failed.")

    success("Ran succesfully")

    stage("1/1", "Lexing")
    if verbose:
        lexer.verbose = True
    try:
        lexed = lexer.Lexer(code).evaluate()
        success("Lexing completed")
    except Exception as e:
        error(f"Lexing failed: {e}")
        raise Exception(f"Failed to lex code: {e}")  # noqa: TRY002

    print(
        f"{RED}Please note that this command may show you advanced stuff, so don't worry if you don't understand any part of the text given below. "
    )

    print(f"""{CYAN}If you thought lexing was some sort of secret magic spell thing, its not that. Lexing is a super stylish term used in compiler engineering. It basically means the conversion of text into small tokens.
Now, you may think, why even tokenize the code when you can directly transpile it? Lexing is actually crucial to the making of a computer language. Think of a giant choclate bar, this will be our code. Do you eat the entire choclate bar at once? Definetly not. We have to take small bites, one by one, and at last, the entire choclate bar is eaten. These small bits of choclates are tokens. They make the other steps of the process more easier to implement. 
Tokens may also take up bits of information like a value. Not all tokens have a value. Only tokens like TT_NUMBER, or TT_IDENTIFIER, have a value. """)
    print(
        f"""To give you a better idea of a `token`, let's look at an example using your own code. The tokens that were generated by the lexer in your code is: {lexed}"""
    )
    print("""Here is a guide to all the token types used in HobbySpark:
IDENTIFIER — The universal token used for names of things, like variables, class names, and function names. Takes one value, which is the name.
NUMBER — The token used to represent floats and integers. Takes one value, which is the number.
STRING — The token used to represnt strings. Takes one value, which is the text inside the string.
ASSIGN — The token used to represent `==`.
ADD — The token used to represent `+`.
MINUS — The token used to represent `-`.
MULTIPLY — The token used to represent `*`, it is also used to represent the stars behind a *args and a **kawargs argument.
DIVISION — The token used to represent `/`.
FLOOR_DIVISION — The token used to represent `//`, which is used for floor division in python.
POWER — The token used to represent `**`, which is used for power in python.
MODULUS — The token used to represent `%`, which is used to find the remainder after dividing in python.
TODO: COMPLETE THIS LIST
""")


def parse(file_in_question, verbose=False):
    banner()

    with open(file_in_question) as f:
        code = f.read()
    stage("checking stage", "Running your file")
    python = shutil.which("python") or shutil.which("python3")

    if python is None:
        error(
            "Python was not found on your system. Please install python on your system to use HobbySpark."
        )
        raise RuntimeError("Python is not installed or could not be found.")

    QApplication(sys.argv)
    window = MainWindow()
    window.show()

    success_ = window.run(file_in_question, python)
    if success_ is None:
        warning(
            "You closed the run window before it finished running. The program will not compile."
        )
        raise RuntimeError("Program execution was cancelled.")
    if success_ is False:
        info("The program will not compile due to an error.")
        raise RuntimeError("Program execution failed.")

    success("Ran succesfully")

    stage("1/2", "Lexing")
    if verbose:
        lexer.verbose = True
    try:
        lexed = lexer.Lexer(code).evaluate()
        success("Lexing completed")
    except Exception as e:  # noqa: BLE001
        error(f"Lexing failed: {e}")
        raise Exception(f"Failed to lex code: {e}")  # noqa: TRY002

    stage("2/2", "Parsing")
    if verbose:
        parser.verbose = True
    try:
        parsed = parser.Parser(lexed).parse()
        success("Parsing completed")
    except Exception as e:  # noqa: BLE001
        error(f"Parsing failed: {e}")
        raise Exception(f"Failed to parse code: {e}")  # noqa: TRY002

    print(f"""{RED}WARNING: Parsing is a more advanced stage of compiler engineering.
The output may contain technical terms and structures that you might
not understand yet. That's completely normal! You don't need to
understand everything to continue.""")

    print(f"""{CYAN}So, you've seen how your code gets broken down into tokens.
But here's a question: how does the computer understand how those
tokens are related to each other?

That's where parsing comes in!

Parsing is the process of analysing a sequence of tokens and
organising them into a structured representation of your program.
This representation is commonly called an Abstract Syntax Tree,
or AST for short.

Think of it like building a sentence. You have individual words,
but simply knowing the words isn't enough to understand the sentence.
You need to understand how those words are arranged and how they
relate to one another.

Parsing does exactly that with your code!

For example, consider this expression:

    5 + 3 * 2

The parser doesn't just see a collection of numbers and operators.
It understands that multiplication must happen before addition.
It represents that relationship in the AST.

The AST is then passed to the next stages of the compiler or
transpiler, where it can be analysed, transformed, or translated
into another programming language.""")
    print(
        f"\nNow, a window will open displaying your program's AST. "
        f"Feel free to explore it! Click on different nodes to inspect "
        f"their structure, attributes, and relationships. "
        f"Have fun exploring HobbySpark's AST! {RESET}"
    )

    app = QApplication.instance()

    if app is None:
        app = QApplication(sys.argv)

    window = visualize_ast(parsed)
    window.show()

    sys.exit(app.exec())


def transpile_test(file_in_question, verbose=False):
    banner()

    with open(file_in_question) as f:
        code = f.read()
    stage("checking stage", "Running your file")
    python = shutil.which("python") or shutil.which("python3")

    if python is None:
        error(
            "Python was not found on your system. Please install python on your system to use HobbySpark."
        )
        raise RuntimeError("Python is not installed or could not be found.")

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    success_ = window.run(file_in_question, python)
    if success_ is None:
        warning(
            "You closed the run window before it finished running. The program will not compile."
        )
        raise RuntimeError("Program execution was cancelled.")
    if success_ is False:
        info("The program will not compile due to an error.")
        raise RuntimeError("Program execution failed.")

    success("Ran succesfully")

    if verbose:
        lexer.verbose = parser.verbose = transpiler.verbose = True

    stage("1/3", "Lexing")
    try:
        lexed = lexer.Lexer(code).evaluate()
        success("Lexing completed")
    except Exception as e:
        error(f"Lexing failed: {e}")
        raise Exception(f"Failed to lex code: {e}")

    stage("2/3", "Parsing")
    try:
        parsed = parser.Parser(lexed).parse()
        success("Parsing completed")
    except Exception as e:
        error(f"Parsing failed: {e}")
        raise Exception(f"Failed to parse code: {e}")

    stage("3/3", "Transpiling")
    try:
        transpiler.Transpiler(parsed).translate()
        success("Transpilation completed")
    except Exception as e:
        error(f"Transpilation failed: {e}")
        raise Exception(f"Failed to transpile code: {e}")

    print(f"\n{BOLD}{GREEN}⚡ Transpile test successful!{RESET}\n")


def upload(file_in_question, board, port, verbose=False):
    banner()
    info("Upload mode: transpile, compile, and upload firmware.")
    cwd = Path.cwd()

    with open(file_in_question) as f:
        code = f.read()
    stage("checking stage", "Running your file")
    python = shutil.which("python") or shutil.which("python3")

    if python is None:
        error(
            "Python was not found on your system. Please install python on your system to use HobbySpark."
        )
        raise RuntimeError("Python is not installed or could not be found.")

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    success_ = window.run(file_in_question, python)
    if success_ is None:
        warning(
            "You closed the run window before it finished running. The program will not compile."
        )
        raise RuntimeError("Program execution was cancelled.")
    if success_ is False:
        info("The program will not compile due to an error.")
        raise RuntimeError("Program execution failed.")

    success("Ran succesfully")

    if verbose:
        lexer.verbose = parser.verbose = transpiler.verbose = True

    stage("1/4", "Lexing")
    try:
        lexed = lexer.Lexer(code).evaluate()
        success("Lexing completed")
    except Exception as e:
        error(f"Lexing failed: {e}")
        raise Exception(f"Failed to lex code: {e}")

    stage("2/4", "Parsing")
    try:
        parsed = parser.Parser(lexed).parse()
        success("Parsing completed")
    except Exception as e:
        error(f"Parsing failed: {e}")
        raise Exception(f"Failed to parse code: {e}")

    stage("3/4", "Transpiling")
    try:
        transpiled = transpiler.Transpiler(parsed).translate()
        success("Transpilation completed")
    except Exception as e:
        error(f"Transpilation failed: {e}")
        raise Exception(f"Failed to transpile code: {e}")

    Path.mkdir(
        Path(cwd) / "COMPILATION" / file_in_question, exist_ok=True, parents=True
    )

    with open(
        Path(cwd) / "COMPILATION" / file_in_question / (file_in_question + ".ino"), "w"
    ) as f:
        f.write("\n".join(transpiled))

    with open(cwd / "COMPILATION" / "package.h", "w") as f:
        with open(resource_path("package.h"), "r") as f2:
            f.write(f2.read())

    success(f"Generated {file_in_question}.ino")

    fqbn = ALL_BOARDS[board]
    compilation_path = cwd / "COMPILATION" / file_in_question

    print(f"\n{DIM}Board: {board}{RESET}")
    print(f"{DIM}FQBN:  {fqbn}{RESET}")
    print(f"{DIM}Port:  {port}{RESET}")

    stage("4/4", "Compiling")

    result = subprocess.run(
        [
            "arduino-cli",
            "compile",
            "--fqbn",
            fqbn,
            "--build-property",
            f"compiler.cpp.extra_flags=-I{cwd / 'COMPILATION'}",
            str(compilation_path),
        ],
        capture_output=True,
        text=True,
        creationflags=WINDOWS_CREATION_FLAGS,
    )

    if result.returncode != 0:
        error("Compilation failed")
        if result.stderr:
            print(f"{RED}{result.stderr}{RESET}")
        raise Exception(f"Error during compilation: {result.stderr}")

    success("Compilation completed")

    stage("Upload", "Uploading firmware")

    result = subprocess.run(
        [
            "arduino-cli",
            "upload",
            "-p",
            port,
            "--fqbn",
            fqbn,
            str(compilation_path),
        ],
        capture_output=True,
        text=True,
        creationflags=WINDOWS_CREATION_FLAGS,
    )

    if result.returncode != 0:
        error("Upload failed")
        if result.stderr:
            print(f"{RED}{result.stderr}{RESET}")
        raise Exception(f"Could not upload: {result.stderr}")

    success("Firmware uploaded successfully!")
    if result.stdout.strip():
        print(f"{DIM}{result.stdout.strip()}{RESET}")

    print(f"\n{BOLD}{GREEN}⚡ Upload successful!{RESET}\n")


def boards():
    banner()
    print(f"{BOLD}SUPPORTED BOARDS{RESET}\n")

    for name, fqbn in ALL_BOARDS.items():
        print(f"  {CYAN}{name:<28}{RESET} {DIM}{fqbn}{RESET}")

    print(f"\n{GREEN}{len(ALL_BOARDS)} boards supported{RESET}\n")


def ports():
    banner()
    print(f"{BOLD}CONNECTED BOARDS AND PORTS{RESET}\n")

    try:
        result = subprocess.run(
            ["arduino-cli", "board", "list"],
            capture_output=True,
            text=True,
            creationflags=WINDOWS_CREATION_FLAGS,
        )
    except FileNotFoundError:
        error("arduino-cli was not found. Is it installed and on PATH?")
        return

    if result.returncode != 0:
        error("Could not list connected boards and ports.")
        if result.stderr:
            print(f"{RED}{result.stderr.strip()}{RESET}")
        return

    if not result.stdout.strip():
        warning("No boards or ports detected.")
        return

    print(result.stdout.rstrip())


command = sys.argv[1]
args = sys.argv[2:]

command_exit_code = 0

try:
    if command == "build":
        try:
            build(args[0], args[1], len(args) == 3 and args[2] == "--verbose")
        except Exception as e:
            command_exit_code = 1
            error(str(e))
            if type(e).__name__ == "IndexError":
                print(
                    f"{BOLD} Usage: {RESET} {CYAN} hobbyspark build {MAGENTA}<file> <board> {CYAN}[{RESET} {YELLOW}--verbose{RESET}{CYAN}] {RESET}"
                )

    elif command == "transpile-test":
        try:
            transpile_test(args[0], "--verbose" in args)
        except Exception as e:
            command_exit_code = 1
            error(str(e))
            if type(e).__name__ == "IndexError":
                print(
                    f"{BOLD} Usage: {RESET} {CYAN} hobbyspark transpile-test {MAGENTA}<file> {CYAN}[{RESET} {YELLOW}--verbose{RESET}{CYAN}] {RESET}"
                )

    elif command == "upload":
        try:
            upload(args[0], args[1], args[2], "--verbose" in args)
        except Exception as e:
            command_exit_code = 1
            error(str(e))
            if type(e).__name__ == "IndexError":
                print(
                    f"{BOLD} Usage: {RESET} {CYAN} hobbyspark upload {MAGENTA}<file> <board> <port> {CYAN}[{RESET} {YELLOW}--verbose{RESET}{CYAN}] {RESET}"
                )

    elif command == "run":
        try:
            run(args[0])
        except Exception as e:
            command_exit_code = 1
            error(str(e))
            if type(e).__name__ == "IndexError":
                print(
                    f"{BOLD} Usage: {RESET} {CYAN} hobbyspark run {MAGENTA}<file>{RESET}"
                )

    elif command == "lex":
        try:
            lex(args[0])
        except Exception as e:
            command_exit_code = 1
            error(str(e))
            if type(e).__name__ == "IndexError":
                print(
                    f"{BOLD} Usage: {RESET} {CYAN} hobbyspark lex {MAGENTA}<file>{RESET}"
                )
    elif command == "parse":
        try:
            parse(args[0])
        except Exception as e:
            command_exit_code = 1
            error(str(e))
            if type(e).__name__ == "IndexError":
                print(
                    f"{BOLD} Usage: {RESET} {CYAN} hobbyspark parse {MAGENTA}<file>{RESET}"
                )

    elif command == "boards":
        boards()
    elif command == "ports":
        ports()

    elif command in ("--help", "help", "-h"):
        show_help()

    elif command == "--version":
        import contextlib
        import io

        with contextlib.redirect_stdout(io.StringIO()):
            import stub
        print(f"HobbySpark v{stub.VERSION}")

    else:
        error(f"Unknown command: {command}")
        print(
            f"{DIM}Available commands: build, upload, transpile-test, run, lex, parse, boards, ports{RESET}"
        )
        command_exit_code = 1

except KeyboardInterrupt:
    command_exit_code = 130
    warning("Operation interrupted by user.")

finally:
    # Only notify the IDE about operations whose completion it needs to track.
    if command in ("build", "upload", "transpile-test", "run", "lex", "parse"):
        notify_command_finished(command_exit_code)

sys.exit(command_exit_code)
