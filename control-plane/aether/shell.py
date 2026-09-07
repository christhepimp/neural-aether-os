from __future__ import annotations

from .kernel import Aether


def main() -> None:
    os = Aether()
    print("Aether OS control plane 0.1 — type 'help', Ctrl-D to leave")
    print(os.interpret("status"))
    while True:
        try:
            line = input("aether> ")
        except (EOFError, KeyboardInterrupt):
            print("\nshutdown")
            break
        out = os.interpret(line)
        if out:
            print(out)


if __name__ == "__main__":
    main()
