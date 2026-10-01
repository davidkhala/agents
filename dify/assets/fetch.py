import ssl
import urllib.request


def main(url: str):
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(url, context=context) as response:
        return {
            'html': response.read().decode("utf-8", errors="ignore")
        }
