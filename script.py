import json
from parsers import stanford, calais, zemanta, dbpedia

ALL_PARSERS = 'stanford calais zemanta dbpedia'

# Use this to either a) categorize a given payload with stanford, calais, and zemanta parsers; or b) take an input json file and categorize it (add category field to it)

def categorize(payload, id_str=None, parsers=ALL_PARSERS):
    parsers = parsers.split()
    results = dict([(i, None) for i in parsers])
    # Run through Stanford NER
    if 'stanford' in parsers:
        results['stanford'] = stanford.get_entities(payload)
    # Run through Calais
    if 'calais' in parsers:
        results['calais'] = calais.entity_call(payload, id_str)
    # Run through Zemanta
    if 'zemanta' in parsers:
        results['zemanta'] = zemanta.ZemantaAPI().entity_query(payload)
    # Run through DBPedia
    if 'dbpedia' in parsers:
        results['dbpedia'] = dbpedia.get_entities(payload)
    return results

def mass_categorize(infile='infile.json', outfile='outfile.json', parsers=ALL_PARSERS):
    with open(infile) as f:
        entries = json.load(f)
    all_entities = []
    for entry in entries:
        payload = "%s. %s" % (entry['name'], entry['fulltext'])
        entities = categorize(payload.encode('utf-8', 'ignore'), id_str=entry['id'], parsers=parsers)
        entry['categories'] = entities
    with open(outfile, 'w+') as f:
        json.dump(entries, f)