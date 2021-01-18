from constants import Tag
from classes import Chapter, Point, Section, Part, Appendix, Preamble, Subtitle, WrapUp
from utils import build_laws_mapping


def validate_laws(laws):
    laws_set = set()
    laws_list = list()
    total_laws = 0
    duplicates = list()

    for law in laws:
        total_laws += 1
        laws_list.append(law)
        if law in laws_set:
            duplicates.append(law)
        laws_set.add(law)

    assert len(laws_set) == len(laws_list) == total_laws
    assert not duplicates


def validate_class(laws, class_object, tag):
    instances_set = set()
    instances_list = list()
    total_instances = 0
    duplicates = list()

    for law in laws:
        for instance in [class_object(law, x) for x in law.root.findall(f'.//{tag}')]:
            total_instances += 1
            instances_list.append(instance)
            if instance in instances_set:
                duplicates.append([instance, instance.law_path, instance.element.attrib['eId']])
            instances_set.add(instance)

    assert len(instances_set) == len(instances_list) == total_instances
    assert not duplicates


def validate(laws):
    validate_laws(laws)
    validate_class(laws, Chapter, Tag.Chapter)
    validate_class(laws, Point, Tag.Point)
    validate_class(laws, Section, Tag.Section)
    validate_class(laws, Part, Tag.Part)
    validate_class(laws, Appendix, Tag.Appendix)
    validate_class(laws, Preamble, Tag.Preamble)
    validate_class(laws, Subtitle, Tag.Subtitle)
    validate_class(laws, WrapUp, Tag.WrapUp)


def main():
    laws, _ = build_laws_mapping()
    validate(laws)


if __name__ == '__main__':
    main()
