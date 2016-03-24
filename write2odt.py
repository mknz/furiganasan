# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals
from odf.opendocument import OpenDocumentText
from odf.style import (Style, RubyProperties)
from odf.text import (P, Ruby, RubyBase, RubyText)
from odf import teletype
import re

TOKENS_KANJI = re.compile(u'[一-龠]+')  # kanji


def add_str(paragraph_element, string):
    """Add string to paragraph element."""
    teletype.addTextToElement(paragraph_element, string)


def add_rubi(paragraph_element, str_base, str_rubi):
    """Add rubi to paragraph element."""
    rubi_element = Ruby(stylename="Rubi1")
    rubi_element.addElement(RubyBase(text=str_base))
    rubi_element.addElement(RubyText(text=str_rubi))
    paragraph_element.addElement(rubi_element)


def create_paragraph(string):
    """Create a paragraph element with rubi text."""
    paragraph_element = P()
    while 1:
        m = re.search(TOKENS_KANJI, string)  # detect kanji start position
        if m is not None:  # if first part of the string is non-kanji
            add_str(paragraph_element, string[:m.start()])
            string = string[m.start():]  # truncate non-kanji

        m = re.match(r'(.*?)\((.*?)\)(.*)', string)
        if m is None:
            add_str(paragraph_element, string)
            break
        else:
            add_rubi(paragraph_element, m.group(1), m.group(2))
            string = m.group(3)

    return paragraph_element


def convert_and_save(text, filename):
    textdoc = OpenDocumentText()

    # Useless: This style setting is somehow overwritten by LibreOffice
    '''
    rubistyle = Style(name="Rubi1", family="ruby")
    rubistyle.addElement(RubyProperties(attributes={"rubyalign": "center", "rubyposition": "above"}))

    textdoc.styles.addElement(rubistyle)
    '''

    lines = text.splitlines()
    for line in lines:
        paragraph_element = create_paragraph(line)
        textdoc.text.addElement(paragraph_element)

    textdoc.save(filename)
