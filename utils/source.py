class Source:
    def __init__(self, sx, sz, sourcefx, sourcefz):
        self.sx = sx
        self.sz = sz
        self.sfx = sourcefx
        self.sfz = sourcefz

    def getXResponse(self, t):
        return self.sfx(t)

    def getZResponse(self, t):
        return self.sfz(t)