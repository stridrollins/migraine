class Circuit:
    def __init__(self, name, location, length):
        self.name = name
        self.location = location
        self.length = length

        self.segments = []
class Segment:
    def __init__(self, start, end, type, value=0):
        self.start = start      # en mètres
        self.end = end
        self.type = type        # "plat", "uphill", "downhill", "turn"
        self.value = value      # pente (%) ou rayon du virage


