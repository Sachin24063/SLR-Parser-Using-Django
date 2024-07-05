import os

from .global_vars import clear_all, grammar, lr0_items, nonterms, symbols, terms
from .parse_input_string import parse_input_string
from .slr_helpers import get_first, get_follow
from .slr_parser import collect_lr0_items, display, perform_action

start_sym = ''
error_sym = 0


def main():
    global start_sym, error_sym
    start_sym = ''
    error_sym = 0

    with open("static/grammer.txt", encoding='utf-8') as grammar_file:
        parse_grammar(grammar_file)

    collect_lr0_items(start_sym)

    parse_table = [['' for _ in range(len(terms) + len(nonterms) + 1)]
                   for _ in range(len(lr0_items))]

    response = display(start_sym, error_sym, parse_table)
    response['row_start_sym'] = start_sym
    response['row_error_sym'] = error_sym
    response['row_parse_table'] = parse_table
    
    return response
    # parse_input_string(start_sym, error_sym, parse_table)


def parse_grammar(file):
    global grammar, start_sym, terms, nonterms, symbols
    
    grammar.clear()
    lr0_items.clear()
    terms.clear()
    nonterms.clear()
    symbols.clear()
    
    
    for line in file:
        if line == '\n':
            break

        head = line[:line.index('->')].strip()
        prods = [
            rule.strip().split(' ')
            for rule in line[line.index('->') + 2:].split('|')
        ]

        if not start_sym:
            start_sym = head + "'"
            grammar[start_sym] = [[head]]
            nonterms.append(start_sym)

        if head not in grammar:
            grammar[head] = []

        if head not in nonterms:
            nonterms.append(head)

        for prod in prods:
            grammar[head].append(prod)

            for char in prod:
                if not char.isupper() and char not in terms:
                    terms.append(char)
                elif char.isupper() and char not in nonterms:
                    nonterms.append(char)
                    # non terminals dont produce other symbols
                    grammar[char] = []
    print("grammer : " ,grammar)
    symbols.extend([*nonterms, *terms])
