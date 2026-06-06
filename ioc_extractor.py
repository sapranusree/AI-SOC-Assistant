import re

def extract_iocs(text):

    ips = re.findall(
        r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
        text
    )

    urls = re.findall(
        r"https?://[^\s]+",
        text
    )

    emails = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    domains = []

    for url in urls:

        domain = (
            url.replace("https://", "")
               .replace("http://", "")
               .split("/")[0]
        )

        domains.append(domain)

    return {
        "ips": list(set(ips)),
        "urls": list(set(urls)),
        "emails": list(set(emails)),
        "domains": list(set(domains))
    }