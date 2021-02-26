LAW_SUFFIX = 'he@/main.xml'
XML_NAMESPACE = '{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}'
HREF = "href"


class Suffix(object):
    Law = ""
    Chapter = "chp"
    Point = "point"
    Section = "sec"
    Part = "part"
    Appendix = "appendix"
    Preamble = "preamble"
    Subtitle = "subtitle"
    WrapUp = "wrapup"


class Tag(object):
    Law = ""
    Chapter = f"{XML_NAMESPACE}chapter"
    Point = f"{XML_NAMESPACE}point"
    Section = f"{XML_NAMESPACE}section"
    Part = f"{XML_NAMESPACE}part"
    Appendix = f"{XML_NAMESPACE}appendix"
    Preamble = f"{XML_NAMESPACE}preamble"
    Subtitle = f"{XML_NAMESPACE}subtitle"
    WrapUp = f"{XML_NAMESPACE}wrapup"
    Act = f"{XML_NAMESPACE}act"


class EdgeType(object):
    Generic = "generic"
    Section_of_law = "סעיף של חוק"
    Sub_section_of_section = "תת-סעיף של סעיף"  # Not used
    Reference_to_another_law = "הפנייה לחוק אחר"
    Reference_to_section_of_another_law = "הפנייה לסעיף של חוק אחר"
    Law_Preamble = "הקדמה לחוק"
    No_Type = "סתמי"


SUFFIX_TO_TAG = {
    Suffix.Law: Tag.Law,
    Suffix.Chapter: Tag.Chapter,
    Suffix.Point: Tag.Point,
    Suffix.Section: Tag.Section,
    Suffix.Part: Tag.Part,
    Suffix.Appendix: Tag.Appendix,
    Suffix.Preamble: Tag.Preamble,
    Suffix.Subtitle: Tag.Subtitle,
    Suffix.WrapUp: Tag.WrapUp
}


TAG_TO_SUFFIX = {
    Tag.Law: Suffix.Law,
    Tag.Chapter: Suffix.Chapter,
    Tag.Point: Suffix.Point,
    Tag.Section: Suffix.Section,
    Tag.Part: Suffix.Part,
    Tag.Appendix: Suffix.Appendix,
    Tag.Preamble: Suffix.Preamble,
    Tag.Subtitle: Suffix.Subtitle,
    Tag.WrapUp: Suffix.WrapUp
}


FULL_TO_SHORT_TAG = {
    Tag.Law: "law",
    Tag.Chapter: "chapter",
    Tag.Point: "point",
    Tag.Section: "section",
    Tag.Part: "part",
    Tag.Appendix: "appendix",
    Tag.Preamble: "preamble",
    Tag.Subtitle: "subtitle",
    Tag.WrapUp: "wrapup"
}


APPENDIX_NUM_TO_HEB = {
    "1": "ראשונה",
    "2": ["שנייה", "שניה"],
    "3": "שלישית",
    "4": "רביעית",
    "5": "חמישית",
    "6": "שישית",
    "7": "שביעית",
    "8": "שמינית",
    "9": "תשיעית"
}


CHAPTER_NUM_TO_HEB = {
    "1": "ראשון",
    "2": "שני",
    "3": "שלישי",
    "4": "רביעי",
    "5": "חמישי",
    "6": ["שישי", "ששי"],
    "7": "שביעי",
    "8": "שמיני",
    "9": "תשיעי",
    "10": "עשירי",
    "11": "אחד־עשר",
    "12": "שנים־עשר",
    "13": "שלושה־עשר",
    "15": "חמישה־עשר",
    "16": "ששה־עשר",
    "17": "שבעה־עשר",
    "18": "שמונה־עשר"
}


ANCESTOR_TAGS = [Tag.Chapter, Tag.Point, Tag.Section, Tag.Part, Tag.Appendix, Tag.Preamble, Tag.Subtitle, Tag.WrapUp]

