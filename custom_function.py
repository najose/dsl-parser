import os


class ComplexValue:
    def parse(self) -> str:
        return ""


class ModuleReference(ComplexValue):
    def __init__(
        self, module_name: str, resource_name: str, property_reference_list: list[str]
    ):
        self.module_name = module_name
        self.resource_name = resource_name
        self.property_reference_list = property_reference_list

    def parse(self) -> str:
        return f"{self.module_name}.{self.resource_name}.{'.'.join(self.property_reference_list)}"


class CustomFunction(ComplexValue):
    def __init__(self, function_name: str, arguments: list[str]):
        self.function_name = function_name
        self.arguments = arguments
        self.n_args = len(arguments)

    def parse(self) -> str:
        try:
            implementation = getattr(CustomFunctions, self.function_name)
            return implementation(self)
        except AttributeError as e:
            raise RuntimeError(
                f'Could not find implementation for the function "{self.function_name}".'
            ) from e


class CustomFunctions:
    @staticmethod
    def ref(custom_function: CustomFunction) -> str:
        if custom_function.n_args != 1:
            raise RuntimeError("Expected single argument.")

        return ".".join(custom_function.arguments[0].split("/"))

    @staticmethod
    def env(custom_function: CustomFunction) -> str:
        if 1 < custom_function.n_args > 2:
            raise RuntimeError(
                "Expected at at least 1 argument and maximum of 2 arguments."
            )

        env_var_value = os.getenv(custom_function.arguments[0])
        if env_var_value is None:
            if custom_function.n_args == 2:
                # Default value
                return custom_function.arguments[1]

            raise RuntimeError(
                f'The environment variable "{custom_function.arguments[0]}" is not set.'
            )

        return env_var_value
