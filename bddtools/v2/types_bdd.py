
class BDDObjectAttributes(object):

    __slots__ = ["occluded", "truncated", "trafficLightColor"]

    def __init__(self):
        self.occluded = False
        self.truncated = False
        self.trafficLightColor = ""

    def read(self, input):
        self.occluded = input.get("occluded", False)
        self.truncated = input.get("truncated", False)
        self.trafficLightColor = input.get("trafficLightColor", "")

    def as_dict(self):
        ret = {}
        ret["occluded"] = self.occluded
        ret["truncated"] = self.truncated
        ret["trafficLightColor"] = self.trafficLightColor
        return ret

class BDDObjectBox2D(object):

    __slots__ = ["x1", "y1", "x2", "y2"]

    def __init__(self):
        self.x1 = 0.0
        self.y1 = 0.0
        self.x2 = 0.0
        self.y2 = 0.0
    
    def read(self, input):
        self.x1 = input.get("x1", 0.0)
        self.y1 = input.get("y1", 0.0)
        self.x2 = input.get("x2", 0.0)
        self.y2 = input.get("y2", 0.0)

    def as_dict(self):
        ret = {}
        ret["x1"] = self.x1
        ret["y1"] = self.y1
        ret["x2"] = self.x2
        ret["y2"] = self.y2
        return ret

class BDDObject(object):

    __slots__ = ["category", "id", "attributes", "box2d", "poly2d"]

    def __init__(self):
        self.category = ""
        self.id = 0
        self.attributes = BDDObjectAttributes()
        self.box2d = BDDObjectBox2D()
        self.poly2d = []

    def has_box2d(self):
        pass

    def read(self, input):
        self.category = input.get("category", "")
        self.id = input.get("id", 0)
        attributes = input.get("attributes", {})
        self.attributes.read(attributes)
        box2d = input.get("box2d", {})
        self.box2d.read(box2d)

        if "poly2d" in input:
            poly2d = input.get("poly2d", [])
            for point in poly2d:
                self.poly2d.append(point)

    def as_dict(self):
        ret = {}
        ret["category"] = self.category
        ret["id"] = self.id
        ret["attributes"] = self.attributes.as_dict()
        ret["box2d"] = self.box2d.as_dict()
        ret["poly2d"] = []
        for point in self.poly2d:
            ret["poly2d"].append(point)

        return ret

class BDDAttributes(object):

    __slots__ = ["weather", "scene", "timeofday"]

    def __init__(self):
        self.weather = ""
        self.scene = ""
        self.timeofday = ""

    def read(self, input):
        self.weather = input.get("weather", "")
        self.scene = input.get("scene", "")
        self.timeofday = input.get("timeofday", "")

    def as_dict(self):
        ret = {}
        ret["weather"] = self.weather
        ret["scene"] = self.scene
        ret["timeofday"] = self.timeofday
        return ret

class BDDFrame(object):

    __slots__ = ["timestamp", "objects"]

    def __init__(self):
        self.timestamp = 0
        self.objects = []

    def read(self, input):
        self.timestamp = input.get("timestamp", 0)
        objects = input.get("objects", [])

        for object_ in objects:
            obj = BDDObject()
            obj.read(object_)
            self.objects.append(obj)

    def as_dict(self):
        ret = {}
        ret["timestamp"] = self.timestamp
        ret["objects"] = []
        for object_ in self.objects:
            ret["objects"].append(object_.as_dict())
        return ret

class BDDData(object):
    
    __slots__ = ["name", "frames", "attributes"]

    def __init__(self):
        self.name = ""
        self.frames = []
        self.attributes = BDDAttributes()

    def read(self, input):
        self.name = input.get("name", "")
        frames = input.get("frames", [])
        for frame in frames:
            f = BDDFrame()
            f.read(frame)
            self.frames.append(f)
        attributes = input.get("attributes", {})
        self.attributes.read(attributes)

    def as_dict(self):
        ret = {}
        ret["name"] = self.name
        ret["frames"] = []
        for frame in self.frames:
            ret["frames"].append(frame.as_dict())
        ret["attributes"] = self.attributes.as_dict()
        return ret

if __name__ == "__main__":
    data = BDDData()
    obj = BDDObject()
    print(data.as_dict())
    print(obj.as_dict())
