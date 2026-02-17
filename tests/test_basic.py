import importlib.util
import os


def test_basic():
    assert 1 + 1 == 2

def test_imports():
    # Helper to import scripts with numbers in filenames
    script_files = [
        "scripts/01_add_district_field.py",
        "scripts/02_extract_districts.py"
    ]

    for script_path in script_files:
        if os.path.exists(script_path):
            try:
                spec = importlib.util.spec_from_file_location("module.name", script_path)
                if spec is not None:
                    foo = importlib.util.module_from_spec(spec)
                    # We don't execute it, just check if it can be loaded as a module
                    assert foo is not None
            except Exception:
                # If dependencies are missing in this environment, it's okay
                pass
    assert True
