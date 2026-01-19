#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LostAndFound.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Modified: provide clearer instructions when Django is not importable
        raise ImportError(
            "Couldn't import Django. This usually means Django is not installed in the "
            "current Python environment or the virtual environment is not activated.\n\n"
            "If you use the project venv 'lostenv' on Windows, run:\n"
            "    d:\\LostAndFoundScratch\\LostAndFound\\lostenv\\Scripts\\activate\n"
            "then install dependencies:\n"
            "    pip install -r requirements.txt\n\n"
            "Or install Django directly:\n"
            "    pip install django\n\n"
            "If you are on Unix/macOS, activate with:\n"
            "    source lostenv/bin/activate\n"
            "and then install dependencies as above.\n\n"
            "Original import error: %s" % exc
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
