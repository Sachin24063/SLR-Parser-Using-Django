from .global_vars import grammar, lr0_items, nonterms, symbols, terms
from .slr_helpers import get_closure, get_first, get_follow


def display(start, error, parse_table):
    global grammar, lr0_items, nonterms, symbols, terms
    print('Grammar')

    for head, prods in grammar.items():
        if head == start:
            continue

        print('{:>{width}} ->'.format(head,
                                      width=len(
                                          max(list(grammar.keys()), key=len))),
              end=' ')

        nprods = 0

        for prod in prods:
            if nprods > 0:
                print('|', end=' ')

            for char in prod:
                print(char, end=' ')

            nprods += 1

        print()

    print('\nAugmented Grammar')
    i = 0
    
    augmented_grammer = ""

    for head, prods in grammar.items():
        for prod in prods:
            print('{:>{width}} ->'.format(head,
                                          width=len(
                                              max(list(grammar.keys()),
                                                  key=len))),
                  end=' ')
            augmented_grammer += '{:>{width}} ->'.format(head,
                                          width=len(
                                              max(list(grammar.keys()),
                                                  key=len))) + " "

            for char in prod:
                print(char, end=' ')
                augmented_grammer += char + " "

            print()
            augmented_grammer += "\n"
            i += 1

    print('\nTerminals   :', terms)
    print('Nonterminals:', nonterms)
    print('Symbols     :', symbols)

    print('\nFirst')
    
    first = []

    for head in grammar:
        print('{:>{width}} ='.format(head,
                                     width=len(
                                         max(list(grammar.keys()), key=len))),
              end=' ')
        
        temp = []
        print('{', end=' ')
        nterms = 0

        for term in get_first(head):
            if nterms > 0:
                print(', ', end=' ')
            print(term, end=' ')
            temp.append(term)
            nterms += 1

        print('}')
        
        first.append({
                "symbol" : head,
                "first" : temp
            }
        )

    print('\nFollow')
    
    follow = []

    for head in grammar:
        print('{:>{width}} ='.format(head,
                                     width=len(
                                         max(list(grammar.keys()), key=len))),
              end=' ')
        print('{', end=' ')
        nterms = 0
        
        temp = []
        for term in get_follow(head, start):
            if nterms > 0:
                print(', ', end=' ')
            print(term, end=' ')
            nterms += 1
            temp.append(term)

        print('}')
        follow.append({
                "symbol" : head,
                "follow" : temp
            }
        )

    print('\nItems')
    
    items = []

    for i in range(len(lr0_items)):
        print('I' + str(i) + ':')
        
        item = 'I' + str(i)
        item_line_list = []

        for head, prods in lr0_items['I' + str(i)].items():
            for prod in prods:
                _str = ""
                print('{:>{width}} ->'.format(head,
                                              width=len(
                                                  max(list(grammar.keys()),
                                                      key=len))),
                      end=' ')
                
                _str += '{:>{width}} ->'.format(head,
                                              width=len(
                                                  max(list(grammar.keys()),
                                                      key=len))) + " "
                
                for char in prod:
                    print(char, end=' ')
                    _str += char + " "

                print()
                item_line_list.append(_str)
        items.append({
            "item" : item,
            "list" : item_line_list
        })
        
    
    for i in range(len(parse_table)):  # len gives number of states
        for sym in symbols:
            response = perform_action(i, sym, start, error, parse_table)
            if "ERROR" in response :
                return {
                    "error" : True,
                    "message" : response,
                    "augmented_grammer" : augmented_grammer,
                    "terminals" : terms,
                    "non_terminals" : nonterms,
                    "symbols" : symbols,
                    "first" : first,
                    "follow" : follow,
                    "items" : items,
                }
            
            
            
    
    parsing_table = []
    
    print('\nParsing Table')
    print('+' + '--------+' * (len(terms) + len(nonterms) + 1))
    print('|{:^8}|'.format('State'), end=' ')
    
    column_headers = []
    column_headers.append("State")

    for term in terms:
        print('{:^7}|'.format(term), end=' ')
        column_headers.append(term)

    print('{:^7}|'.format('$'), end=' ')
    column_headers.append('$')

    for nonterm in nonterms:
        if nonterm == start:
            continue
        
        print('{:^7}|'.format(nonterm), end=' ')
        column_headers.append(nonterm)

    print('\n+' + '--------+' * (len(terms) + len(nonterms) + 1))
    
    parsing_table.append(column_headers)
    
    for i in range(len(parse_table)):
        row = []
        
        print('|{:^8}|'.format(i), end=' ')
        row.append(i)
        
        for j in range(len(parse_table[i]) - 1):
            print('{:^7}|'.format(parse_table[i][j]), end=' ')
            row.append(parse_table[i][j])

        print()
        parsing_table.append(row)

    print('+' + '--------+' * (len(terms) + len(nonterms) + 1))
    
    return {
        "error" : False,
        "augmented_grammer" : augmented_grammer,
        "terminals" : terms,
        "non_terminals" : nonterms,
        "symbols" : symbols,
        "first" : first,
        "follow" : follow,
        "items" : items,
        "parsing_table" : parsing_table
    }


def collect_lr0_items(start):
    global lr0_items
    i = 1
    lr0_items['I0'] = get_closure({start: [['.'] + grammar[start][0]]})

    while True:
        item_len = len(lr0_items) + sum(len(v) for v in lr0_items.values())

        for idx in list(lr0_items):
            for sym in symbols:
                if goto(lr0_items[idx], sym) and (goto(lr0_items[idx], sym)
                                                  not in lr0_items.values()):
                    lr0_items['I' + str(i)] = goto(lr0_items[idx], sym)
                    i += 1

        if item_len == len(lr0_items) + sum(
                len(v) for v in lr0_items.values()):

            return


def goto(item, symbol):
    goto_states = {}

    for head, prods in item.items():
        for prod in prods:
            for i in range(len(prod) - 1):
                if prod[i] != '.' or prod[i + 1] != symbol:
                    continue

                tmp_prod = prod[:]
                tmp_prod[i], tmp_prod[i + 1] = (tmp_prod[i + 1], tmp_prod[i])
                prod_closure = get_closure({head: [tmp_prod]})

                for sym in prod_closure:
                    if sym not in goto_states:
                        goto_states[sym] = prod_closure[sym]
                    elif prod_closure[sym] not in goto_states[sym]:
                        goto_states[sym].extend(list(prod_closure[sym]))

    return goto_states


def perform_action(i, symbol, start, error, parse_table):
    for _, prods in lr0_items['I' + str(i)].items():
        for prod in prods:
            for j in range(len(prod) - 1):
                if prod[j] == '.' and prod[j + 1] == symbol:
                    for k in range(len(lr0_items)):
                        if goto(lr0_items['I' + str(i)],
                                symbol) == lr0_items['I' + str(k)]:

                            if symbol in terms:
                                if 'r' in parse_table[i][terms.index(symbol)]:

                                    if error != 1:
                                        return 'ERROR: Shift-Reduce conflict' + \
                                              ' at State ' + str(i) + \
                                              ', Symbol \'' + \
                                              str(terms.index(symbol)) + '\''

                                    error = 1

                                    if 's' + str(k) not in parse_table[i][
                                            terms.index(symbol)]:
                                        parse_table[i][terms.index(
                                            symbol
                                        )] = parse_table[i][terms.index(
                                            symbol)] + '/s' + str(k)

                                        return parse_table[i][terms.index(
                                            symbol)]
                                else:
                                    parse_table[i][terms.index(
                                        symbol)] = 's' + str(k)
                            else:
                                parse_table[i][len(terms) +
                                               nonterms.index(symbol)] = str(k)

                            return 's' + str(k)

    for lr0_head, lr0_prods in lr0_items['I' + str(i)].items():
        if lr0_head != start:
            for lr0_prod in lr0_prods:
                if lr0_prod[-1] == '.':  # final item
                    k = 0

                    for gram_head, gram_prods in grammar.items():
                        for gram_prod in gram_prods:
                            if (gram_head == lr0_head
                                    and gram_prod == lr0_prod[:-1]
                                    and (symbol in terms or symbol == '$')):

                                for term in get_follow(lr0_head, start):
                                    if term == '$':
                                        index = len(terms)
                                    else:
                                        index = terms.index(term)

                                    if 's' in parse_table[i][index]:
                                        if error != 1:
                                            return \
                                                'ERROR: Shift-Reduce conflict' \
                                                + ' at State ' + str(i) + \
                                                ', Symbol \'' + str(term) + \
                                                '\''

                                        error = 1

                                        if 'r' + str(k) not in parse_table[i][
                                                index]:
                                            parse_table[i][index] = (
                                                parse_table[i][index] + '/r' +
                                                str(k))

                                        return parse_table[i][index]
                                    elif parse_table[i][index] and (
                                            parse_table[i][index] !=
                                            'r' + str(k)):

                                        if error != 1:
                                            return \
                                                'ERROR: Reduce-Reduce conflict' \
                                                + ' at State ' + str(i) + \
                                                ', Symbol \'' + str(term) + \
                                                '\''

                                        error = 1

                                        if 'r' + str(k) not in parse_table[i][
                                                index]:
                                            parse_table[i][index] = (
                                                parse_table[i][index] + '/r' +
                                                str(k))

                                        return parse_table[i][index]
                                    else:
                                        parse_table[i][index] = 'r' + str(k)

                                return 'r' + str(k)

                            k += 1

    if start in lr0_items['I' + str(i)] and (
            grammar[start][0] + ['.'] in lr0_items['I' + str(i)][start]):
        parse_table[i][len(terms)] = 'acc'

        return 'acc'

    return ''
