def parse_logs(content):

    findings = []

    text = content.lower()

    if text.count("failed login") >= 5:
        findings.append(
            "Possible Brute Force Attack Detected"
        )

    if "port scan" in text:
        findings.append(
            "Possible Port Scanning Activity"
        )

    if "ransomware" in text:
        findings.append(
            "Potential Ransomware Activity"
        )

    if "malware" in text:
        findings.append(
            "Potential Malware Activity"
        )

    if not findings:
        findings.append(
            "No obvious threats detected"
        )

    return findings