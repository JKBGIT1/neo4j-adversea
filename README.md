## How to run
* python3 -m venv ./venv
* source ./venv/bin/activate
* pip install -r requirements.txt
* docker-compose up -d 
* wait about 10 seconds
* python3 ./main.py

## How to work with neo4j
* connect to localhost:7474 in browser
* use this query `MATCH (p:Person {name: 'donald tusk'})--(a:Article) OPTIONAL MATCH (a)--(relatedPerson:Person) OPTIONAL MATCH (a)--(organization:Organization) OPTIONAL MATCH (organization)--(associate:Person) RETURN p, a, relatedPerson, organization, associate;`