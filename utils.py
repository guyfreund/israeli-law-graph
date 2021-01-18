from constants import ANCESTOR_TAGS, LAW_SUFFIX, Suffix, Tag, SUFFIX_TO_TAG, HREF, APPENDIX_NUM_TO_HEB, CHAPTER_NUM_TO_HEB, FULL_TO_SHORT_TAG
from classes import Chapter, Part, Point, Preamble, Appendix, Section, Law, Subtitle, WrapUp
from error import Error, add_error_entry

import os
import glob
import logging


def parse_ref(ref_element, law, errors_dict):
    raw_href = ref_element.attrib[HREF]

    if raw_href.startswith('#'):
        href = f'{law.frbr_work_uri}{raw_href}'
    elif raw_href.startswith('/'):
        href = raw_href[1:]
    else:
        href = raw_href

    frbr_work_uri, eid = split_ref(href)

    if not os.path.exists(frbr_work_uri):
        error_msg = Error.PATH_DOES_NOT_EXISTS.value.format(frbr_work_uri)
        logging.error(error_msg)
        add_error_entry(errors_dict=errors_dict, error_msg=error_msg, from_law=law, error_type=Error.PATH_DOES_NOT_EXISTS.name, from_element=ref_element)
        return str(), str()
    if not os.path.exists(os.path.join(frbr_work_uri, LAW_SUFFIX)):
        error_msg = Error.NO_LAW_FOUND.value.format(frbr_work_uri)
        logging.error(error_msg)
        add_error_entry(errors_dict=errors_dict, error_msg=error_msg, from_law=law, error_type=Error.NO_LAW_FOUND.name, from_element=ref_element)
        return str(), str()

    return frbr_work_uri, eid


def get_ref_ancestor_element(law, element):
    parent = law.parent_map.get(element)
    while parent and parent.tag not in ANCESTOR_TAGS:
        last_ancestor = parent
        parent = law.parent_map.get(parent)
        if not parent:
            error_msg = f'parent was not found for element {element.tag}:{element.text} in law {law.path}, ' \
                        f'last ancestor found is: {last_ancestor.tag}:{last_ancestor.text}'
            logging.debug(error_msg)
            raise Exception(error_msg)
    return classify_vertex_by_tag(parent.tag, parent, law)


def classify_vertex_by_tag_and_eid(tag, eids, to_law, from_law, from_element, errors_dict):
    if tag:
        for eid in eids:
            element = to_law.root.findall(f'.//{tag}[@eId="{eid}"]')
            if len(element) > 1:
                error_msg = Error.FOUND_MORE_THAN_ONE_EID.value.format(FULL_TO_SHORT_TAG[tag], eid, to_law.path)
                logging.error(error_msg)
                add_error_entry(errors_dict=errors_dict, error_msg=error_msg, error_type=Error.FOUND_MORE_THAN_ONE_EID.name, from_law=from_law, to_law=to_law, from_element=from_element, to_elements=element)
                return classify_vertex_by_tag(tag=Tag.Law, element=to_law.root, law=to_law)  # if we didn't find the element, we return a law vertex
            if element:
                element = element[0]
                return classify_vertex_by_tag(tag=tag, element=element, law=to_law)

        # unsuccessful classification
        error_msg = Error.DID_NOT_FIND_ELEMENT.value.format(FULL_TO_SHORT_TAG[tag], eids, to_law.path)
        logging.error(error_msg)
        add_error_entry(errors_dict=errors_dict, error_msg=error_msg, error_type=Error.DID_NOT_FIND_ELEMENT.name, from_law=from_law, to_law=to_law, from_element=from_element)
        return classify_vertex_by_tag(Tag.Law, to_law.root, to_law)  # if we didn't find the element, we return a law vertex

    else:
        # tag is empty then it's a law
        return classify_vertex_by_tag(tag=tag, element=to_law.root, law=to_law)


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


def classify_tag(eid, errors_dict, from_law, ref_element):
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
        error_msg = Error.DID_NOT_SUCCEED_TO_CLASSIFY_EID.value.format(eid, from_law.path)
        logging.error(error_msg)
        add_error_entry(errors_dict=errors_dict, error_msg=error_msg, error_type=Error.DID_NOT_SUCCEED_TO_CLASSIFY_EID.name, from_law=from_law, from_element=ref_element)
        return Tag.Law  # if didn't succeed to classify node's tag, return law's tag

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
