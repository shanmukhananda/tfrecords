import os
import sys
import fnmatch
import json
import logging
import io

''' creates json file which can consumed by create_tfrecords.py
    input: bdd labels folder
    output: tfrecord json file
'''

logging.basicConfig(level=logging.DEBUG)

def area_rectangle(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    return dx * dy

label_map = {}
counter = 0
def label_id(key):
    global label_map
    global counter
    if key not in label_map:
        counter += 1
        label_map[key] = counter
    return label_map[key]

def bdd2tfrecord(infile):
    ''' convert a bdd label file to tfrecord json '''
    img_width = 1280
    img_height = 720
    
    infile_name = os.path.basename(infile)
    image_data = {}
    image_data["filename"] = os.path.splitext(infile_name)[0] + ".jpg"
    image_data["id"] = os.path.splitext(infile_name)[0]

    with open(infile, "r") as read_file:
        data = json.load(read_file)
        frames = data.get("frames", [])
        for frame in frames:
            label = []
            text = []
            xmax = []
            xmin = []
            ymax = []
            ymin = []
            objects = frame["objects"]
            tf_object = {}
            tf_bbx = {}
            
            for object_ in objects:
                if "box2d" in object_: # box2d labels only, poly2d are ignored
                    box = object_["box2d"]
                    x1 = box["x1"]
                    x2 = box["x2"]
                    y1 = box["y1"]
                    y2 = box["y2"]
                    category = object_["category"]
                    
                    xmin.append(x1 / img_width)
                    xmax.append(x2 / img_width)
                    ymin.append(y1 / img_height)
                    ymax.append(y2 / img_height)
                    text.append(category)
                    label.append(label_id(category))

            tf_bbx["label"] = label
            tf_bbx["text"] = text
            tf_bbx["xmax"] = xmax
            tf_bbx["xmin"] = xmin
            tf_bbx["ymax"] = ymax
            tf_bbx["ymin"] = ymin

            tf_object["bbox"] = tf_bbx
            image_data["object"] = tf_object

    return image_data

def log_label_map():
    global label_map
    
    items = []
    for key, value in label_map.iteritems():
        item = "id:{}\nname:'{}'".format(value, key)
        item = "item{\n" + item + "\n}\n"
        items.append(item)

    with open("label_map.pbtxt", "w") as f:
        for pbtext in items:
            f.write(pbtext)

def main(argv):

    assert len(argv) >=3 , "usage: bdd2tfrecord.py bdd_json output_file"
    input_dir = argv[1]
    output_file = argv[2]

    assert os.path.isdir(input_dir), ("{0} is not a valid folder".format(input_dir))

    json_files = fnmatch.filter(os.listdir(input_dir), "*.json")

    tfrecord_list = []
    for file in json_files:
        infile = os.path.join(input_dir, file)
        logging.debug("processing {0}".format(infile))
        tfrecord = bdd2tfrecord(infile)
        tfrecord_list.append(tfrecord)

    logging.debug("saving tfrecord json file {0}".format(output_file))
    with open(output_file, "w") as outfile:
            json.dump(tfrecord_list, outfile, sort_keys=True, indent=4)

    log_label_map()

if __name__ == "__main__":
    main(sys.argv)
