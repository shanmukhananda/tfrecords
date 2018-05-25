class TFRecordClass(object):

    __slots__ = ["label", "text", "conf"]

    def __init__(self):
        self.label = 0
        self.text = ""
        self.conf = 0.0

    def as_dict(self):
        ret = {}
        ret["label"] = self.label
        ret["text"] = self.text
        ret["conf"] = self.conf
        return ret

class TFRecordObjectBBox(object):

    __slots__ = ["conf", "label", "score", "text", "xmax", "xmin", "ymax", "ymin"]

    def __init__(self):
        self.conf = []
        self.label = []
        self.score = []
        self.text = []
        self.xmax = []
        self.xmin = []
        self.ymax = []
        self.ymin = []

    def as_dict(self):
        ret = {}
        ret["conf"] = self.conf
        ret["label"] = self.label
        ret["score"] = self.score
        ret["text"] = self.text
        ret["xmax"] = self.xmax
        ret["xmin"] = self.xmin
        ret["ymax"] = self.ymax
        ret["ymin"] = self.ymin
        return ret

class TFRecordObject(object):

    __slots__ = ["count", "area", "id", "bbox"]

    def __init__(self):
        self.count = 0
        self.area = []
        self.id = []
        self.bbox = TFRecordObjectBBox()

    def as_dict(self):
        ret = {}
        ret["count"] = self.count
        ret["area"] = self.area
        ret["id"] = self.id
        ret["bbox"] = self.bbox.as_dict()
        return ret

class TFRecordParts(object):

    __slots__ = ["x", "y", "v", "score"]

    def __init__(self):
        self.x = []
        self.y = []
        self.v = []
        self.score = []

    def as_dict(self):
        ret = {}
        ret["x"] = self.x
        ret["y"] = self.y
        ret["v"] = self.v
        ret["score"] = self.score
        return ret

class TFRecord(object):

    __slots__ = ["filename", "id", "iclass", "object", "parts"]

    def __init__(self):
        self.filename = ""
        self.id = ""
        self.iclass = TFRecordClass()
        self.object = TFRecordObject()
        self.parts = TFRecordParts()

    def as_dict(self):
        ret = {}
        ret["filename"] = self.filename
        ret["id"] = self.id
        ret["class"] = self.iclass.as_dict()
        ret["object"] = self.object.as_dict()
        ret["parts"] = self.parts.as_dict()
        return ret

if __name__ == "__main__":
    rec = TFRecord()
    print(rec.as_dict())
