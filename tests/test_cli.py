from types import SimpleNamespace

import pytest

from test_automation_prioritization import cli
from test_automation_prioritization.models import (
    TestCaseAssessment as Assessment,
)

RESPONSES = (
    "API", "YES", "YES", "YES", "HIGH", "ORDINARY",
    "FREQUENT", "YES", "LOW", "LOW",
)


def test_collect_assessment_maps_answers_to_model(monkeypatch):
    answers = iter(RESPONSES)
    monkeypatch.setattr(cli, "select_answer", lambda message, options: next(answers))
    monkeypatch.setattr(cli, "show_header", lambda title: None)

    assessment = cli.collect_assessment()

    assert assessment == Assessment(
        test_type="API",
        oracle="YES",
        repeatability="YES",
        access="YES",
        impact="HIGH",
        likelihood="ORDINARY",
        cadence="FREQUENT",
        distinct_coverage="YES",
        implementation_effort="LOW",
        maintenance="LOW",
    )


def test_likelihood_options_map_ordinary_to_internal_value(monkeypatch):
    captured = {}

    def fake_select(message, options):
        captured["options"] = options
        return "ORDINARY"

    monkeypatch.setattr(cli, "select_answer", fake_select)

    assert cli.ask_likelihood() == "ORDINARY"
    assert any(
        value == "ORDINARY" and "Ordinary" in label
        for label, value in captured["options"]
    )


def test_cancelling_a_question_exits_cleanly(monkeypatch, capsys):
    fake_question = SimpleNamespace(ask=lambda: None)
    monkeypatch.setattr(cli.questionary, "print", lambda message, **kwargs: print(message))

    with pytest.raises(SystemExit) as exc:
        cli.ask(fake_question)

    assert exc.value.code == 0
    assert "Evaluation cancelled by user" in capsys.readouterr().out


def test_result_hides_internal_oracle_and_rule_id(monkeypatch, capsys):
    monkeypatch.setattr(cli, "show_header", lambda title: print(title))
    monkeypatch.setattr(cli.questionary, "print", lambda message, **kwargs: print(message))
    result = SimpleNamespace(
        verdict="KEEP_MANUAL",
        test_type="UI",
        reason="The test cannot currently be automated reliably.",
        supporting_factors=("No reliable automated test oracle",),
        next_step="Maintain manual validation.",
        limitations=("oracle: NO", "access: UNKNOWN"),
        triggered_rule="R2",
    )

    cli.show_result(result)
    output = capsys.readouterr().out

    assert "KEEP_MANUAL" in output
    assert "The expected result cannot be verified reliably" in output
    assert "Required tools, environments, and system access: Not enough information" in output
    assert "oracle: NO" not in output
    assert "test oracle" not in output.lower()
    assert "Decision Rule" not in output
    assert "R2" not in output
    assert output.count("The expected result cannot be verified reliably") == 1


def test_main_passes_assessment_to_evaluator_and_displays_result(monkeypatch):
    assessment = Assessment(
        test_type="API", oracle="YES", repeatability="YES", access="YES",
        impact="HIGH", likelihood="ORDINARY", cadence="FREQUENT",
        distinct_coverage="YES", implementation_effort="LOW", maintenance="LOW",
    )
    expected_result = object()
    calls = []

    monkeypatch.setattr(cli, "show_intro", lambda: calls.append("intro"))
    monkeypatch.setattr(cli, "collect_assessment", lambda: assessment)

    def fake_evaluate(received):
        assert received is assessment
        calls.append("evaluate")
        return expected_result

    monkeypatch.setattr(cli, "evaluate", fake_evaluate)
    monkeypatch.setattr(cli, "show_result", lambda value: calls.append(("result", value)))

    cli.main()

    assert calls == ["intro", "evaluate", ("result", expected_result)]