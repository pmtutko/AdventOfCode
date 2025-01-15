import itertools

class Point:
    id_gen = itertools.count()

    def __init__(self):
        this_id = next(self.id_gen)
        self.r = this_id
        self.c = this_id

    def __str__(self):
        return f'({self.r}, {self.c})'


class someClass:
    def __init__(self):
        self.list = []

    def add(self, item):
        self.list.append(item)

    def __iter__(self):
        for x in self.list:
            yield x


pts = someClass()

for i in range(5):
    pts.add(Point())
for p in pts:
    print(p)
