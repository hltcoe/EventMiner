EventMiner
=======

Using the hammer of supervised learning to make events.

About
-----

EventMiner aims to serve, primarily, as an interface to various NLP analytics
to extract event information from text. This project is setup with a REST
frontend interface, which accepts text input, that is then further passed
via a RabbitMQ messaging queue to various analytics as appropriate. The project
is comprised of Docker containers, with orchestration handled by
docker-compose. This, combined with RabbitMQ as the messaging layer, allows for
clean definitions of interactions between services and minimal setup for the
end user. 

Services
---------

The services defined in this project are as follows:

* `mitie` - Provide NER tagging via [MITIE](https://github.com/mit-nlp/MITIE).
* `relevancy` - An SVM classifier to determine story relevancy based on the story title.
* `quad` - A convolutional neural net to classify a sentence into one of four `QuadCategories`: verbal conflict, verbal cooperation, material conflict, material cooperation.
* `hypnos` - Rule-based event extractor. Used primarily for actor extraction in this setup.
* `collector` - Light process to pull in events and write them out to a file.

Deployment
----------

There are two `docker-compose` projects that make up mjolnir. The first is the
`miner` application itself. The second is `hypnos`, which is the container
architecture around the `PETRARCH2` event extractor. `docker-compose` must be
run for `miner` first, and `hypnos` second, due to nuances relating to the
shared docker networks. Thus, deployment is as follows (assuming the user
starts in the top-level `EventMiner` directory):

```
docker-compose up -d 
cd ./hynpos
docker-compose up -d
```

This will lead to a REST interface deployed on port 6000. With the features
of `docker-compose`, it's possible to arbitrarily scale up the various services
connected within `miner`. For example, the `quad` service is rather slow
since it's a neural net running on a CPU. Since each service consumes from a
messaging queue, we don't need to worry about things such as load balancing;
each service just consumes when it's ready. Given this, to scale the `quad`
service is as simple as (assuming the user is in the root `EventMiner` directory):

```
docker-compose scale quad=3
```

to run three of the `quad` containers.

Usage
-----

The interface accepts JSON input via REST. As an example:

```
import json
import requests

headers = {'Content-Type': 'application/json'}

test = {'title': 'Syrian rebels attacked Aleppo.', 'content': 'This is the content. Rebels attacked Aleppo.'}
data = {'data': test}

r = requests.post('http://localhost:6000/EventMiner', data=json.dumps(data), headers=headers)
```

The response object from `EventMiner` will contain a unique ID for the input data
that allows the user to trace the progress of the content throughout the
pipeline. The pipeline will write data out to the `EventMiner/data` directory. The
results are in a file titled `events.YYYYMMDD.txt` with one JSON record per
line. The output format (for now...) is as follows:

```
{u'content': u'This is the content. Rebels attacked Aleppo.',
 u'event_info': {u'267bbae4-dcc0-4224-94e9-67679b0b6ad1': {u'coded': [],
   u'predicted_class': {u'class': 4, u'score': u'0.89923'},
   u'sent': u'This is the content.'},
  u'8b464457-18d2-419c-b5c1-49c6131be947': {u'coded': [[u'---REB',
     u'SYR',
     u'190']],
   u'predicted_class': {u'class': 4, u'score': u'0.986187'},
   u'sent': u'Rebels attacked Aleppo.'}},
 u'pipeline_key': u'4c4f7e7a-db31-4137-a888-2cdbbbf1c225',
 u'predicted_relevancy': 1,
 u'sents': {u'267bbae4-dcc0-4224-94e9-67679b0b6ad1': u'This is the content.',
  u'8b464457-18d2-419c-b5c1-49c6131be947': u'Rebels attacked Aleppo.'},
 u'title': u'Syrian rebels attacked Aleppo.'}
 ```


Acknowledgements
----------------

This work was funded by the DARPA Quantitative Crisis Response (QCR) program.
