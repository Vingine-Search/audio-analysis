# These lines makes tensorflow able to use the GPU.
CUDNN_PATH=$(dirname $(python -c "import nvidia.cudnn;print(nvidia.cudnn.__file__)"))
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$CUDNN_PATH/lib"