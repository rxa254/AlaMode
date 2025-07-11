import subprocess
import sys
import os

def test_customcostexample():
    script_path = os.path.join(os.path.dirname(__file__), '..', 'examples', 'customcostexample.py')
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script {script_path} failed: {result.stderr}"
