from changetext.common_state import get_state
from changetext.utils import (
    inflect_collocation,
    re_sentence,
    any_cyr,
    cut_number,
    inflect_enumeration,
    get_form,
    smart_join,
    custom_parse,
)


def parse_tags(text):
    start = 0
    for i, c in enumerate(text):
        if c == "<":
            if start < i:
                yield text[start:i]
            start = i
        elif c == ">":
            yield text[start : i + 1]
            start = i + 1

    if start < len(text):
        yield text[start:]


def corr_tags(text):
    # print('corr_tags(%r)' % s)
    li = []
    get_index = None
    set_indices = set()
    capitalize_indices = set()
    inflect_next = set()
    for i, item in enumerate(parse_tags(text)):
        # print(repr(item))
        if not item.strip():
            pass
        elif item[0] == "<":
            item = item.strip("<>")
            if not item:
                return None
            tags, _, item = item.partition(":")
            tags = set(tags.split(","))
            # print(tags)

            if "capitalize" in tags:
                tags.remove("capitalize")
                capitalize_indices.add(len(li))

            if item:
                # Inflect the word inside the tag after the colon
                word = item.strip()

                if "get-form" in tags:
                    if get_index is not None:
                        raise ValueError("Duplicate <get-form> tag in %r" % text)
                    get_index = len(li)
                    tags.remove("get-form")
                elif "set-form" in tags:
                    set_indices.add(len(li))
                    tags.remove("set-form")

                if tags:
                    if " " in word:
                        item = inflect_collocation(word, tags)
                    else:
                        p = custom_parse(word)[0]
                        item = p.inflect(tags).word
                        # if not make_lower and word[0].isupper():
                        if word[0].isupper():
                            item = item.capitalize()
                else:
                    # item = word if not make_lower else word.lower()
                    item = word
            else:
                # Inflect a part of text after the tag till the ending point of the sentence.
                inflect_next = tags
                continue
        elif inflect_next:
            sentence = re_sentence.search(item)
            if sentence:
                item = sentence.group(1)
                tail = sentence.group(2)
            else:
                tail = ""
            item = item.lstrip(" ")
            if not any_cyr(item.split(" ")[0]):
                if item.strip()[0].isdigit():
                    if "loct" in inflect_next:
                        inflect_next.remove("loct")
                        inflect_next.add("loc2")  # inflect into 'году' instead of 'годе'
                    item, tail1 = cut_number(item)
                    item += " " + custom_parse("год")[0].inflect(inflect_next).word + tail1.lstrip(",")
                elif (not li or not any_cyr(li[-1].rstrip().split(" ")[-1])) and inflect_next == {"gent"}:
                    li.append("of ")
                pass
            else:
                if "," in item:
                    item = inflect_enumeration(item, inflect_next)
                elif " " in item:
                    item = inflect_collocation(item, inflect_next)
                else:
                    p = custom_parse(item)[0]
                    item = p.inflect(tags).word
            item += tail
            inflect_next = set()
        else:
            pass
        li.append(item)

    delayed = ""
    if inflect_next:
        delayed += "<%s>" % ",".join(inflect_next)
        # print('Delay to the next string: %r' % prev_tail)

    if get_index is not None:
        # print(get_index)
        form = get_form(li[get_index])
        form -= {"anim", "inan"}  # discard these two because they doesn't matter for the nominal case
        # print(form)
        for i in set_indices:
            word = li[i]
            if " " in word:
                item = inflect_collocation(word, form)
            else:
                p = custom_parse(word)[0]
                item = p.inflect(form).word
                if word[0].isupper():
                    item = item.capitalize()
            li[i] = item

    if capitalize_indices:
        for i in capitalize_indices:
            if i >= len(li):
                delayed += "<capitalize>"
            else:
                for part in li[i].split():
                    if part:
                        li[i] = li[i].replace(part, part.capitalize(), 1)
                        break

    if delayed:
        # print('Delay to the next string: %r' % delayed)
        state = get_state()
        state.prev_tail += delayed

    # print(li)
    return smart_join(li)
