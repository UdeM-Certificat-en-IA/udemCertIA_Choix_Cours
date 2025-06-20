from course_scheduler import Course, Section, solve_schedule, score_sections


def make_section(sid, day, loc="Campus"):
    return Section(id=sid, day=day, time="18:30 - 21:29", dates="", location=loc)


def test_score_sections():
    secs = [
        make_section("A", "Mer"),
        make_section("B", "Jeu"),
        make_section("C", "Lun", loc="B"),
    ]
    assert score_sections(secs) == 10 + 7 - 6 - 2


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
