import sys
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from my_project.utils.decorators.validator import validate_args


class TestValidateArgs(unittest.TestCase):

    def setUp(self):
        """Set test function"""

        @validate_args()
        def func_with_types(a: int, b: str, c: float = 2.5, d: bool = False):
            return f"{a}, {b}, {c}, {d}"

        @validate_args()
        def func_without_types(x, y: int):
            return f"{x}, {y}"

        @validate_args()
        def func_default_val(x, y: int = 2):
            return f"{x}, {y}"

        @validate_args(debug=True)
        def debug_func(x: int, y: str):
            return f"{x}, {y}"

        @validate_args()
        def func_with_path(x: int, b: Path):
            return f"{x}, {b}"

        self.func_with_types = func_with_types
        self.func_without_types = func_without_types
        self.func_default_val = func_default_val
        self.debug_func = debug_func
        self.func_with_path = func_with_path

    def test_valid_inputs(self):
        self.assertEqual(self.func_with_types(1, "hello"), "1, hello, 2.5, False")
        self.assertEqual(
            self.func_with_types(10, "user", 123.12341, True),
            "10, user, 123.12341, True",
        )

    def test_invalid_type_int(self):
        with self.assertRaises(TypeError) as context:
            self.func_with_types("test_wrong", "test")
        self.assertIn("Argument 'a' must be int, but got str.", str(context.exception))

    def test_invalid_type_string(self):
        with self.assertRaises(TypeError) as context:
            self.func_with_types(1, 2)
        self.assertIn("Argument 'b' must be str, but got int.", str(context.exception))

    def test_invalid_type_float(self):
        with self.assertRaises(TypeError) as context:
            self.func_with_types(1, "test", 2)
        self.assertIn(
            "Argument 'c' must be float, but got int.", str(context.exception)
        )

    def test_invalid_type_bool(self):
        with self.assertRaises(TypeError) as context:
            self.func_with_types(1, "test", d="test_d")
        self.assertIn("Argument 'd' must be bool, but got str.", str(context.exception))

    def test_invalid_none(self):
        with self.assertRaises(ValueError) as context:
            self.func_with_types(None, "test")
        self.assertIn("Argument 'a' cannot be None.", str(context.exception))

    def test_no_type_arg(self):
        self.assertEqual(self.func_without_types("tst", 1), "tst, 1")
        self.assertEqual(self.func_without_types(None, 10), "None, 10")

    def test_invalid_no_type_arg(self):
        with self.assertRaises(TypeError) as context:
            self.func_without_types("tst", "tst")
        self.assertIn("Argument 'y' must be int", str(context.exception))

    def test_default_argument(self):
        self.assertEqual(self.func_default_val("tst"), "tst, 2")
        self.assertEqual(self.func_default_val(1.5), "1.5, 2")

    def test_debug_output(self):
        captured_output = StringIO()
        sys.stdout = captured_output

        self.debug_func(1, "test")

        output = captured_output.getvalue()
        self.assertIn(
            f"\n🔍 Debug: Executed `debug_func\n   📌 x = 1\n   📌 y = test\n",
            output,
        )

    def test_valid_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            __valid_path = Path(tmpdir) / "data.yaml"
            __valid_path.touch()
            self.assertEqual(self.func_with_path(1, __valid_path), f"1, {__valid_path}")

    def test_invalid_path(self):
        __invalid_path = Path("invalid/path/is/here/data.yaml")
        with self.assertRaises(ValueError) as context:
            self.func_with_path(1, __invalid_path)
        self.assertIn(
            "❌ Path 'invalid/path/is/here/data.yaml' does not exist.",
            str(context.exception),
        )

    def test_invalid_path_extension(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            __temp_file = Path(tmpdir) / "data.exe"
            __temp_file.touch()
            with self.assertRaises(ValueError) as context:
                self.func_with_path(1, __temp_file)
            self.assertIn(
                f"❌ File '{__temp_file}' must have a valid extension (.yaml, .json, .txt, .logs).",
                str(context.exception),
            )


if __name__ == "__main__":
    unittest.main()
