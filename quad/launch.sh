set -x
echo "Starting up analytic service..."
python /src/app.py -m /src/quad_trained/quad_character_model.json \
                   -w /src/quad_trained/quad_character_model_weights.h5 \
                   -v /src/quad_trained/quad_character_model_vocab.pkl
