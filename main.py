import json
import settings
from py2neo import Graph, Node, Relationship

graph = Graph(settings.NEO4J_BOLT_URL,
            auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD))

create_person_query = '''
MERGE (person: Person {name: $name})
RETURN person;
'''

create_organization_query = '''
MERGE (organization: Organization {name: $name})
RETURN organization;
'''

with open('clean_data.jl', 'r') as file:
    for line in file:
        article = json.loads(line)

        article_title = article['title'].lower()

        article_node = Node('Article', title=article_title)

        graph.create(article_node)

        if 'gpt3_names' not in article:
            continue
        
        try:
            if 'gpt3_names' in article:
                names = article['gpt3_names']

                for name in names:
                    person_cursor = graph.run(create_person_query, name=name.lower())
                    person_node = person_cursor.data()[0]['person']
                    relationship = Relationship(article_node, 'CONTAINS', person_node)

                    graph.create(relationship)
            
            if 'gpt3_organizations' in article:
                # TODO: add organization to
                organizations_with_associates = article['gpt3_organizations']

                for org_with_asscs in organizations_with_associates:
                    org_name = org_with_asscs['organization']
                    org_cursor = graph.run(create_organization_query, name=name.lower())
                    org_node = org_cursor.data()[0]['organization']

                    associates = org_with_asscs['associates']

                    for name in associates:
                        person_cursor = graph.run(create_person_query, name=name.lower())
                        person_node = person_cursor.data()[0]['person']

                        relationship = Relationship(org_node, 'CONTAINS', person_node)

                        graph.create(relationship)

        except Exception as e:
            print(e)