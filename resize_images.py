from __future__ import print_function

import os
import sys
import fnmatch
from PIL import Image

def main(argv):

    assert len(argv) >=3, "usage: resize_images.py image_folder output_folder"

    input_dir = argv[1]
    output_dir = argv[2]

    assert os.path.isdir(input_dir), ("{0} is not a valid folder".format(input_dir))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    jpg_files = fnmatch.filter(os.listdir(input_dir), "*.jpg")

    for file in jpg_files:
        infile = os.path.join(input_dir, file)
        outfile = os.path.join(output_dir, file)
        try :
            im = Image.open(infile)
            width, height = im.size
            size = (width / 2, height / 2)
            out = im.resize(size, Image.ANTIALIAS)
            out.save(outfile, "jpeg")
        except IOError:
            print("cannot reduce image for ", infile)

if __name__ == "__main__":
    main(sys.argv)
