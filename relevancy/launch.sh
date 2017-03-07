set -x
echo "Starting up analytic service..."
cd /src
python /src/app.py -m /src/relevancy_trained_classifier/svm/relevancy_classifier.pkl \
                   -tf /src/relevancy_trained_classifier/tfidf/relevancy_classifier_tfidf.pkl
