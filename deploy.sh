#!/usr/bin/env bash

MODEL_NAME="default"
MODEL_FILE="main.json"
CEREBRO_URL="http://192.168.1.16:9444"

echo "Checking cerebro status..."
echo " ==> curl --write-out %{http_code} --silent --output /dev/null ${CEREBRO_URL}/models/${MODEL_NAME}/train"
response=$(curl --write-out %{http_code} --silent --output /dev/null ${CEREBRO_URL}/models/${MODEL_NAME}/train)

if [ $response = "200" ]
then
    echo "Cerebro is available !"
else
    echo "Cerebro is unavailable (${response}), please try again in a few minutes."
    exit 1
fi

echo "Uploading the model ${MODEL_NAME} from the file ${MODEL_FILE} ..."
echo " ==> curl -X PUT \"${CEREBRO_URL}/models/${MODEL_NAME}/samples\" -d @${MODEL_FILE}"
curl -X PUT "${CEREBRO_URL}/models/${MODEL_NAME}/samples" -d @${MODEL_FILE} || exit 1
echo "Model uploaded !"

echo "Training the model ${MODEL_NAME} ..."
echo " ==> curl -X POST \"${CEREBRO_URL}/models/${MODEL_NAME}/train\""
curl -X POST "${CEREBRO_URL}/models/${MODEL_NAME}/train" || exit 1
echo "Model train triggered !"


attempt_counter=0
max_attempts=18 # Wait for 5 min max

until [ $(curl --write-out %{http_code} --silent --fail --output /dev/null ${CEREBRO_URL}/models/${MODEL_NAME}/train) = "200" ]; do
    if [ ${attempt_counter} -eq ${max_attempts} ];then
      echo "Max attempts reached, check the cerebro instance."
      exit 1
    fi

    printf '.'
    attempt_counter=$(($attempt_counter+1))
    sleep 10
done

echo "Model has been successfully deployed !"
