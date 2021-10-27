import pymorphy2

morph = pymorphy2.MorphAnalyzer()

unwanted_tags = ('Name', 'Surn', 'Infr')


def custom_parse(text):
    if text.lower().startswith('адамантин'):
        return morph.parse(text)  # Pymorphy2 thinks that adamantine is a surname and treats it properly
    else:
        return [p for p in morph.parse(text) if all(tag not in p.tag for tag in unwanted_tags)]


def is_adjective(word: str, parse=None):
    if parse is None:
        parse = custom_parse(word)
    return any('ADJF' in p.tag or 'PRTF' in p.tag for p in parse)


def parse_as_adjective(adjective: str) -> list:
    parse = [p for p in custom_parse(adjective) if 'ADJF' in p.tag or 'PRTF' in p.tag]
    assert len(parse) > 0, 'parse: %r' % parse
    return parse


def inflect_adjective(adjective: str, gender: str, case='nomn', animated=None):
    # print('inflect_adjective(%s, %s)' % (adjective, case))
    assert gender is not None
    parse = parse_as_adjective(adjective)
    p = parse[0]
    form_set = {gender, case}
    if animated is not None and gender in {'masc', 'plur'}:
        form_set.add('anim' if animated else 'inan')
    # print('form_set:', form_set)
    new_form = p.inflect(form_set)
    if new_form is None:
        form_set = {gender, case}
        # print('form_set:', form_set)
        new_form = p.inflect(form_set)
    ret = new_form.word
    # print('%s -> %s' % (adjective, ret))
    return ret


def inflect_noun(word: str, case: str, orig_form=None):
    # print('inflect_noun(%r, %r, %r)' % (word, case, orig_form))
    parse = list(filter(lambda x: x.tag.POS == 'NOUN', custom_parse(word)))

    if orig_form:
        parse = [p for p in parse if orig_form in p.tag]

    if len(parse) == 0:
        # print('Failed to set %r to %s case.' % (word, case))
        return None

    new_form = parse[0].inflect({case})

    return new_form.word


gent_case_except = {
    'шпинель': 'шпинели',  # определяет как сущ. м.р.
    'стена': 'стены',  # определяет как сущ. м.р.
    'лиса': 'лисы',  # определяет как сущ. м.р.
    'споры': 'спор',  # в родительный падеж ставит как "споров"
}


def genitive_case_single_noun(word: str):
    # print('genitive_case_single_noun')
    # print(word)
    if word.lower() in gent_case_except:
        return gent_case_except[word.lower()]
    else:
        return inflect_noun(word, case='gent')


gender_exceptions = {
    'шпинель': 'femn', 'гризли': 'masc',
}


def pm_gender(parse):
    tag = parse.tag
    # print(tag)
    if tag.number == 'plur':
        gender = tag.number
    else:
        gender = tag.gender
    # print(gender)
    return str(gender)  # explicitly convert to a string any internal types returned from pymorphy2


def get_gender(obj, known_tags=None):
    # print("get_gender(%r, known_tags=%r)" % (obj, known_tags))
    assert ' ' not in obj, 'get_gender() is not suitable for word collocations'

    if '-' in obj:
        obj = obj.split('-')
        if obj[0] in {'мини'}:
            obj = obj[1]
            # print('Using the second part of the hyphen-compound: %r' % obj)
        else:
            obj = obj[0]
            # print('Using the first part of the hyphen-compound: %r' % obj)

    parse = custom_parse(obj)
    if known_tags is not None:
        parse = [p for p in parse if known_tags in p.tag]

    if obj.lower() in gender_exceptions:
        return gender_exceptions[obj.lower()]
    else:
        if len(parse) > 0:
            gender = pm_gender(parse[0])
            for p in parse:
                if pm_gender(p) != gender:
                    # print("Gender cannot be recognized definitely for %r. Try to specify known tags (eg. case)" % obj)
                    return None
        else:
            # print("Gender not recoginzed for %r" % obj)
            return None
        return pm_gender(parse[0])


def any_in_tag(gram, parse):
    return any(gram in p.tag for p in parse)


def genitive_case_list(words: list):
    # print("genitive_case_list(%r)" % words)
    if len(words) == 1:
        gender = get_gender(words[0], {'nomn'})
    else:
        gender = None
        for word in words:
            if any_in_tag({'NOUN', 'nomn'}, custom_parse(word)):
                gender = get_gender(word, {'NOUN', 'nomn'})
                break
        assert gender is not None

    for word in words:
        if is_adjective(word):
            word = inflect_adjective(word, gender, 'gent')
        else:
            word = genitive_case_single_noun(word)
        assert word is not None
        yield word


def genitive_case(word: str):
    return ' '.join(genitive_case_list(word.split()))
