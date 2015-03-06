from nltk.tag.stanford import NERTagger
import config
# Requires nltk library and plugins

class StanfordNER(object):
    """
    Interacts with the Stanford Tagger.

    :param classifier: Classifier to use for tagging. Defaults to the ``STANFORD_DEFAULT_CLASSIFIER`` config variable.
    :param jarfile: Jarfile to use for tagging. Defaults to the ``STANFORD_JARFILE`` config variable.
    """

    def __init__(self, classifier=None, jarfile=None):
        self.classifier = classifier or config.STANFORD_DEFAULT_CLASSIFIER
        self.jarfile = jarfile or config.STANFORD_JARFILE


    def run_tagger(self, payload):
        """        
        Runs :py:meth:`nltk.tag.stanford.NERTagger.tag_sents` on the provided text
        (http://www.nltk.org/api/nltk.tag.html#nltk.tag.stanford.StanfordTagger.tag_sents)

        :param payload: Fulltext payload.
        :type payload: string
        :return: List of parsed sentences.
        """
        return NERTagger(self.classifier, self.jarfile).tag_sents([payload.encode('ascii', 'ignore').split()])


    def process_sentences(self, sentences):
        """
        Takes a list of parsed sentences, such as returned by :py:meth:`nltk.tag.stanford.NERTagger.tag_sents`,
        and reformats them for entity processing.

        :param sentences: Parsed sentences from the NER Tagger
        :type sentences: list of tuples
        :return: Dict of lists (locations, people, and organizations)
        """
        # Set up empty dicts to add formatted responses
        entity_dict = {
            "LOCATION": [],
            "PERSON": [],
            "ORGANIZATION": []
        }
        # Walk through each section of each sentence
        for sentence in sentences:
            for index, pair in enumerate(sentence):
                element, entity_type = pair[0], pair[1]
                if entity_type in entity_dict.keys():
                    # It is a designated entity. Check to see if the word before it was the same type. if so, it's assumed to be the same entity.
                    if index > 0 and sentence[index-1][1] == entity_type:
                        # Yes, so it is paired with the previous word. Merge it.
                        old_entry = entity_dict[entity_type][-1]
                        entity_dict[entity_type][-1] = "%s %s" % (old_entry, element)
                    else:
                        # No, so it is a new entity.
                        entity_dict[entity_type].append(element)
        return entity_dict


    def extract_entities(self, payload):
        """
        Takes any input text, runs it through the Stanford tagger to extract any entities,
        and formats the results as a list of people, places, and organizations.

        Calls :py:meth:`parserbot.stanford.StanfordNER.run_tagger` followed by :py:meth:`parserbot.stanford.StanfordNER.process_sentences`.

        :param payload: The payload in natural language text.
        :type payload: string
        :return: Dict of lists (locations, people, and organizations)
        """
        # Get the raw response
        sentences = self.run_tagger(payload)
        entities = self.process_sentences(sentences)
        return entities
