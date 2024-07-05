from django.shortcuts import render
from django.http import HttpResponse
from .main import main
from .parse_input_string import parse_input_string
# Create your views here.
def index(request) :
    if request.method == "POST" :
        res = request.POST
        grammer = res['grammer']
        print("Grammer : " , grammer)
        file_path = "static/grammer.txt"
        with open(file_path , "w") as file :
            file.write(grammer.replace('\r' , ''))
        data = main()
        print(data)
        if data['error'] == False :
            data['parsing_table_heading'] = data['parsing_table'][0]
            data['parsing_table_row'] = data['parsing_table'][1:]
        return render(request , "index.html" , {'data' : data , 'grammer' : grammer})
    return render(request , "index.html")


def check_string(request) :
    string = "something-went-wrong"
    if request.method == "POST" :
        res = request.POST
        string = res['string']
        data = main()
        grammer = ""
        with open("static/grammer.txt" , "r") as file :
            grammer = "".join(file.readlines())
        response_ = parse_input_string(string , data['row_start_sym'] , data['row_error_sym'] , data['row_parse_table'])
        if data['error'] == False :
            data['parsing_table_heading'] = data['parsing_table'][0]
            data['parsing_table_row'] = data['parsing_table'][1:]
        print("string : " , string)
        return render(request , "index.html" , {'data' : data , 'grammer' : grammer , 'track_stack_headers' : response_[0] , 'track_stack_rows' : response_[1:] , 'string' : string})
    return render(request , "index.html")

# "augmented_grammer" : augmented_grammer,
# "terminals" : terms,
# "non_terminals" : nonterms,
# "symbols" : symbols,
# "first" : first,
# "follow" : follow,
# "items" : items,
# "parsing_table" : parsing_table