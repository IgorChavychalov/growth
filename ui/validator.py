def validate_create_form(line_list: list) -> list:
    valid_list = []
    for i in range(6):
        valid_list
        if i > 1:
            valid_year(line_list[i])
    return


def valid_year(value: str):
    if value is None:
        return None
    if len(value) != 4:
        return 0
    else:
        try:
            for elem in value:
                int(elem)
        except Exception as e:
            return 0
        return int(value)

def serialization_create_form_date(input_date: list):
