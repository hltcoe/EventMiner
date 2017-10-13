set -x
echo "Starting up analytic service..."
./src/wait-for rabbitmq:5672 -t 60 -- python /src/app.py \
    -m /src/quad_trained/quad_character_model.json \
    -w /src/quad_trained/quad_character_model_weights.h5 \
    -v /src/quad_trained/quad_character_model_vocab.pkl
