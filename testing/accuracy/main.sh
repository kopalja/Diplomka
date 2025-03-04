#!/bin/bash


# 1. parse parameters
# a) model name/path b) all/day/night "c") resolution (this is parsed from .log)
usage(){
    echo "Usage: sysinfo_page [[-n name of model ], [-t type of new dataset {all, day, night}]]"
    exit
}


MODELS_ROOT_DIR="${PROJECT_ROOT}/training/output"
TYPE="all"

# 0. parse arguments
if [ "$1" = "" ]; then usage; fi
while [ "$1" != "" ]; do
    case $1 in
        -n | --name )           
            shift
            MODEL_DIR="${MODELS_ROOT_DIR}/$1/model"
            if [ ! -d "${MODEL_DIR}" ]; then
                echo "Folder ${MODEL_DIR} doesn't exist."
                exit
            fi
            ;;
        # test type
        -t | --type ) 
            shift 
            if [ "$1" != "all" ] && [ "$1" != "day" ] && [ "$1" != "night" ]; then
                usage
            fi  
            TYPE=$1
            ;;
        -h | --help )           
            usage
            ;;
        * )                     
            usage
    esac
    shift
done


# 1. set variables
HEIGHT=$(cat "${MODEL_DIR}/output_tflite_graph_edgetpu.log" | grep "height:" | sed "s/[a-z]*://g")
WIDTH=$(cat "${MODEL_DIR}/output_tflite_graph_edgetpu.log" | grep "width:" | sed "s/[a-z]*://g")
TESTING_DIR=$(echo "${LOCAL_GIT}/testing/exported/${TYPE}_${WIDTH}x${HEIGHT}" | sed 's/ //g')
ORIGIN=$(cat "${MODEL_DIR}/output_tflite_graph_edgetpu.log" | grep "origin:" | sed "s/[a-z]*://g" | sed 's/ //g')



# 2. generate groung truth
if [ -d "${TESTING_DIR}" ]; then 
    echo 'Ground truth already exist'
else
    echo 'Generating new ground truth testing set'
    python generate_ground_truth.py --type ${TYPE} --width ${WIDTH} --height ${HEIGHT}
fi



# 3. generate model results
echo "Generating model results..."
python generate_model_results.py \
    --model_path="${MODEL_DIR}/output_tflite_graph_edgetpu.tflite" \
    --testing_data="${TESTING_DIR}" \
    --origin="${ORIGIN}"


echo "${TESTING_DIR}"
# 4. evaluate model results
echo "Evaluating model results..."
python evaluate_results.py \
    --ground_truth="${TESTING_DIR}"


rm -rf "${PROJECT_ROOT}/testing/accuracy/model_detection_txts"
