import re


def parse_null(input_string):
    data = re.search("^null", input_string)
    if data is None:
        return None
    return None, input_string[4:]


def parse_bool(input_string):
    data = re.search("^(true|false)", input_string)
    if data:
        if data[0][0] == "t":
            return True, input_string[4:]
        return False, input_string[5:]
    return None


def parse_number(input_string):
    scientific_float_pattern = (
        "^([-]?((([1-9]([0-9]*)|0)[.][0-9]+)((e|E)[-+]?[0-9]+)?))"
    )
    data = re.search(scientific_float_pattern, input_string)
    if data is not None:
        final_output = float(data[0])
        return final_output, input_string[len(data[0]) :]
    scientific_integer_pattern = "^([-]?(([1-9][0-9]*|0)((e|E)[-+]?[0-9]+)?))"
    data = re.search(scientific_integer_pattern, input_string)
    if data is None:
        return None
    if "e" in data[0] or "E" in data[0]:
        final_output = float(data[0])
        return final_output, input_string[len(data[0]) :]
    final_output = int(data[0])
    return final_output, input_string[len(data[0]) :]


def parse_string(input_string):
    pattern = '^"([^"\\\\\x00-\x1f\x7f-\x9f]|(\\\\(b|n|t|\\\\|"|r|f))|(\\\\u[a-fA-F0-9]{4}))*"'
    data = re.search(pattern, input_string)
    if data is not None:
        output = (data[0])[1:-1]
        if "\\" in output:
            fin_output = output.encode().decode("unicode_escape")
            return fin_output, input_string[len(data[0]) :]
        return output, input_string[len(data[0]) :]
    return None


def parse_value(input_string):
    parsers = (
        parse_null,
        parse_bool,
        parse_number,
        parse_string,
        parse_array,
        parse_object,
    )
    for parser in parsers:
        output = parser(input_string)
        if output is not None:
            return output
    return None


def parse_array(input_string):
    if input_string[0] != "[" or input_string[0:2] == "[,":
        return None
    input_string = input_string[1:]
    output_array = []
    while input_string[0] != "]":
        input_string = input_string.lstrip()
        if parse_value(input_string) is not None:
            output_array.append(parse_value(input_string)[0])
            input_string = parse_value(input_string)[1]
        else:
            return None
        input_string = input_string.lstrip()
        if input_string[0] == ",":
            if input_string[1] == "," or input_string[1] == "]":
                return None
            input_string = input_string[1:]
            continue
        elif input_string[0] == "]":
            break
        return None
    return output_array, input_string[1:]


def parse_object(input_string):
    if input_string[0] != "{" or input_string[0:2] == "{,":
        return None
    input_string = input_string[1:]
    output_object = {}
    while input_string[0] != "}":
        input_string = input_string.lstrip()
        key_string = parse_string(input_string)
        if key_string is None:
            return None
        parsed_key = key_string[0]
        input_string = key_string[1]
        input_string = input_string.lstrip()
        if input_string[0] != ":":
            return None
        else:
            if (
                input_string[1] == ":"
                or input_string[1] == ","
                or input_string[1] == "}"
            ):
                return None
            input_string = input_string[1:]
        input_string = input_string.lstrip()
        output_object[parsed_key] = parse_value(input_string)[0]
        input_string = parse_value(input_string)[1]
        input_string = input_string.lstrip()
        if input_string[0] == ",":
            if input_string[1] == "," or input_string[1] == "}":
                return None
            input_string = input_string[1:]
            continue
        elif input_string[0] == "}":
            break
        return None
    return output_object, input_string[1:]


def parse_json(input_string):
    output = parse_value(input_string)
    if output is not None:
        if output[1] == "":
            return output[0]
        return None
    return None
