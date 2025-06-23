from course_scheduler import Course, Section, solve_schedule, score_sections
from course_scheduler.solver import DEFAULT_WEIGHTS


def make_section(sid, day, loc="Campus"):
    return Section(id=sid, day=day, time="18:30 - 21:29", dates="", location=loc)


def test_score_sections():
    secs = [
        make_section("A", "Mer"),
        make_section("B", "Jeu"),
        make_section("C", "Lun", loc="B"),
    ]
    assert score_sections(secs) == 10 + 7 - 6 - 2


def test_preference_weight_ordering():
    assert score_sections([make_section("W", "Mer")]) == 10
    assert score_sections([make_section("T", "Jeu")]) == 7
    assert score_sections([make_section("F", "V")]) == 5


def test_penalty_monday_tuesday():
    assert score_sections([make_section("M", "Lun")]) == -6
    assert score_sections([make_section("Tu", "Ma")]) == -6


def test_location_penalty_multiple():
    secs = [
        make_section("A", "Mer", "X"),
        make_section("B", "Jeu", "Y"),
        make_section("C", "V", "Z"),
    ]
    assert score_sections(secs) == 10 + 7 + 5 - 2 * 2


def test_default_weights_include_prereq():
    assert "prereq" in DEFAULT_WEIGHTS


def test_local_search_improves_solution():
    c1 = Course(
        code="IFT1000",
        name="Intro",
        credits=3,
        sections=[make_section("A1", "Lun"), make_section("A2", "Mer")],
    )
    c2 = Course(
        code="IFT2000",
        name="Adv",
        credits=3,
        sections=[make_section("B1", "Ma")],
    )

    success, secs = solve_schedule([c1, c2])
    assert success
    days = {s.day for s in secs}
    assert "Mer" in days
    assert "Lun" not in days


def test_local_search_no_improvement():
    c = Course(
        code="IFT3000",
        name="X",
        credits=3,
        sections=[make_section("S1", "Mer"), make_section("S2", "Jeu")],
    )
    ok, sol = solve_schedule([c])
    assert ok
    assert {s.id for s in sol} == {"S1"}
