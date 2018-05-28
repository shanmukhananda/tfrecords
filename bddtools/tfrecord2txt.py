import tensorflow as tf
import sys

def print_tfrecord(path):
    for example in tf.python_io.tf_record_iterator(path):
        result = tf.train.Example.FromString(example)
        print(result)

def main(argv):
    assert len(argv) == 2, "usage: tfrecord2txt.py tfrecord"
    tfrecord_file = argv[1]
    print_tfrecord(tfrecord_file)

if __name__ == "__main__":
    main(sys.argv)
