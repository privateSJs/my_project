import functools
import inspect
from pathlib import Path


def validate_args(debug=False):
    """
    Arguments validation decorator basing type annotations
    Check variable type and if string is not empty
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Set function annotations
            annotations = func.__annotations__  # Collection annotations from func

            # Passed signature
            sig = inspect.signature(func)

            # Passed signature list parameters
            parameters = list(sig.parameters.keys())

            # Check if func have "self"
            is_method = parameters and parameters[0] == "self"

            # Collection defined value of args
            args_names = parameters[1:] if is_method else parameters

            # Create dictionary of passed arguments
            passed_args = dict(zip(args_names, args[1:] if is_method else args))

            # Adding arguments defined as kwargs
            passed_args.update(kwargs)

            # Checking default variable values
            default_values = func.__defaults__ or ()

            # Create arguments dictionary with default defines value
            default_args = dict(zip(args_names[-len(default_values) :], default_values))

            # Connect passed value and default values
            for arg_name in args_names:
                if arg_name not in passed_args:
                    passed_args[arg_name] = default_args.get(arg_name)

            # DEBUG: Show all function arguments
            if debug:
                print(f"\n🔍 Debug: Executed `{func.__name__}")
                for arg_name, value in passed_args.items():
                    print(f"   📌 {arg_name} = {value}")

            # Variable validation
            for var_name, expected_type in annotations.items():
                if var_name == "return":
                    continue

                value = passed_args.get(var_name)

                if value is None:
                    raise ValueError(f"Argument '{var_name}' cannot be None.")

                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"Argument '{var_name}' must be {expected_type.__name__}, "
                        f"but got {type(value).__name__}."
                    )

                if isinstance(value, str) and not value.strip():
                    raise ValueError(f"Argument '{var_name}' cannot be empty or None.")

                if isinstance(value, Path):
                    if not value.exists():
                        raise ValueError(f"❌ Path '{value}' does not exist.")
                    if value.is_file() and value.suffix not in [
                        ".yaml",
                        ".json",
                        ".txt",
                        ".logs",
                    ]:
                        raise ValueError(
                            f"❌ File '{value}' must have a valid extension (.yaml, .json, .txt, .logs)."
                        )

            return func(*args, **kwargs)

        return wrapper

    return decorator
