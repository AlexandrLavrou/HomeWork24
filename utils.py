import os

from typing import Iterable, Iterator, Generator, List, Any, Union

from werkzeug.exceptions import BadRequest


def iter_limit(data: Iterable, limit: int) -> Iterator:
    i: int = 0
    for item in data:
        if i < limit:
            yield item
        else:
            break
        i += 1


def query_maker(cmd: str, value: str, data: list) -> list:

    mapped_data = map(lambda v: v.strip(), data)

    if cmd == "unique":
        result = list(set(mapped_data))
    elif cmd == "filter":
        result = list(filter(lambda x: value in x, mapped_data))
    elif cmd == "map":
        result = list(map(lambda x: x.split(' ')[int(value)], mapped_data))
    elif cmd == "limit":
        result = list(iter_limit(mapped_data, int(value)))
    elif cmd == "sort":
        result = list(sorted(mapped_data, reverse=True if value == "desc" else False))
    else:
        BadRequest("Введен неверный запрос!")

    return result


def get_cmd(query: dict) -> Generator:
    del query["file_name"]
    buf: List[str] = []
    # buf = (item for item in query.values() if len(buf) == 2)
    for item in query.values():
        buf.append(item)
        if len(buf) == 2:
            yield buf
            buf = []


def do_query(data: Union[list, Any], items: Generator) -> list:
    result = data
    for cmd, value in items:
        result = query_maker(cmd, value, result)
    return result


def get_result(path: str, file_name: str, chunk: Generator) -> list:
    with open(os.path.join(path, file_name)) as f:
        return do_query(f, chunk)
