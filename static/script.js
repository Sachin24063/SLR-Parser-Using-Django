document.getElementById("copy-1").addEventListener("click" , function(){
    document.getElementsByTagName("textarea")[0].value = `E -> E + T | T
T -> T F | F
F -> F * | a | b
`
})

document.getElementById("copy-error").addEventListener("click" , function(){
    document.getElementsByTagName("textarea")[0].value = `S -> R
L -> * R
L -> id
R -> L
`
})

document.getElementById("copy-2").addEventListener("click" , function(){
    document.getElementsByTagName("textarea")[0].value = `E -> E + T | T
T -> T * F | F
F -> ( E ) | id
`
})