from constants import ANCESTOR_TAGS, LAW_SUFFIX, Suffix, Tag, SUFFIX_TO_TAG, HREF, NON_EXISTING_LAWS_PATH, \
    APPENDIX_NUM_TO_HEB, CHAPTER_NUM_TO_HEB, FULL_TO_SHORT_TAG
from classes import Chapter, Part, Point, Preamble, Appendix, Section, Law, Subtitle, WrapUp
import os
import json
import glob


def load_json(file_path):
    try:
        if file_path and os.path.exists(file_path):
            with open(file_path, 'r') as json_file:
                result = json.load(json_file)
        else:
            result = {}
        return result
    except json.decoder.JSONDecodeError:
        return {}


NON_EXISTING_LAWS = load_json(NON_EXISTING_LAWS_PATH)


def parse_ref(ref_element, frbr_work_uri):
    raw_href = ref_element.attrib[HREF]
    if raw_href.startswith('#'):
        href = f'{frbr_work_uri}{raw_href}'
    elif raw_href.startswith('/'):
        href = raw_href[1:]
    else:
        href = raw_href
    frbr_work_uri, eid = split_ref(href)
    if not os.path.exists(frbr_work_uri) or not os.path.exists(os.path.join(frbr_work_uri, LAW_SUFFIX)):
        NON_EXISTING_LAWS[frbr_work_uri] = ""
        return "", ""
    return frbr_work_uri, eid


def write_non_existing_rules():
    with open(NON_EXISTING_LAWS_PATH, "w") as f:
        f.write(json.dumps(NON_EXISTING_LAWS, indent=4, ensure_ascii=False).encode('utf8').decode())


def get_ref_ancestor_element(law, element):
    parent = law.parent_map.get(element)
    while parent and parent.tag not in ANCESTOR_TAGS:
        last_ancestor = parent
        parent = law.parent_map.get(parent)
        if not parent:
            raise Exception(f'parent was not found for element {element.tag}:{element.text} in law {law.path}, '
                            f'last ancestor found is: {last_ancestor.tag}:{last_ancestor.text}')
    return classify_vertex_by_tag(parent.tag, parent, law)


def classify_vertex_by_tag_and_eid(tag, eids, law):
    if tag:
        for eid in eids:
            element = law.root.findall(f'.//{tag}[@eId="{eid}"]')
            if len(element) > 1:
                raise Exception(f'Found more than one element {FULL_TO_SHORT_TAG[tag]} with eid {eid} in law {law.path}')
                # return classify_vertex_by_tag(Tag.Law, law.root, law)  # if we didn't find the element, we return a law vertex
            if element:
                element = element[0]
                return classify_vertex_by_tag(tag, element, law)
        raise Exception(f'Did not find element {FULL_TO_SHORT_TAG[tag]} with eids {eids} in law {law.path}')
        # return classify_vertex_by_tag(Tag.Law, law.root, law)  # if we didn't find the element, we return a law vertex
    else:
        return classify_vertex_by_tag(tag, law.root, law)


def classify_vertex_by_tag(tag, element, law):
    if tag == Tag.Chapter:
        return Chapter(law, element)
    elif tag == Tag.Point:
        return Point(law, element)
    elif tag == Tag.Section:
        return Section(law, element)
    elif tag == Tag.Part:
        return Part(law, element)
    elif tag == Tag.Appendix:
        return Appendix(law, element)
    elif tag == Tag.Preamble:
        return Preamble(law, element)
    elif tag == Tag.Subtitle:
        return Subtitle(law, element)
    elif tag == Tag.WrapUp:
        return WrapUp(law, element)
    elif tag == Tag.Law:
        return law
    else:
        raise Exception('Unexpected behavior')


def classify_tag(eid):
    if eid == Suffix.Law:
        return Tag.Law

    is_part = Suffix.Part if Suffix.Part in eid else None
    is_section = Suffix.Section if Suffix.Section in eid else None
    is_point = Suffix.Point if Suffix.Point in eid else None
    is_chapter = Suffix.Chapter if Suffix.Chapter in eid else None
    is_appendix = Suffix.Appendix if Suffix.Appendix in eid else None
    is_preamble = Suffix.Preamble if Suffix.Preamble in eid else None
    is_subtitle = Suffix.Subtitle if Suffix.Subtitle in eid else None
    is_wrapup = Suffix.WrapUp if Suffix.WrapUp in eid else None

    potential_suffixes = [is_part, is_section, is_point, is_chapter, is_appendix, is_preamble, is_subtitle, is_wrapup]
    potential_suffixes = list(filter(None, potential_suffixes))

    if not potential_suffixes:
        raise Exception(f'Did not succeed to classify tag to suffix {eid}')
        # return Tag.Law

    locations = [eid.find(suffix) for suffix in potential_suffixes]
    last_location = max(locations)
    last_location_index = locations.index(last_location)
    return SUFFIX_TO_TAG[potential_suffixes[last_location_index]]


def classify_eid_by_tag(tag, eid):
    if tag == Tag.Appendix:
        _, suffix = eid.split(Suffix.Appendix)
        if suffix.startswith('_'):
            suffix = suffix[1:]
        if suffix:
            heb_num_suffix = APPENDIX_NUM_TO_HEB.get(suffix)
            if heb_num_suffix:
                if isinstance(heb_num_suffix, str):
                    heb_num_suffix = [heb_num_suffix]
                return [f'{Suffix.Appendix}_{option}' for option in heb_num_suffix]
    elif tag == Tag.Chapter:
        _, suffix = eid.split(Suffix.Chapter)
        if suffix.startswith('_'):
            suffix = suffix[1:]
        if suffix:
            heb_num_suffix = CHAPTER_NUM_TO_HEB.get(suffix)
            if heb_num_suffix:
                if isinstance(heb_num_suffix, str):
                    heb_num_suffix = [heb_num_suffix]
                return [f'{Suffix.Chapter}_{option}' for option in heb_num_suffix]
    return [eid]


def split_ref(ref):
    if '#' in ref:
        frbr_work_uri, eid = ref.split('#')
    else:
        frbr_work_uri, eid = ref, ""
    return frbr_work_uri, eid


def build_laws_mapping():
    laws = []
    frbr_work_uri_to_law = {}
    for law_path in glob.glob(f'akn/**/*.xml', recursive=True):
        law = Law(law_path)
        frbr_work_uri_to_law[law.frbr_work_uri] = law
        laws.append(law)
    return laws, frbr_work_uri_to_law
