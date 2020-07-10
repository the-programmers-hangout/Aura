import os
import shutil

if __name__ == "__main__":
    if not os.path.exists("config.yaml"):
        shutil.copy("config.yaml.example", "config.yaml")
