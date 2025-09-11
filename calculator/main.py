# python
import sys
from pkg.calculator import Calculator

def main():
    if len(sys.argv) < 2:
        print('usage: uv run calculator/main.py "3 + 7 * 2"')
        raise SystemExit(1)

    expr = sys.argv[1]
    calc = Calculator()
    result = calc.evaluate(expr)
    # If you want an int-like display for whole numbers:
    if result.is_integer():
        print(int(result))
    else:
        print(result)

if __name__ == "__main__":
    main()