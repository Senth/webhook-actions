import pytest
from mockito import mock, unstub, verifyStubbedInvocationsAreUsed, when

from ...core.entities.action import Action
from .run import RunOutput, Run
from .run_repo import RunRepo


@pytest.fixture
def mock_repo():
    return mock(RunRepo)


@pytest.fixture
def action():
    return Action("this/is/my/path", "some data")


def test_run_successful(mock_repo, action):
    when(mock_repo).exists(...).thenReturn(True)
    when(mock_repo).run(...).thenReturn(True)

    run = Run(mock_repo)
    output = run.execute(action)

    assert output == RunOutput.success

    verifyStubbedInvocationsAreUsed()
    unstub()


def test_run_failed(mock_repo, action):
    when(mock_repo).exists(...).thenReturn(True)
    when(mock_repo).run(...).thenReturn(False)

    run = Run(mock_repo)
    output = run.execute(action)

    assert output == RunOutput.fail

    verifyStubbedInvocationsAreUsed()
    unstub()


def test_run_script_not_found(mock_repo, action):
    when(mock_repo).exists(...).thenReturn(False)

    run = Run(mock_repo)
    output = run.execute(action)

    assert output == RunOutput.not_found

    verifyStubbedInvocationsAreUsed()
    unstub()
