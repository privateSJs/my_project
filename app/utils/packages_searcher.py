import os
import ast


class PackagesSearcher:
    def __init__(self, framework_name, directory, framework_short_cut="np"):
        self.file_path = ""
        self.directory = directory
        self.framework_name = framework_name
        self.framework_short_cut = framework_short_cut
        self.found_packages = []

    def is_node_install(self):
        try:
            import self.node
        except ImportError:
            raise ImportError("Framework is not installed at this project.")

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
        with open(self.file_path, "r", encoding="utf-8") as file:
            tree = ast.parse(file.read(), filename=self.file_path)

        package_is_here = False
        for node in ast.walk(tree):
            func_name = self.is_node_function(node=node)
            if func_name:
                package_is_here = True
                self.found_packages.append((self.file_path, node.lineno, func_name))
                print(
                    f"Found in {self.file_path} | Line - {node.lineno} | Function- {func_name}"
                )

        if not package_is_here:
            print(f"In current module {self.file_path} framework does not exist.")

    def scan_project(self):
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.endswith(".py"):
                    self.file_path = os.path.join(root, file)
                    try:
                        self.analyze_file()
                    except Exception as e:
                        print(f"❌ Error during analyze {self.file_path}")


if __name__ == "__main__":
    FRAMEWORK_NAME = "pandas"
    DIRECTORY = "/home/jarek9917/Dokumenty/MasterDegree/my_project/app/utils"
    SHORT_CUT = ""
    ## Instance of package searcher
    packages_searcher = PackagesSearcher(
        framework_name=FRAMEWORK_NAME,
        directory=DIRECTORY,
        framework_short_cut=SHORT_CUT,
    )
    packages_searcher.scan_project()
