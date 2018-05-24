#!/bin/bash

script_dir=$(realpath $(dirname $0))
project_dir=$(realpath ${script_dir}/..)

cd ${project_dir}/tests

python ${project_dir}/create_tfrecords.py --dataset_path train_cat.json --prefix train --output_dir ${project_dir}/tests --shards 1 --threads 1 --store_images

cd ${project_dir}
