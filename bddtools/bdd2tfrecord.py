import os
import sys
import fnmatch
import json
import logging

''' creates json file which can consumed by create_tfrecords.py
    input: bdd labels folder
    output: tfrecord json file
'''

logging.basicConfig(level=logging.DEBUG)

def area_rectangle(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    return dx * dy

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
            area = []
            conf = []
            label = []
            score = []
            text = []
            xmax = []
            xmin = []
            ymax = []
            ymin = []
            ids = []
            objects = frame.get("objects", [])
            tf_object = {}
            tf_bbx = {}
            box_obj_cnt = 0
            
            for object_ in objects:
                if "box2d" in object_: # box2d labels only, poly2d are ignored
                    box_obj_cnt += 1   
                    box = object_.get("box2d", [])
                    x1 = box.get("x1")
                    x2 = box.get("x2")
                    y1 = box.get("y1")
                    y2 = box.get("y2")
                    category = object_.get("category", "")
                    obj_id = object_.get("id")
                    
                    obj_area = area_rectangle(x1, y1, x2, y2) / (img_width * img_height)
                    area.append(obj_area)
                    xmin.append(x1 / img_width)
                    xmax.append(x2 / img_width)
                    ymin.append(y1 / img_height)
                    ymax.append(y2 / img_height)
                    text.append(category)
                    ids.append(obj_id)
                    label.append(obj_id)

            tf_bbx["conf"] = conf
            tf_bbx["label"] = label
            tf_bbx["score"] = score
            tf_bbx["text"] = text
            tf_bbx["xmax"] = xmax
            tf_bbx["xmin"] = xmin
            tf_bbx["ymax"] = ymax
            tf_bbx["ymin"] = ymin

            tf_object["count"] = box_obj_cnt
            tf_object["area"] = area
            tf_object["id"] = ids
            tf_object["bbox"] = tf_bbx
            image_data["object"] = tf_object

    return image_data

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

if __name__ == "__main__":
    main(sys.argv)
