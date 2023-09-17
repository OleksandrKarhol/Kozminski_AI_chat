from bs4 import BeautifulSoup

with open("table.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

table = soup.find('table')

table_contents = {'column_names' : [], 
                  'rows': []}
for child in table.children:
    if child.name == 'thead':
        descendants = [a for a in child.descendants if "th" in str(a) and 'tr' not in str(a)]
        for i in range(len(descendants)):
            column_name = descendants[i].string
            if column_name == None:
                table_contents['column_names'].append(f'Column {i}')
            else:
                table_contents['column_names'].append(f'{column_name.string}')
        
    elif child.name == 'tbody':
        tr_list = [a for a in child.children if 'td' in str(a)]

        for n in range(len(tr_list)):
            element = tr_list[n]
            table_contents['rows'].append({f'row {n}': []})
            td_list = [a for a in element.children if "td" in str(a)]

            for k in range(len(td_list)):
                cell_value = td_list[k].string
                table_contents['rows'][n][f'row {n}'].append(f'{table_contents["column_names"][k]} : {cell_value}')
            
    elif child != None:
        pass

print(table_contents)