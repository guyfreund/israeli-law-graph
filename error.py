from constants import HREF

import enum
import json

ERRORS_FILE_PATH = 'errors.json'


class Error(enum.Enum):
    PATH_DOES_NOT_EXISTS = "Path {} does not exists in database"
    NO_LAW_FOUND = "No law found. Assuming law path is: {}/he@/main.xml"
    FOUND_MORE_THAN_ONE_EID = "Found more than one element {} with eid {} in to_law {}"
    DID_NOT_FIND_ELEMENT = "Didn't find element {} with the following possible eid's {} in to_law {}"
    DID_NOT_SUCCEED_TO_CLASSIFY_EID = "Didn't succeed to classify tag to eid {} in from_law {}"


def init_errors_dict():
    return {
        Error.PATH_DOES_NOT_EXISTS.name: [],
        Error.NO_LAW_FOUND.name: [],
        Error.FOUND_MORE_THAN_ONE_EID.name: [],
        Error.DID_NOT_FIND_ELEMENT.name: [],
        Error.DID_NOT_SUCCEED_TO_CLASSIFY_EID.name: []
    }


def get_error_object(error_msg, from_law, error_type, from_element, to_elements, to_law):
    if error_type == Error.PATH_DOES_NOT_EXISTS.name:
        return {
                'error_msg': error_msg,
                'from_law_path': from_law.path,
                'path_to_element_in_from_law': from_law.get_path_from_root(from_element),
                'href': from_element.attrib[HREF]
            }
    elif error_type == Error.NO_LAW_FOUND.name:
        return {
                'error_msg': error_msg,
                'from_law_path': from_law.path,
                'path_to_element_in_from_law': from_law.get_path_from_root(from_element),
                'href': from_element.attrib[HREF]
            }
    elif error_type == Error.FOUND_MORE_THAN_ONE_EID.name:
        return {
                'error_msg': error_msg,
                'from_law_path': from_law.path,
                'to_law_path': to_law.path,
                'path_to_element_in_from_law': from_law.get_path_from_root(from_element),
                'paths_to_elements_in_to_law': [to_law.get_path_from_root(to_element) for to_element in to_elements],
                'href': from_element.attrib[HREF]
            }
    elif error_type == Error.DID_NOT_FIND_ELEMENT.name:
        return {
                'error_msg': error_msg,
                'from_law_path': from_law.path,
                'to_law_path': to_law.path,
                'path_to_element_in_from_law': from_law.get_path_from_root(from_element),
                'href': from_element.attrib[HREF]
            }
    elif error_type == Error.DID_NOT_SUCCEED_TO_CLASSIFY_EID.name:
        return {
                'error_msg': error_msg,
                'from_law_path': from_law.path,
                'path_to_element_in_from_law': from_law.get_path_from_root(from_element),
                'href': from_element.attrib[HREF]
            }
    else:
        raise Exception('Unexpected Behavior')


def add_error_entry(errors_dict, error_msg, from_law, error_type, from_element, to_elements=None, to_law=None):
    errors_dict[error_type].append(get_error_object(
        error_msg=error_msg,
        from_law=from_law,
        error_type=error_type,
        from_element=from_element,
        to_elements=to_elements,
        to_law=to_law
    ))


def write_to_errors_file(errors_dict):
    with open(ERRORS_FILE_PATH, "w") as f:
        f.write(json.dumps(errors_dict, indent=4, ensure_ascii=False).encode('utf8').decode())
