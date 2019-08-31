#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    # print('程序启动之后使用浏览器访问 http://127.0.0.1/index')
    # print('启动中，请稍后.....')
    # print()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PedestriansDetection.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
    # os.system('pause') #按任意键继续


if __name__ == '__main__':
    main()
