set -x
echo "Starting up analytic service..."
cd /src
./wait-for rabbitmq:5672 -t 60 -- python /src/app.py -m /src/relevancy_trained_classifier/svm/relevancy_classifier.pkl \
                   -tf /src/relevancy_trained_classifier/tfidf/relevancy_classifier_tfidf.pkl
