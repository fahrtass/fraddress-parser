#!/usr/bin/python
# -*- coding: utf-8 -*-

import pycrfsuite
import os
import re
import warnings
from collections import OrderedDict


#  _____________________
# |1. CONFIGURE LABELS! |
# |_____________________| 
#     (\__/) || 
#     (•ㅅ•) || 
#     / 　 づ
LABELS = ['Area',
          'AreaNumber',
          'AreaLink',
          'AreaName',
          'AddressNumber',
          'AddressNumberSuffix',
          'StreetType',
          'StreetLink',
          'StreetName',
          'StreetDirection',
          'StreetNumber',
          'PostalBox',
          'PostalBoxNumber',
          'PreSubAddress',
          'SubAddressType',
          'SubAddressNumber',
          'PostSubAddress',
          'City',
          'Zipcode',
          'Phone',
          'PhoneLink',
          'PhoneNumber',
          'NotAddress'] # The labels should be a list of strings

#***************** OPTIONAL CONFIG ***************************************************
PARENT_LABEL  = 'TokenSequence'               # the XML tag for each labeled string
GROUP_LABEL   = 'Collection'                  # the XML tag for a group of strings
NULL_LABEL    = 'Null'                        # the null XML tag
MODEL_FILE    = 'learned_settings.crfsuite'   # filename for the crfsuite settings file

DIRECTIONS = set(['n', 's', 'e', 'w', 'o',
                  'ne', 'nw', 'se', 'sw', 'no',
                  'nord', 'sud', 'est', 'ouest',
                  'nord-est', 'nord-ouest', 'sud-est', 'sud-ouest'])

STREET_NAMES = {
    "abbaye", "agglomération", "aire", "aires", "allée", "allées", "anse", "arcade", "arcades", "autoroute", "avenue",
    "barriere", "barrieres", "bastide", "bastion", "beguinage", "béguinages", "berge", "berges", "bois", "boucle",
    "boulevard", "bourg", "butte", "cale", "camp", "campagne", "camping", "carre", "carreau", "carrefour", "carrière",
    "carrières", "castel", "cavée", "central", "chalet", "chapelle", "charmille", "château", "chaussée", "chaussées",
    "chemin", "cheminement", "cheminements", "chemins", "chez", "cite", "cites", "cloître", "clos", "col", "colline",
    "collines", "contour", "corniche", "corniches", "cote", "côteau", "cottage", "cottages", "cour", "cours", "darse",
    "degré", "degrés", "descente", "descentes", "digue", "digues", "domaine", "domaines", "écluse", "écluses", "église",
    "enceinte", "enclave", "enclos", "escalier", "escaliers", "espace", "esplanade", "esplanades", "étang", "faubourg",
    "ferme", "fermes", "fontaine", "fort", "forum", "fosse", "fosses", "foyer", "galerie", "galeries", "gare", "garenne",
    "grille", "grimpette", "groupe", "groupement", "groupes", "halle", "halles", "hameau", "hameaux", "hippodrome", "hlm",
    "île", "immeuble", "immeubles", "impasse", "impasses", "jardin", "jardins", "jetee", "jetees", "levée", "lieu dit",
    "lotissement", "lotissements", "mail", "manoir", "marche", "marches", "mas", "métro", "montée", "montees", "moulin",
    "moulins", "musée", "palais", "parc", "parcs", "parking", "parvis", "passage", "passe", "passerelle", "passerelles",
    "passes", "patio", "pavillon", "pavillons", "péripherique", "péristyle", "place", "placis", "plage", "plages",
    "plaine", "plan", "plateau", "plateaux", "pointe", "point", "pont", "ponts", "porche", "port", "porte", "portique",
    "portiques", "poterne", "pourtour", "pré", "presqu'île", "promenade", "quai", "quartier", "raccourci", "raidillon",
    "rampe", "rempart", "résidence", "résidences", "roc", "rocade", "rond", "roquet", "rotonde", "route", "routes", "rue",
    "ruelle", "ruelles", "rues", "rn", "rd", "rte", "sente", "sentes", "sentier", "sentiers", "square", "stade", "station", "terrain",
    "terrasse", "terrasses", "terre-plein", "tertre", "tertres", "tour", "traverse", "val", "vallée", "vallon",
    "venelle", "venelles", "via", "villa", "village", "villages", "villas", "voie", "voies"
}

AREA = {
    "zone", "centre", "commercial", "zi", "za", "zac", "cc", "c.c", "c.c.", "c", "c.", "lieu", "dit", "espace", "galerie",
    "marchande", "parking", "pôle", "ccial", "cite", "z.a.", "z.a"
}

PREPOSITIONS = {
    "le", "la", "de", "du", "les", "des", "a", "au", "aux"
}
#************************************************************************************



try :
    TAGGER = pycrfsuite.Tagger()
    TAGGER.open(os.path.split(os.path.abspath(__file__))[0]+'/'+MODEL_FILE)
except IOError :
    TAGGER = None
    warnings.warn('You must train the model (parserator train [traindata] [modulename]) to create the %s file before you can use the parse and tag methods' %MODEL_FILE)

def parse(raw_string):
    if not TAGGER:
        raise IOError('\nMISSING MODEL FILE: %s\nYou must train the model before you can use the parse and tag methods\nTo train the model annd create the model file, run:\nparserator train [traindata] [modulename]' %MODEL_FILE)

    tokens = tokenize(raw_string)
    if not tokens :
        return []

    features = tokens2features(tokens)

    tags = TAGGER.tag(features)
    return list(zip(tokens, tags))

def tag(raw_string) :
    tagged = OrderedDict()
    for token, label in parse(raw_string) :
        tagged.setdefault(label, []).append(token)

    for token in tagged :
        component = ' '.join(tagged[token])
        component = component.strip(' ,;')
        tagged[token] = component

    return tagged


#  _____________________
# |2. CONFIGURE TOKENS! |
# |_____________________| 
#     (\__/) || 
#     (•ㅅ•) || 
#     / 　 づ
def tokenize(raw_string):
    # this determines how any given string is split into its tokens
    # handle any punctuation you want to split on, as well as any punctuation to capture

    if isinstance(raw_string, bytes):
        try:
            raw_string = str(raw_string, encoding='utf-8')
        except:
            raw_string = str(raw_string)
    
    re_tokens = re.compile(r"""
    \(*\b[^\s,;#&()]+[.,;)\n]*   # ['ab. cd,ef '] -> ['ab.', 'cd,', 'ef']
    |
    [#&]                       # [^'#abc'] -> ['#']
    """,
                           re.VERBOSE | re.UNICODE)  # re.compile( [REGEX HERE], re.VERBOSE | re.UNICODE)
    tokens = re_tokens.findall(raw_string)

    if not tokens :
        return []
    return tokens


#  _______________________
# |3. CONFIGURE FEATURES! |
# |_______________________| 
#     (\__/) || 
#     (•ㅅ•) || 
#     / 　 づ
def tokenFeatures(token) :
    if token in (u'&', u'#', u'½'):
        token_clean = token
    else:
        token_clean = re.sub(r'(^[\W]*)|([^.\w]*$)', u'', token,
                             flags=re.UNICODE)

    token_abbrev = re.sub(r'[.]', u'', token_clean.lower())
    features = {
        'abbrev': token_clean[-1] == u'.',
        'digits': digits(token_clean),
        'word': (token_abbrev
                 if not token_abbrev.isdigit()
                 else False),
        'trailing.zeros': (trailingZeros(token_abbrev)
                           if token_abbrev.isdigit()
                           else False),
        'length': (u'd:' + str(len(token_abbrev))
                   if token_abbrev.isdigit()
                   else u'w:' + str(len(token_abbrev))),
        'endsinpunc': (token[-1]
                       if bool(re.match('.+[^.\w]', token, flags=re.UNICODE))
                       else False),
        'area' : token_abbrev in AREA,
        'directional': token_abbrev in DIRECTIONS,
        'street_name': token_abbrev in STREET_NAMES,
        'preposition': token_abbrev in PREPOSITIONS,
        'has.vowels': bool(set(token_abbrev[1:]) & set('aeiouy')),
    }
    return features


def tokens2features(tokens):
    # this should call tokenFeatures to get features for individual tokens,
    # as well as define any features that are dependent upon tokens before/after
    
    feature_sequence = [tokenFeatures(tokens[0])]
    previous_features = feature_sequence[-1].copy()

    for token in tokens[1:] :
        # set features for individual tokens (calling tokenFeatures)
        token_features = tokenFeatures(token)
        current_features = token_features.copy()

        # features for the features of adjacent tokens
        feature_sequence[-1]['next'] = current_features
        token_features['previous'] = previous_features        
        
        # DEFINE ANY OTHER FEATURES THAT ARE DEPENDENT UPON TOKENS BEFORE/AFTER
        # for example, a feature for whether a certain character has appeared previously in the token sequence
        
        feature_sequence.append(token_features)
        previous_features = current_features

    if len(feature_sequence) > 1 :
        # these are features for the tokens at the beginning and end of a string
        feature_sequence[0]['rawstring.start'] = True
        feature_sequence[-1]['rawstring.end'] = True
        feature_sequence[1]['previous']['rawstring.start'] = True
        feature_sequence[-2]['next']['rawstring.end'] = True

    else : 
        # a singleton feature, for if there is only one token in a string
        feature_sequence[0]['singleton'] = True

    return feature_sequence

# define any other methods for features. this is an example to get the casing of a token
def casing(token) :
    if token.isupper() :
        return 'upper'
    elif token.islower() :
        return 'lower'
    elif token.istitle() :
        return 'title'
    elif token.isalpha() :
        return 'mixed'
    else :
        return False


def digits(token):
    if token.isdigit():
        return 'all_digits'
    else:
        return 'no_digits'


def trailingZeros(token):
    results = re.findall(r'(0+)$', token)
    if results:
        return results[0]
    else:
        return ''


