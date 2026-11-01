
import sys
from pathlib import Path
import subprocess
import shutil

from pager_maker import QApplication, MainWindow

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
    print(f"{DIM}Commands: build, upload, transpile-test{RESET}\n")
    sys.exit(1)

import lexer
import transpiler
import parser

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
    print(f"  {CYAN}build{RESET} <file> <board>             Compile a HobbySpark program")
    print(f"  {CYAN}upload{RESET} <file> <board> <port>    Compile and upload to a board")
    print(f"  {CYAN}transpile-test{RESET} <file>           Test transpilation only")
    print(f"  {CYAN}boards{RESET}                           List supported boards")
    print(f"  {CYAN}ports{RESET}                            List serial ports")

    print(f"\n{BOLD}OPTIONS{RESET}")
    print(f"  {MAGENTA}--verbose{RESET}                         Show compiler debug output")
    print(f"  {MAGENTA}--help, -h{RESET}                       Show this help message")
    print(f"  {MAGENTA}--version{RESET}                        Show the CLI version")

    print(f"\n{BOLD}EXAMPLES{RESET}")
    print(f"  {DIM}hobbyspark build main.py ArduinoUnoR3{RESET}")
    print(f"  {DIM}hobbyspark upload main.py ArduinoNano /dev/ttyUSB0(on linux){RESET}")
    print(f"  {DIM}hobbyspark transpile-test main.py{RESET}")

    print(f"\n{DIM}HobbySpark — From Python-like code to microcontrollers. ⚡{RESET}\n")
    print("For more information, please go to HobbySpark's website, sites.google.com/view/hobbyspark.")

def build(file_in_question, board, verbose=False):
    banner()
    info("Build mode: compile only — no firmware upload.")
    cwd = Path.cwd()
    with open(file_in_question) as f:
        code = f.read()
    stage("checking stage", "Running your file")
    python = shutil.which("python") or shutil.which("python3")

    if python is None:
        error("Python was not found on your system. Please install python on your system to use HobbySpark.")
        raise RuntimeError("Python is not installed or could not be found.")

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    success_ = window.run(file_in_question, python)
    if success_ is False:
        info("The program will not compile due to an error.")
        raise RuntimeError("Program execution failed.")
    if success_ is None:
        warning("You closed the run window before it finished running. The program will not compile.")
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

    Path.mkdir(Path(cwd) / "COMPILATION" / file_in_question,
                exist_ok=True, parents=True)

    with open(
        Path(cwd) / "COMPILATION" / file_in_question /
        (file_in_question + ".ino"),
        "w"
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
        capture_output=True,
        text=True,
        creationflags=WINDOWS_CREATION_FLAGS
    )

    if result.returncode != 0:
        error("Compilation failed")
        if result.stderr:
            print(f"{RED}{result.stderr}{RESET}")
        raise Exception(f"Error during compilation: {result.stderr}")

    success("Compilation completed successfully!")
    print(f"\n{BOLD}{GREEN}⚡ Build successful!{RESET}")
    print(f"{DIM}Your sketch is ready in COMPILATION/{file_in_question}/{RESET}\n")

def transpile_test(file_in_question, verbose=False):
    banner()

    with open(file_in_question) as f:
        code = f.read()
    stage("checking stage", "Running your file")
    python = shutil.which("python") or shutil.which("python3")
    
    if python is None:
        error("Python was not found on your system. Please install python on your system to use HobbySpark.")
        raise RuntimeError("Python is not installed or could not be found.")
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    success_ = window.run(file_in_question, python)
    if success_ is None:
        warning("You closed the run window before it finished running. The program will not compile.")
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
        error("Python was not found on your system. Please install python on your system to use HobbySpark.")
        raise RuntimeError("Python is not installed or could not be found.")
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    success_ = window.run(file_in_question, python)
    if success_ is None:
        warning("You closed the run window before it finished running. The program will not compile.")
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

    Path.mkdir(Path(cwd) / "COMPILATION" / file_in_question,
                exist_ok=True, parents=True)

    with open(
        Path(cwd) / "COMPILATION" / file_in_question /
        (file_in_question + ".ino"),
        "w"
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
        creationflags=WINDOWS_CREATION_FLAGS
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
        creationflags=WINDOWS_CREATION_FLAGS
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
            creationflags=WINDOWS_CREATION_FLAGS
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
            build(
                args[0],
                args[1],
                len(args) == 3 and args[2] == "--verbose"
            )
        except Exception as e:
            command_exit_code = 1
            error(str(e))
            if type(e).__name__ == "IndexError":
                print(f"{BOLD} Usage: {RESET} {CYAN} hobbyspark build {MAGENTA}<file> <board> {CYAN}[{RESET} {YELLOW}--verbose{RESET}{CYAN}] {RESET}")

    elif command == "transpile-test":
        try:
            transpile_test(
                args[0],
                "--verbose" in args
            )
        except Exception as e:
            command_exit_code = 1
            error(str(e))
            if type(e).__name__ == "IndexError":
                print(f"{BOLD} Usage: {RESET} {CYAN} hobbyspark transpile-test {MAGENTA}<file> {CYAN}[{RESET} {YELLOW}--verbose{RESET}{CYAN}] {RESET}")

    elif command == "upload":
        try:
            upload(
                args[0],
                args[1],
                args[2],
                "--verbose" in args
            )
        except Exception as e:
            command_exit_code = 1
            error(str(e))
            if type(e).__name__ == "IndexError":
                print(f"{BOLD} Usage: {RESET} {CYAN} hobbyspark upload {MAGENTA}<file> <board> <port> {CYAN}[{RESET} {YELLOW}--verbose{RESET}{CYAN}] {RESET}")

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
        print(f"{DIM}Available commands: build, upload, transpile-test{RESET}")
        command_exit_code = 1

except KeyboardInterrupt:
    command_exit_code = 130
    warning("Operation interrupted by user.")

finally:
    # Only notify the IDE about operations whose completion it needs to track.
    if command in ("build", "upload", "transpile-test"):
        notify_command_finished(command_exit_code)

sys.exit(command_exit_code)
