#!/usr/bin/env python3
"""
Generates .txt and .pdf files from email info.
Usage: python3 generate_output_files.py <body_file> <output_base>
- <body_file>: path to a text file containing the email body
- <output_base>: base path (without extension) for output files
Creates <output_base>.txt and <output_base>.pdf
"""
import sys
from fpdf import FPDF

def save_txt(body, out_path):
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(body)

def save_pdf(body, out_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in body.splitlines():
        pdf.cell(0, 10, line, ln=1)
    pdf.output(out_path)

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 generate_output_files.py <body_file> <output_base>", file=sys.stderr)
        sys.exit(1)
    body_file, output_base = sys.argv[1], sys.argv[2]
    with open(body_file, 'r', encoding='utf-8') as f:
        body = f.read()
    save_txt(body, output_base + '.txt')
    save_pdf(body, output_base + '.pdf')

if __name__ == "__main__":
    main()
