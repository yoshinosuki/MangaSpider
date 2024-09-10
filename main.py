import os
import time
import subprocess
import re
import sys

script_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_path)
script_path = script_path + '\\utils'


def validate_url(url):
    regex = r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
    return re.match(regex, url) is not None


def main():
    choice1 = input("Enter '1' to start from getting ID or enter '2' to continue from the last download progress\n")

    os.chdir(script_path)

    if choice1 == '1':
        choice2 = input(
            "Enter '1' to download using default category\nEnter '2' to download Chinese category\nEnter '3' to download uncensored Chinese category\nEnter '4' to download by using a url\n")

        if choice2 == '1':
            subprocess.run([sys.executable, os.path.join(script_path, "get_id.py")])
            time.sleep(3)
            subprocess.run([sys.executable, os.path.join(script_path, "handing.py")])
            time.sleep(3)
            subprocess.run([sys.executable, os.path.join(script_path, "download.py")])
            time.sleep(3)
            subprocess.run([sys.executable, os.path.join(script_path, "fix.py")])

        elif choice2 == '2':
            subprocess.run([sys.executable, os.path.join(script_path, "get_id.py"),
                            'https://nhentai.net/search/?q=pages%3A%3E100+%5Bchinese%5D&page='])
            time.sleep(3)
            subprocess.run([sys.executable, os.path.join(script_path, "handing.py")])
            time.sleep(3)
            subprocess.run([sys.executable, os.path.join(script_path, "download.py")])
            time.sleep(3)
            subprocess.run([sys.executable, os.path.join(script_path, "fix.py")])

        elif choice2 == '3':
            subprocess.run([sys.executable, os.path.join(script_path, "get_id.py"),
                            'https://nhentai.net/search/?q=pages%3A%3E60+uncensored+%5Bchinese%5D&page='])
            time.sleep(3)
            subprocess.run([sys.executable, os.path.join(script_path, "handing.py")])
            time.sleep(3)
            subprocess.run([sys.executable, os.path.join(script_path, "download.py")])
            time.sleep(3)
            subprocess.run([sys.executable, os.path.join(script_path, "fix.py")])

        elif choice2 == '4':
            while True:
                url = input("Enter URL: ")
                if validate_url(url):
                    subprocess.run([sys.executable, os.path.join(script_path, "get_id.py"), url])
                    time.sleep(3)
                    subprocess.run([sys.executable, os.path.join(script_path, "handing.py")])
                    time.sleep(3)
                    subprocess.run([sys.executable, os.path.join(script_path, "download.py")])
                    time.sleep(3)
                    subprocess.run([sys.executable, os.path.join(script_path, "fix.py")])
                    break  # Exit loop
                else:
                    print("The entered URL is invalid, please enter a valid URL.\n")

        else:
            print("Invalid input.")

    elif choice1 == '2':
        subprocess.run([sys.executable, os.path.join(script_path, "download.py")])
        time.sleep(3)
        subprocess.run([sys.executable, os.path.join(script_path, "fix.py")])

    else:
        print("Invalid input.")


if __name__ == "__main__":
    main()
