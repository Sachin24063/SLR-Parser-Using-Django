grammar = {}
lr0_items = {}
terms = []
nonterms = []
symbols = []

def clear_all() :
    global grammar, start_sym, terms, nonterms, symbols, lr0_items
    grammar = {}
    lr0_items = {}
    terms = []
    nonterms = []
    symbols = []