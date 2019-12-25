export IMAGE_SIZE=224  
export ARCHITECTURE="mobilenet_0.50_${IMAGE_SIZE}" 

#Useful Commands
Create conda env: 
condo create -n tf python=3.7

Activate env:
conda activate tf

Tensorflow installation
pip install https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.7.0-py3-none-any.whl
