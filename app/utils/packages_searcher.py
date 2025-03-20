import os
import ast
import importlib


class PackagesSearcher:
    def __init__(self, framework_name, directory, ignore_option, framework_short_cut):
        self.file_path = ""
        self.directory = directory
        self.framework_name = framework_name
        self.framework_short_cut = (
            framework_short_cut if framework_short_cut else framework_name
        )
        self.found_results = []
        self.ignore_option = ignore_option

    def is_node_install(self):
        try:
            importlib.import_module(self.framework_name)
        except ImportError:
            raise ImportError(
                f"Framework {self.framework_name} is not installed in the project."
            )

    def is_import_statement(self, node):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == self.framework_name:
                    return f"import {alias.name}"
        elif isinstance(node, ast.ImportFrom):
            if node.module == self.framework_name:
                return (
                    f"from {node.module} import {', '.join(a.name for a in node.names)}"
                )
        return None

    def is_node_function(self, node):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute) and isinstance(
                node.func.value, ast.Name
            ):
                if (
                    node.func.value.id == self.framework_short_cut
                    or node.func.value.id == self.framework_name
                ):
                    return node.func.attr
        return None

    def analyze_file(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                tree = ast.parse(file.read(), filename=self.file_path)
        except SyntaxError as err:
            print(f"❌ Syntax error in {self.file_path}: {err}")
            return

        package_found = False

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == self.framework_name:
                        import_statement = f"import {alias.name}"
                        self.found_results.append(
                            (self.file_path, node.lineno, import_statement)
                        )
                        print(
                            f"📦 Import found in {self.file_path} | Line {node.lineno} | {import_statement}"
                        )
                        package_found = True

            elif isinstance(node, ast.ImportFrom):
                if node.module == self.framework_name:
                    import_statement = f"from {node.module} import {', '.join(a.name for a in node.names)}"
                    self.found_results.append(
                        (self.file_path, node.lineno, import_statement)
                    )
                    print(
                        f"📦 Import found in {self.file_path} | Line {node.lineno} | {import_statement}"
                    )
                    package_found = True

            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute) and isinstance(
                    node.func.value, ast.Name
                ):
                    if (
                        node.func.value.id == self.framework_short_cut
                        or node.func.value.id == self.framework_name
                    ):
                        func_name = node.func.attr
                        self.found_results.append(
                            (self.file_path, node.lineno, func_name)
                        )
                        print(
                            f"✅ Function found in {self.file_path} | Line {node.lineno} | {func_name}"
                        )
                        package_found = True

        if not package_found:
            print(f"🔍 No framework usage found in {self.file_path}.")

    def scan_project(self):
        for root, dirs, files in os.walk(self.directory):
            dirs[:] = [d for d in dirs if d not in self.ignore_option]
            for file in files:
                if file.endswith(".py"):
                    self.file_path = os.path.join(root, file)
                    try:
                        self.analyze_file()
                    except Exception as err:
                        print(f"❌ Error during analyze {self.file_path} with {err}")


if __name__ == "__main__":
    # Configure here your searcher, add here your virtual environments or files to ignore
    IGNORE_FILES = ["venv", ".venv"]

    # Configure here your framework name for example "pandas", "numpy" etc.
    FRAMEWORK_NAME = "numpy"

    # Configure here your project directory -> what u want to be scanning
    DIRECTORY = "/home/jarek9917/Dokumenty/MasterDegree/my_project"

    # Optional give here short-cut name, for example for pandas usually we use "pd"
    # For Numpy we use "np"
    SHORT_CUT = "np"

    ## Instance of package searcher
    packages_searcher = PackagesSearcher(
        framework_name=FRAMEWORK_NAME,
        directory=DIRECTORY,
        ignore_option=IGNORE_FILES,
        framework_short_cut=SHORT_CUT,
    )

    # Check is framework is installed
    try:
        packages_searcher.is_node_install()
    except ImportError as e:
        print(f"⚠️ {e}")
        exit(1)

    packages_searcher.scan_project()
