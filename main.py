from value_parser import ValueParser

def main():
    value_parser = ValueParser()
    test_values = [
        "${ env(SHELL) }",
        "${env(SHELL, SHOULD_NOT_PRINT)}",
        "${env(NOTHING, DEFAULT_VALUE_1)}",
        "${ env(NOTHING,DEFAULT_VALUE_2 )}",

        "${ ref(disk/created/properties) }",
        "${ref(disk/created/properties/name)}",
        "${ref(disk/created/properties/size )}",
        "${ ref( disk/created/properties/type ) }",

        "disk/created/properties",
        "disk/created/properties/name",
        "disk/created/properties/size",
        "disk / created/ properties/ type"
    ]

    for value in test_values:
        print(f"{value} -> {value_parser.parse(value)}")
        print(value_parser.pretty_tree(value))


main()