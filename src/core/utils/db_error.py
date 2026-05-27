import re


def parse_integrity_error(err) -> str:
    error_cause = str(err.__cause__.args[0])
    lines = error_cause.split("\n")
    for line in lines:
        if "FOREIGN KEY" in line or "foreign key" in line.lower():
            match = re.search(r"\((\w+)_id\)", line)
            if match:
                return match.group(1) + "_id"
        elif "UNIQUE constraint failed" in line:
            field = line.split(".")[-1]
            return field
    return "unknown"
