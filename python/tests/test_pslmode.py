import subprocess
import sys
import os

def test_pslmode():
    script_path = os.path.join(os.path.dirname(__file__), '..', 'examples', 'pslmode.py')
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script {script} failed: {result.stderr}"
