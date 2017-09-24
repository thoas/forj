import re

CRITERIA_SEPARATOR = '-'
RANGE_CRITERIA_SEPARATOR = '/'
CHOICE_CRITERIA_SEPARATOR = '|'

criteria_regex = re.compile(r'(?P<name>\w+)\((?P<value>[\w\{}\{}]+)\)'.format(RANGE_CRITERIA_SEPARATOR, CHOICE_CRITERIA_SEPARATOR))


class CriteriaSet(object):
    def __init__(self, criterias):
        self.criterias = criterias

    @classmethod
    def from_reference(cls, reference,
                       separator=CRITERIA_SEPARATOR):

        segments = reference.split(separator)

        return cls([get_criteria_class(segment).from_segment(segment)
                    for segment in segments])

    def __len__(self):
        return len(self.criterias)


class Criteria(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    @classmethod
    def from_segment(cls, segment):
        match = criteria_regex.match(segment)

        if not match:
            return None

        return cls(name=match.group('name'),
                   value=match.group('value'))

    def __repr__(self):
        return '<{}: {}:{}>'.format(self.__class__.__name__,
                                    self.name,
                                    self.value)

    def __eq__(self, criteria):
        return criteria.name == self.name and criteria.value == self.value

    def __contains__(self, value):
        return self == value


class RangeCriteria(Criteria):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        start, end = self.value.split(RANGE_CRITERIA_SEPARATOR)

        self.value = range(int(start), int(end) + 1)

    def __eq__(self, criteria):
        return criteria.name == self.name and int(criteria.value) in self.value


class ChoiceCriteria(Criteria):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.value = self.value.split(CHOICE_CRITERIA_SEPARATOR)

    def __eq__(self, criteria):
        return criteria.name == self.name and criteria.value in self.value


def get_criteria_class(segment):
    if RANGE_CRITERIA_SEPARATOR in segment:
        return RangeCriteria

    if CHOICE_CRITERIA_SEPARATOR in segment:
        return ChoiceCriteria

    return Criteria
