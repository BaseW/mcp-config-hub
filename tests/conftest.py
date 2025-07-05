import pytest


@pytest.fixture(autouse=True)
def patch_home_and_cwd(tmp_path, monkeypatch):
    # Patch HOME and CWD to tmp_path for isolation
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    yield
