import json


class JsonParser:
    def __init__(self, json_text):
        self._json_text = json_text
        self._json_handler = None

    def __enter__(self):
        self._json_handler = json.loads(self._json_text)
        return json.loads(self._json_text)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rectangle:
    def __init__(self, point_a, point_b):
        self._start_point = point_a
        self._end_point = point_b

    def contains(self, point):
        if (self._inbetween(self._start_point.x, self._end_point.x, point.x) and
                self._inbetween(self._start_point.y, self._end_point.y, point.y)):
            return True
        return False

    def _inbetween(self, a, b, c):
        if (a <= c <= b) or (b <= c <= a):
            return True
        return False


if __name__ == '__main__':
    with JsonParser('"hello"') as res:
        assert res == "hello"

    with JsonParser('{"hello": "world", "key": [1,2,3]}') as res:
        assert res == {"hello": "world", "key": [1, 2, 3]}

    start_point = Point(1, 0)
    end_point = Point(7, 3)

    rect = Rectangle(start_point, end_point)
    assert rect.contains(start_point)
    assert not rect.contains(Point(-1, 3))
    assert rect.contains(Point(1, 3))
