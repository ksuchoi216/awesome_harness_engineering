import subprocess
import os

def test_detect_stale_tests_no_signal_without_legacy(tmp_path):
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_ahe_new.py").write_text("# keeper")
    
    detector_script = os.path.abspath("packages/ahe-codex/.codex/skills/ahe-compress/scripts/detect_stale_tests.py")
    
    result = subprocess.run(["python", detector_script], cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 0
    assert "TEST_COMPRESSION_REQUIRED" not in result.stdout

def test_detect_stale_tests_signals_with_legacy(tmp_path):
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_new_workflow.py").write_text("# legacy")
    (tests_dir / "test_ahe_new.py").write_text("# keeper")
    
    detector_script = os.path.abspath("packages/ahe-codex/.codex/skills/ahe-compress/scripts/detect_stale_tests.py")
    
    result = subprocess.run(["python", detector_script], cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 2
    assert "TEST_COMPRESSION_REQUIRED" in result.stdout
    assert "REVIEW_TEST\ttests/test_new_workflow.py\tcovered_by=tests/test_ahe_new.py" in result.stdout
