hypnos
======

A RESTful API around the [PETRARCH](https://github.com/openeventdata/petrarch)
event data coder. Using `docker compose`, this setup also integrates the 
Stanford [CoreNLP](http://nlp.stanford.edu/software/corenlp.shtml) parser
using Casey Hilland's [docker container](https://github.com/chilland/ccNLP).
This setup allows the users to stream texts into the API, rather than the 
batch mode seen in applications such as the [Phoenix pipeline](https://github.com/openeventdata/phoenix_pipeline).

Running
-------

Running the system is as simple as using

`docker-compose up`

or 

`docker-compose up -d`

to run in the background.

This assumes that you have `docker-compose` and `docker` installed.

Usage
-----

```
headers = {'Content-Type': 'application/json'}
data = {'text': "At least 37 people are dead after Islamist radical group Boko
Haram assaulted a town in northeastern Nigeria.", 'id': 'abc123', 'date':
'20010101'}
data = json.dumps(data)
r = requests.get('http://localhost:5002/hypnos/extract', data=data,
                 headers=headers)
r.json()
```

Returns:

```
{u'abc123': {u'meta': {u'date': u'20010101'},
  u'sents': {u'0': {u'content': u'At least 37 people are dead after Islamist
  radical group Boko Haram assaulted a town in northeastern Nigeria .',
      u'events': [[u'NGAREBMUS', u'NGA', u'190']],
          u'issues': [[u'ID_EXTREMISM', 1], [u'NAMED_TERROR_GROUP', 1]],
              u'parsed': u'(ROOT (S (NP (QP (IN AT ) (JJS LEAST ) (CD 37 ) )
              (NNS PEOPLE ) ) (VP (VBP ARE ) (ADJP (JJ DEAD ) ) (SBAR (IN AFTER
              ) (S (NP (JJ ISLAMIST ) (JJ RADICAL ) (NN GROUP ) (NNP BOKO )
              (NNP HARAM ) ) (VP (VBD ASSAULTED ) (NP (NP (DT A ) (NN TOWN ) )
              (PP (IN IN ) (NP (JJ NORTHEASTERN ) (NNP NIGERIA ) ) ) ) ) ) ) )
              (. . ) ) )'}}}}
```
