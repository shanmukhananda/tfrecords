#!/bin/bash

script_dir=$(realpath $(dirname $0))
project_dir=$(realpath ${script_dir}/..)

dataset_json=${project_dir}/bddtools/result_tfrecord.json

bdd_images_dir=${project_dir}/bddtools/tests/resized_images
bdd_labels_dir=${project_dir}/bddtools/tests/labels
tfrecord_json_out=${project_dir}/bddtools/tests/results_tfrecord.json

python ${project_dir}/bddtools/bdd2tfrecord.py ${bdd_labels_dir} ${tfrecord_json_out}

output_dir=${project_dir}/bddtools/tests/train_results
mkdir -p ${output_dir}

cd ${bdd_images_dir}

python ${project_dir}/create_tfrecords.py \
--dataset_path ${tfrecord_json_out} \
--prefix train \
--output_dir ${output_dir} \
--shards 1 \
--threads 1 \
--store_images

cd ${project_dir}
