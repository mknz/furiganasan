# -*- coding: utf-8 -*-
import re

TOKENS_KANJI = re.compile(u'[一-龠]+')  # kanji


def create_rubi_paragraph(string):
    """Create rubi tagged html."""
    html = "<p>"
    while 1:
        m = re.search(TOKENS_KANJI, string)  # detect kanji start position
        if m is not None:  # if first part of the string is non-kanji
            html += string[:m.start()]
            string = string[m.start():]  # truncate non-kanji

        m = re.match(r'(.*?)\((.*?)\)(.*)', string)
        if m is None:
            html += string
            break
        else:
            html += "<ruby>" + m.group(1)
            html += "<rp>(</rp><rt>" + m.group(2) + "</rt><rp>)</rp>"
            html += "</ruby>"
            string = m.group(3)

    html += "</p>"
    return html


def convert(text):
    lines = text.splitlines()
    html = ""
    for line in lines:
        html += create_rubi_paragraph(line)
        html += "\n"

    return html
