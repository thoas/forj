from forj.criteria import CriteriaSet, Criteria, RangeCriteria, ChoiceCriteria


def test_criteria_from_segment():
    segments = {
        'LA(50)': ('LA', '50'),
        'LO(25)': ('LO', '25'),
        'P(AGLO)': ('P', 'AGLO'),
        'H(40)': ('H', '40'),
        'R(0000)': ('R', '0000'),
    }

    for segment, values in segments.items():
        criteria = Criteria.from_segment(segment)

        assert criteria is not None
        assert criteria.name == values[0]
        assert criteria.value == values[1]


def test_criteria_eq():
    c1 = Criteria.from_segment('LA(50)')
    assert c1 is not None

    c2 = Criteria.from_segment('LA(50)')
    assert c2 is not None

    assert c1 == c2


def test_criteria_contains():
    c1 = Criteria.from_segment('LA(50)')
    assert c1 is not None

    c2 = Criteria.from_segment('LA(50)')
    assert c2 is not None

    assert c1 in c2


def test_range_criteria_contains():
    c1 = RangeCriteria.from_segment('LA(50/100)')
    assert c1 is not None

    c2 = Criteria.from_segment('LA(50)')
    assert c2 is not None

    assert c2 in c1


def test_choice_criteria_contains():
    c1 = ChoiceCriteria.from_segment('R(0000|0202)')
    assert c1 is not None

    c2 = Criteria.from_segment('R(0000)')
    assert c2 is not None

    assert c2 in c1


def test_criteria_set_from_reference():
    reference = 'LA(50)-LO(25)-P(AGLO)-H(40)-R(0000)'

    criteria_set = CriteriaSet.from_reference(reference)

    assert len(criteria_set) == 5


def test_criteria_set_contains():
    c0 = CriteriaSet.from_reference('LO(25)-LA(50)-H(40)-R(0000)-P(AGLO)')
    c1 = CriteriaSet.from_reference('LA(50)-LO(25)-P(AGLO)-H(40)-R(0000)')
    c2 = CriteriaSet.from_reference('LA(50)-LO(25)-P(AGLO)-H(40)-R(0001)')
    c3 = CriteriaSet.from_reference('LA(101)-LO(25)-P(AGLO)-H(40)-R(0001)')
    c4 = CriteriaSet.from_reference('LA(100)-LO(25)-P(AGLO)-H(40)-R(0002)')
    c5 = CriteriaSet.from_reference('LA(100)-LO(25)-P(AGLO)-H(40)-R(0001)')
    crange = CriteriaSet.from_reference('LA(25/100)-LO(25/100)-P(AGLO)-H(40/120)-R(0000|0001)')

    assert c0 in crange
    assert c1 in crange
    assert c2 in crange
    assert c5 in crange
    assert c3 not in crange
    assert c4 not in crange
