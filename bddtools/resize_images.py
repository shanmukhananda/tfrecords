from PIL import Image
import concurrent.futures
import fnmatch
import logging
import logging
import os
import sys

logging.basicConfig(
    filename="resize_images.log",
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(processName)s:%(process)d:%(threadName)s:%(thread)d:%(filename)s:%(lineno)d:%(funcName)s:%(message)s"
)

def resize(input_path, output_path):

    logging.debug("resizing {0}".format(input_path))
    im = Image.open(infile)
    width, height = im.size
    size = (int(width / 2), int(height / 2))
    out = im.resize(size, Image.ANTIALIAS)
    out.save(outfile, im.format)

def get_data(input_dir, output_dir):
    
    assert os.path.isdir(input_dir), ("{0} is not a valid folder".format(input_dir))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    jpg_files = fnmatch.filter(os.listdir(input_dir), "*.jpg")

    for file in jpg_files:
        infile = os.path.join(input_dir, file)
        outfile = os.path.join(output_dir, file)
        yield (infile, outfile)

def main(argv):

    assert len(argv) == 4, "usage: resize_images.py image_folder output_folder num_threads"
    logging.info("{}".format(argv))

    input_dir = argv[1]
    output_dir = argv[2]
    num_threads = int(argv[3])

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        for infile, outfile in get_data(input_dir, output_dir):
            executor.submit(resize, infile, outfile)

if __name__ == "__main__":
    main(sys.argv)
