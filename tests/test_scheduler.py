from course_scheduler import Course, Section, solve_schedule


def make_section(sid, day, time):
    return Section(id=sid, day=day, time=time, dates="", location="Online")


def test_section_conflict_detection():
    a = make_section("A", "Lun", "18:30 - 21:29")
    b = make_section("B", "Lun", "20:00 - 22:30")
    c = make_section("C", "Ma", "18:30 - 21:29")

    assert a.conflicts_with(b)
    assert b.conflicts_with(a)
    assert not a.conflicts_with(c)


def test_solver_finds_non_conflicting_schedule():
    # Course 1 offer two overlapping sections; solver should pick "IFT1400-B"
    c1 = Course(
        code="IFT1400",
        name="Intro IA",
        credits=3,
        sections=[
            make_section("IFT1400-A", "Lun", "18:30 - 21:29"),
            make_section("IFT1400-B", "Ma", "18:30 - 21:29"),
        ],
    )

    # Course 2 has a single section on Monday evening – conflicts with IFT1400-A
    c2 = Course(
        code="IFT1410",
        name="IA générative",
        credits=3,
        sections=[make_section("IFT1410-A", "Lun", "18:30 - 21:29")],
    )

    success, selected = solve_schedule([c1, c2])

    assert success, "Solver should find a valid schedule"

    # Ensure the chosen sections are indeed non-conflicting
    ids = {s.id for s in selected}
    assert "IFT1400-B" in ids
    assert "IFT1410-A" in ids
    assert "IFT1400-A" not in ids

