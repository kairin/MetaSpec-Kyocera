#!/usr/bin/env python3
"""
Extracts model, sent date, and plain text body from a .eml file.
Usage: python3 extract_email_info.py <eml_file>
Prints a JSON object to stdout with keys: body, email_date, model
"""
import sys
import re
import json
from email import policy
from email.parser import BytesParser
from datetime import datetime

MODEL_NAMES = ["TASKalfa 5054ci", "TASKalfa 5004i"]

def extract_email_info(eml_path):
    with open(eml_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)
    # Extract plain text body
    body = msg.get_body(preferencelist=('plain'))
    if body:
        body = body.get_content()
    else:
        body = msg.get_body().get_content() if msg.get_body() else ''
    # Extract sent date
    sent_date = msg['date']
    try:
        email_dt = None
        if sent_date:
            from email.utils import parsedate_to_datetime
            email_dt = parsedate_to_datetime(sent_date)
        if email_dt:
            email_date_str = email_dt.strftime('%Y-%m-%d')
        else:
            email_date_str = datetime.now().strftime('%Y-%m-%d')
    except Exception:
        email_date_str = datetime.now().strftime('%Y-%m-%d')
    # Extract model name (look in subject and body)
    model = None
    subject = msg['subject'] or ''
    for m in MODEL_NAMES:
        if m in subject:
            model = m
            break
    if not model:
        for m in MODEL_NAMES:
            if m in body:
                model = m
                break
    if not model:
        match = re.search(r'Model Name:\s*(TASKalfa [\d]+ci|TASKalfa [\d]+i)', body)
        if match:
            model = match.group(1)
    return {"body": body, "email_date": email_date_str, "model": model}

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 extract_email_info.py <eml_file>", file=sys.stderr)
        sys.exit(1)
    info = extract_email_info(sys.argv[1])
    print(json.dumps(info, ensure_ascii=False))

if __name__ == "__main__":
    main()
