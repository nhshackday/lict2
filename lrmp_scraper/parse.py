#!/usr/bin/env python
import pdb
from bs4 import BeautifulSoup

inputFile = 'result2.html'

with open('./example-html/' + inputFile, 'r') as f_in:
    html_doc = f_in.read()
    #pdb.set_trace()
    doc = BeautifulSoup(html_doc)

    info = []
    for td in doc.find_all('td'):
        if td.get('class') and td.get('class')[0] == 'listapplettablerows':
            info.append(td)

    column = 0
    #keys = ['GMC Ref Number', 'Given Names', 'Surname', 'Status', 'Prov Reg Date', 'Full Reg Date', 'Annual Fee Due Date', '']
    # split on every 7th
    with open('./example-output.csv', 'w') as f_out:
        for result in info:
            f_out.write(result.text + ', ')
            column += 1
            if column == 7:
                f_out.write('\n')
                column = 0

