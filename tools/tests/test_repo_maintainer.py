import pytest

from tools.repo_maintainer import (
    GitHub,
    is_allowed_source_path,
    parse_model_response,
    validate_proposal,
)


def test_parse_model_response_accepts_json_code_fence():
    assert parse_model_response('```json\n{"action":"no_change"}\n```') == {
        "action": "no_change"
    }


def test_source_path_rejects_traversal_and_workflow_files():
    assert is_allowed_source_path("backend/app/main.py")
    assert not is_allowed_source_path("../outside.py")
    assert not is_allowed_source_path(".github/workflows/ci.yml")


def test_validate_proposal_only_allows_existing_source_files():
    files = {"app.py": "old = True\n"}
    proposal = {
        "action": "propose_change",
        "title": "Fix condition",
        "summary": "Correct the condition.",
        "files": [{"path": "app.py", "content": "old = False\n"}],
    }

    assert validate_proposal(proposal, files)["files"][0]["content"] == "old = False\n"

    proposal["files"][0]["path"] = ".github/workflows/ci.yml"
    with pytest.raises(ValueError):
        validate_proposal(proposal, files)


def test_validate_proposal_skips_unchanged_content():
    files = {"app.py": "value = 1\n"}
    proposal = {
        "action": "propose_change",
        "title": "Update value",
        "summary": "No actual difference.",
        "files": [{"path": "app.py", "content": "value = 1\n"}],
    }

    assert validate_proposal(proposal, files) is None


def test_source_files_uses_commit_tree_sha(monkeypatch):
    github = GitHub.__new__(GitHub)
    requests = []

    def fake_request(method, path, **kwargs):
        requests.append(path)
        if path.endswith("/branches/main"):
            return {"commit": {"sha": "commit-sha"}}
        if path.endswith("/git/commits/commit-sha"):
            return {"tree": {"sha": "tree-sha"}}
        if path.endswith("/git/trees/tree-sha"):
            return {"tree": []}
        raise AssertionError(f"Unexpected GitHub request: {path}")

    monkeypatch.setattr(github, "request", fake_request)
    base_sha, base_tree_sha, files = github.source_files(
        {"full_name": "owner/repo"}, "main"
    )

    assert base_sha == "commit-sha"
    assert base_tree_sha == "tree-sha"
    assert files == {}
    assert "/git/trees/tree-sha" in requests[-1]