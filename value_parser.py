from custom_function import ComplexValue, CustomFunction, ModuleReference

from lark import Lark, Transformer, Token

grammar = r"""
    ?value: function
          | reference

    function : "${" function_name "(" args ")" "}"
    function_name : CNAME
    args : STRING ("," STRING)* | STRING

    reference : module_name "/" resource_name "/" properties
    module_name : CNAME
    resource_name : CNAME
    properties : CNAME ("/" CNAME)* | CNAME

    STRING : /[^ \t\f\r\n\(\),]+/

    %import common.CNAME
    %import common.WS
    %ignore WS

"""


class ValueTransformer(Transformer):
    def reference(self, items: list[list[Token]]) -> ModuleReference:
        return ModuleReference(
            module_name=items[0][0].value,
            resource_name=items[1][0].value,
            property_reference_list=[item.value for item in items[2]],
        )

    def function(self, items: list[list[Token]]) -> CustomFunction:
        return CustomFunction(
            function_name=items[0][0].value, arguments=[item.value for item in items[1]]
        )

    def function_name(self, name: list[Token]):
        return name

    def args(self, items: list[Token]):
        return list(items)

    def module_name(self, name: list[Token]):
        return name

    def resource_name(self, name: list[Token]):
        return name

    def properties(self, properties: list[Token]):
        return list(properties)


class ValueParser:
    def __init__(self) -> None:
        self.lark = Lark(grammar, start="value")
        self.value_transformer = ValueTransformer()

    def parse(self, value: str) -> str:
        return self.transform(value).parse()

    def transform(self, value: str) -> ComplexValue:
        return self.value_transformer.transform(self.lark.parse(value))

    def pretty_tree(self, value: str) -> str:
        return self.lark.parse(value).pretty()
