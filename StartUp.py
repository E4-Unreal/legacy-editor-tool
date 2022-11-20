import sys

# Custom 폴더 경로
module_path = "경로/Custom"
if not module_path in sys.path:
    sys.path.append(module_path)