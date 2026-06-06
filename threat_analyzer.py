def analyze_threat(model, content):

    prompt = f"""
You are a Senior SOC Analyst.

Analyze the following content.

Provide:

1. Threat Type
2. Severity
3. Risk Score (0-100)
4. MITRE ATT&CK Technique
5. Indicators of Compromise
6. Explanation
7. Recommended Actions

Content:
{content}
"""

    response = model.generate_content(prompt)

    return response.text