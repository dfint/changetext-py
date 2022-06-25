from changetext.common_state import get_state
from changetext.utils import (
    any_cyr,
    custom_parse,
    cut_number,
    get_form,
    inflect_collocation,
    inflect_enumeration,
    smart_join,
    split_sentence,
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
    text_parts = []
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
                capitalize_indices.add(len(text_parts))

            if item:
                # Inflect the word inside the tag after the colon
                word = item.strip()

                if "get-form" in tags:
                    if get_index is not None:
                        raise ValueError("Duplicate <get-form> tag in %r" % text)
                    get_index = len(text_parts)
                    tags.remove("get-form")
                elif "set-form" in tags:
                    set_indices.add(len(text_parts))
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
            item, tail = split_sentence(item)
            item = item.lstrip(" ")
            if not any_cyr(item.split(" ")[0]):
                if item.strip()[0].isdigit():
                    if "loct" in inflect_next:
                        inflect_next.remove("loct")
                        inflect_next.add("loc2")  # inflect into 'году' instead of 'годе'
                    item, tail1 = cut_number(item)
                    item += " " + custom_parse("год")[0].inflect(inflect_next).word + tail1.lstrip(",")
                elif (not text_parts or not any_cyr(text_parts[-1].rstrip().split(" ")[-1])) and inflect_next == {
                    "gent"
                }:
                    text_parts.append("of ")
                pass
            else:
                tags = inflect_next - {"masc", "femn", "neut", "plur"}
                if "," in item:
                    item = inflect_enumeration(item, tags)
                elif " " in item:
                    item = inflect_collocation(item, tags)
                else:
                    p = custom_parse(item)[0]
                    item = p.inflect(inflect_next).word
            item += tail
            inflect_next = set()
        else:
            pass
        text_parts.append(item)

    delayed = ""
    if inflect_next:
        delayed += "<%s>" % ",".join(inflect_next)
        # print('Delay to the next string: %r' % prev_tail)

    if get_index is not None:
        # print(get_index)
        form = get_form(text_parts[get_index])
        form -= {"anim", "inan"}  # discard these two because they doesn't matter for the nominal case
        # print(form)
        for i in set_indices:
            word = text_parts[i]
            if " " in word:
                item = inflect_collocation(word, form)
            else:
                p = custom_parse(word)[0]
                item = p.inflect(form).word
                if word[0].isupper():
                    item = item.capitalize()
            text_parts[i] = item

    if capitalize_indices:
        for i in capitalize_indices:
            if i >= len(text_parts):
                delayed += "<capitalize>"
            else:
                for part in text_parts[i].split():
                    if part:
                        text_parts[i] = text_parts[i].replace(part, part.capitalize(), 1)
                        break

    if delayed:
        # print('Delay to the next string: %r' % delayed)
        state = get_state()
        state.prev_tail += delayed

    # print(li)
    return smart_join(text_parts)
