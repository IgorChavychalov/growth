def valid_year(value: str):
    if not len(value) == 4:
        return 0
    else:
        try:
            for elem in value:
                int(elem)
        except Exception as e:
            return 0
        return 1
