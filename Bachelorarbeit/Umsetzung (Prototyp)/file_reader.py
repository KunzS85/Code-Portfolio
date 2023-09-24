import os
from typing import List, Any, Set, Dict, Tuple, Optional
import fitz

def read_txt(url: str) -> str:
    """
    Requires the specification of the directory of the document
    (Could also be shortened so that directory and file are specified)
    :param txt_dir: directory url from the textfile
    :return: returns the entire text of the document as a string
    """
    content = ""
    with open(url, 'r') as f:
        lines = f.readlines()
    for line in lines:
        content = content + line
    return content


def read_pdf(url: str):
    """
    This method reads a PDF document and returns it as a string for further processing
    :param url: URL including name and file type designation (.pdf) of the document to be read
    :return: a string which represents the whole content of the document
    """
    doc = fitz.open(url)
    txt = ""
    for p in range(len(doc)):
        page = doc[p]
        #print(page)
        text = page.get_text("text")
        #print(text)
        txt = txt + text
    return txt
