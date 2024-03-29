from changetext.common_state import get_state
from changetext.utils import (
    any_cyr,
    custom_parse,
    cut_number,
    get_form,
    inflect_collocation,
    inflect_enumeration,
    inflect_text,
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


def corr_tags(text, state=None):
    state = state or get_state()
    text_parts = []
    get_index = None
    set_indices = set()
    capitalize_indices = set()
    inflect_next = set()
    for i, item in enumerate(parse_tags(text)):
        if not item.strip():
            pass
        elif item[0] == "<":
            item = item.strip("<>")
            if not item:
                return None
            tags, _, item = item.partition(":")
            tags = set(tags.split(","))

            if "capitalize" in tags:
                tags.remove("capitalize")
                capitalize_indices.add(len(text_parts))

            if item:
                # Inflect the word inside the tag after the colon
                word = item.strip()

                if "get-form" in tags:
                    if get_index is not None:
                        raise ValueError(f"Duplicate <get-form> tag in {text!r}")
                    get_index = len(text_parts)
                    tags.remove("get-form")
                elif "set-form" in tags:
                    set_indices.add(len(text_parts))
                    tags.remove("set-form")

                if tags:
                    item = inflect_text(word, tags)
                else:
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
        delayed += "<{}>".format(",".join(inflect_next))

    if get_index is not None:
        form = get_form(text_parts[get_index])
        form -= {"anim", "inan"}  # discard these two because they don't matter for the nominal case

        for i in set_indices:
            word = text_parts[i]
            text_parts[i] = inflect_text(word, form)

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
        state.prev_tail += delayed

    return smart_join(text_parts)
