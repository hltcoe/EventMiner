set -x
#echo "Decompressing models..."
#cd $MESOS_SANDBOX
#tar xzf $CLF_FILE
#rm -rf $CLF_FILE
#cd /
set -x
echo "Starting up Kafka analytic service..."
python /src/app.py -m /src/quad_trained/quad_character_model.json \
                   -w /src/quad_trained/quad_character_model_weights.h5 \
                   -v /src/quad_trained/quad_character_model_vocab.pkl
