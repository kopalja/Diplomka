#!/bin/bash


# 1. parse parameters
# a) model name/path b) all/day/night "c") resolution (this is parsed from .log)
usage(){
    echo "Usage: sysinfo_page [[-n name of model ], [-t type of new dataset {all, day, night}]]"
    exit
}


MODELS_ROOT_DIR="/home/kopi/diplomka/training/output"
TYPE="all"

# parse arguments
while [ "$1" != "" ]; do
    case $1 in
        -n | --name )           
            shift
            MODEL_DIR="${MODELS_ROOT_DIR}/$1"
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

HEIGHT=$(cat "${MODEL_DIR}/model/output_tflite_graph_edgetpu.log" | grep "height:" | sed "s/[a-z]*://g")
WIDTH=$(cat "${MODEL_DIR}/model/output_tflite_graph_edgetpu.log" | grep "width:" | sed "s/[a-z]*://g")


echo ${MODEL_DIR}
echo ${HEIGHT}
echo ${WIDTH}





# 2. generate groung truth







# 3. generate model results

# 4. evaluate model results
