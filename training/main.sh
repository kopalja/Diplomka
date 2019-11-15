#!/bin/bash

# Exit script on error.
set -e
# Echo each command, easier for debugging.
set -x

# keep only tensorboard data
delete_train_files(){   
    for NAME in $1/*; do
        if [ "$(basename $NAME)" != "eval_0" ]; then
            rm -r "${NAME}";
        fi
    done
}

# keep only final edge_tpu model(and log)
delete_model_files(){
    for NAME in $1/*; do
        if [ "$(basename $NAME)" != "output_tflite_graph_edgetpu.tflite" ] && [ "$(basename $NAME)" != "output_tflite_graph_edgetpu.log" ]; then
            rm "${NAME}";
        fi
    done 
}

copy_model_into_obj_api(){
    TYPE=$(cat "$1/pipeline.config" | grep "type:" | sed 's/[a-z]*: \"//g' | sed 's/\"//g' | sed 's/\s//g')
    ARCHITECTURE_DIR="$2/${TYPE}"
    #copy model to obj API
    cp "${ARCHITECTURE_DIR}/model.ckpt.data-00000-of-00001" "model.ckpt.data-00000-of-00001"
    cp "${ARCHITECTURE_DIR}/model.ckpt.index" "model.ckpt.index"
    cp "${ARCHITECTURE_DIR}/model.ckpt.meta" "model.ckpt.meta" 
}

# set variables 
DATASET="batch_1_day"
INPUT_TENSORS='normalized_input_image_tensor'
OUTPUT_TENSORS='TFLite_Detection_PostProcess,TFLite_Detection_PostProcess:1,TFLite_Detection_PostProcess:2,TFLite_Detection_PostProcess:3'

cd "${LOCAL_GIT}/object_detection_api/"
#source "/home/kopi/tools/enviroments/tf_gpu/bin/activate"

for CKPT_DIR in ~/diplomka/training/configs/configs_to_process/*/ ; do


    echo "CONVERTING dataset to TF Record..."
    python object_detection/dataset_tools/create_pet_tf_record2.py \
        --data_dir="${LOCAL_GIT}/dataset/exported/${DATASET}" \
        --output_dir="${LOCAL_GIT}/dataset/exported/tf_records"

    echo "tf records done"

    CKPT_NAME="$(basename $CKPT_DIR)"
    OUTPUT_I="${PROJECT_ROOT}/training/output/${CKPT_NAME}"
    if [ -d "${OUTPUT_I}" ]; then rm -Rf ${OUTPUT_I}; fi
    mkdir "${OUTPUT_I}"



    copy_model_into_obj_api "${CKPT_DIR}" "${HOME}/local_git/architectures"

    TRAIN_DIR="${OUTPUT_I}/train"
    echo "Start training..."
    num_training_steps=11000
    num_eval_steps=2000
    python object_detection/model_main.py \
        --pipeline_config_path="${CKPT_DIR}/pipeline.config" \
        --model_dir="${TRAIN_DIR}" \
        --num_train_steps="${num_training_steps}" \
        --num_eval_steps="${num_eval_steps}"




    MODEL_DIR="${OUTPUT_I}/model"
    ckpt_number=${num_training_steps}
    echo "EXPORTING frozen graph from checkpoint..."
    python object_detection/export_tflite_ssd_graph.py \
        --pipeline_config_path="${CKPT_DIR}/pipeline.config" \
        --trained_checkpoint_prefix="${TRAIN_DIR}/model.ckpt-${ckpt_number}" \
        --output_directory="${MODEL_DIR}" \
        --add_postprocessing_op=true


    # Parse width and height from pipeline.config file
    HEIGHT=$(cat "${CKPT_DIR}/pipeline.config" | grep "height:" | sed "s/[a-z]*://g")
    WIDTH=$(cat "${CKPT_DIR}/pipeline.config" | grep "width:" | sed "s/[a-z]*://g")

    echo "CONVERTING frozen graph to TF Lite file..."
    tflite_convert \
        --output_file="${MODEL_DIR}/output_tflite_graph.tflite" \
        --graph_def_file="${MODEL_DIR}/tflite_graph.pb" \
        --inference_type=QUANTIZED_UINT8 \
        --input_arrays="${INPUT_TENSORS}" \
        --output_arrays="${OUTPUT_TENSORS}" \
        --mean_values=128 \
        --std_dev_values=128 \
        --input_shapes=1,"${HEIGHT}","${WIDTH}",3 \
        --change_concat_input_ranges=false \
        --allow_nudging_weights_to_use_fast_gemm_kernel=true \
        --allow_custom_ops

    # Compile model for edge tpu
    edgetpu_compiler "${MODEL_DIR}/output_tflite_graph.tflite" -o "${MODEL_DIR}"

    # Delete all unnessesary model files
    delete_train_files "${TRAIN_DIR}"
    delete_model_files "${MODEL_DIR}"

    echo "---Additional informations---" >> "${MODEL_DIR}/output_tflite_graph_edgetpu.log"
    echo "width: ${WIDTH}" >> "${MODEL_DIR}/output_tflite_graph_edgetpu.log"
    echo "height: ${HEIGHT}" >> "${MODEL_DIR}/output_tflite_graph_edgetpu.log"

done


