from nltk.tag.stanford import NERTagger
import settings
# Requires nltk library and plugins
# NOTE: set STANFORD_NER_HOME to wherever you unpacked your Stanford NER directory. Default classifier should then load automaticall8y.

def stanford_tag(sentence, classifier=settings.STANFORD_DEFAULT_CLASSIFIER, jarfile=settings.STANFORD_JARFILE):
    """ Takes any text and optional classifier/jarfile kwargs. Returns raw response from Stanford NER. """
    t = NERTagger(classifier, jarfile)
    return t.batch_tag([sentence.split()])

def get_entities(sentence, **kwargs):
    """ Takes any text and optional classifier/jarfile kwargs. Returns a dictionary """
    # Get the raw response
    parsed_sentences = stanford_tag(sentence, **kwargs)
    # Set up empty dicts to add formatted responses
    entity_dict = {
        "LOCATION": [],
        "PERSON": [],
        "ORGANIZATION": []
    }
    # Walk through each section of each sentence
    for parsed_sentence in parsed_sentences:
        for index, pair in enumerate(parsed_sentence):
            element, entity_type = pair[0], pair[1]
            if entity_type in entity_dict.keys():
                # It is a designated entity. Check to see if the word before it was the same type. if so, it's assumed to be the same entity.
                if index > 0 and parsed_sentence[index-1][1] == entity_type:
                    # Yes, so it is paired with the previous word. Merge it.
                    old_entry = entity_dict[entity_type][-1]
                    entity_dict[entity_type][-1] = "%s %s" % (old_entry, element)
                else:
                    # No, so it is a new entity.
                    entity_dict[entity_type].append(element)
    return entity_dict