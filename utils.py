from constants import ANCESTOR_TAGS, LAW_SUFFIX, Suffix, Tag, SUFFIX_TO_TAG, HREF, APPENDIX_NUM_TO_HEB, \
    CHAPTER_NUM_TO_HEB, FULL_TO_SHORT_TAG
from classes import Chapter, Part, Point, Preamble, Appendix, Section, Law, Subtitle, WrapUp
from error import Error, add_error_entry

import os
import glob
import logging


def parse_ref(ref_element, from_law, errors_dict):
    """ Parses the raw reference text into FRBRWorkURI prefix and element identifier suffix """
    raw_href = ref_element.attrib[HREF]

    if raw_href.startswith('#'):
        href = f'{from_law.frbr_work_uri}{raw_href}'
    elif raw_href.startswith('/'):
        href = raw_href[1:]
    else:
        href = raw_href

    frbr_work_uri, eid = split_ref(href)  # Get FRBRWorkURI prefix and element identifier suffix

    if not os.path.exists(frbr_work_uri):  # Find out if FRBRWorkURI directory is in database
        error_msg = Error.PATH_DOES_NOT_EXISTS.value.format(frbr_work_uri)
        logging.error(error_msg)
        add_error_entry(
            errors_dict=errors_dict, error_msg=error_msg, from_law=from_law,
            error_type=Error.PATH_DOES_NOT_EXISTS.name, from_element=ref_element
        )
        return str(), str()

    if not os.path.exists(os.path.join(frbr_work_uri, LAW_SUFFIX)):  # Find out if law xml file is not in database
        error_msg = Error.NO_LAW_FOUND.value.format(os.path.join(frbr_work_uri, LAW_SUFFIX))
        logging.error(error_msg)
        add_error_entry(
            errors_dict=errors_dict, error_msg=error_msg, from_law=from_law,
            error_type=Error.NO_LAW_FOUND.name, from_element=ref_element
        )
        return str(), str()

    return frbr_work_uri, eid


def get_ref_ancestor_element(law, element, vertexes_map):
    """ Search for the reference element's ancestor that is tagged by one of ANCESTOR_TAGS """
    parent = law.parent_map.get(element)
    while parent and parent.tag not in ANCESTOR_TAGS:
        last_ancestor = parent
        parent = law.parent_map.get(parent)
        if not parent:
            error_msg = f'parent was not found for element {element.tag}:{element.text} in law {law.path}, ' \
                        f'last ancestor found is: {last_ancestor.tag}:{last_ancestor.text}'
            logging.exception(error_msg)
            raise Exception(error_msg)
    return create_vertex_by_tag(parent.tag, parent, law, vertexes_map)


def classify_vertex_by_tag_and_eid(tag, eids, to_law, from_law, from_element, errors_dict, vertexes_map):
    """ Searches for an element tagged by `tag` and one of the potential eids """
    if tag:
        for eid in eids:
            element = to_law.root.findall(f'.//{tag}[@eId="{eid}"]')
            if len(element) > 1:
                error_msg = Error.FOUND_MORE_THAN_ONE_EID.value.format(FULL_TO_SHORT_TAG[tag], eid, to_law.path)
                logging.error(error_msg)
                add_error_entry(
                    errors_dict=errors_dict, error_msg=error_msg, error_type=Error.FOUND_MORE_THAN_ONE_EID.name,
                    from_law=from_law, to_law=to_law, from_element=from_element, to_elements=element
                )
                # if we didn't find the element, we return a law vertex
                return create_vertex_by_tag(tag=Tag.Law, element=to_law.root, law=to_law, vertexes_map=vertexes_map)
            if element:
                element = element[0]  # Should be only one element due to hashing
                return create_vertex_by_tag(tag=tag, element=element, law=to_law, vertexes_map=vertexes_map)

        # unsuccessful classification
        error_msg = Error.DID_NOT_FIND_ELEMENT.value.format(FULL_TO_SHORT_TAG[tag], eids, to_law.path)
        logging.error(error_msg)
        add_error_entry(
            errors_dict=errors_dict, error_msg=error_msg, error_type=Error.DID_NOT_FIND_ELEMENT.name, from_law=from_law,
            to_law=to_law, from_element=from_element
        )
        # if we didn't find the element, we return a law vertex
        return create_vertex_by_tag(Tag.Law, to_law.root, to_law, vertexes_map=vertexes_map)

    else:
        # tag is empty then it's a law
        return create_vertex_by_tag(tag=tag, element=to_law.root, law=to_law, vertexes_map=vertexes_map)


def create_vertex_by_tag(tag, element, law, vertexes_map):
    """ Creates a Vertex inherited object by a Tag """
    if tag == Tag.Chapter:
        vertex = Chapter(law, element)
    elif tag == Tag.Point:
        vertex = Point(law, element)
    elif tag == Tag.Section:
        vertex = Section(law, element)
    elif tag == Tag.Part:
        vertex = Part(law, element)
    elif tag == Tag.Appendix:
        vertex = Appendix(law, element)
    elif tag == Tag.Preamble:
        vertex = Preamble(law, element)
    elif tag == Tag.Subtitle:
        vertex = Subtitle(law, element)
    elif tag == Tag.WrapUp:
        vertex = WrapUp(law, element)
    elif tag == Tag.Law:
        vertex = law
    else:
        raise Exception('Unexpected behavior')

    vertex_hash = hash(vertex)
    if vertex_hash in vertexes_map:
        return vertexes_map[vertex_hash]
    else:
        vertexes_map[vertex_hash] = vertex
        return vertex


def classify_tag(eid, errors_dict, from_law, ref_element):
    """ Classify the vertex's Tag from the reference's element identifier
    For an example, the string '{Suffix.Chaper}_{Suffix.Point}' will be tagged as Tag.Point

    """
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
        add_error_entry(
            errors_dict=errors_dict, error_msg=error_msg, error_type=Error.DID_NOT_SUCCEED_TO_CLASSIFY_EID.name,
            from_law=from_law, from_element=ref_element
        )
        return Tag.Law  # if didn't succeed to classify node's tag, return law's tag

    locations = [eid.find(suffix) for suffix in potential_suffixes]
    last_location = max(locations)
    last_location_index = locations.index(last_location)
    return SUFFIX_TO_TAG[potential_suffixes[last_location_index]]


def classify_eid_by_tag(tag, eid):
    """ There are a lot of eid mistakes. This function tries to deal with them.
    For Appendix and Chapter eids we try to convert Hebrew characters to numbers.
    """
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
    """ Builds a map data-structure that maps a FRBRWorkURI to its Law object """
    laws = []
    frbr_work_uri_to_law = {}
    for law_path in glob.glob(f'akn/**/*.xml', recursive=True):
        law = Law(law_path)
        frbr_work_uri_to_law[law.frbr_work_uri] = law
        laws.append(law)
    return laws, frbr_work_uri_to_law
