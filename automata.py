def validarCad(cadena):
    path = "q1 "
    f = open("transitions.txt","a")
    estado='q1'
    for i in range(0,len(cadena)):
        estado=transitions[(estado,cadena[i])]
        path = path + estado + " "
    if (
        estado == 'q5' or
        estado == 'q10' or
        estado == 'q14' or
        estado == 'q17' or
        estado == 'q21' or
        estado == 'q26' or
        estado == 'q33' or
        estado == 'q38' or
        estado == 'q42' or
        estado == 'q45' or
        estado == 'q50' or
        estado == 'q55' or
        estado == 'q57' or
        estado == 'q61' or
        estado == 'q63' or
        estado == 'q65' or
        estado == 'q69' or
        estado == 'q77' or
        estado == 'q81' or
        estado == 'q86' or
        estado == 'q91' or
        estado == 'q95' or
        estado == 'q100' or
        estado == 'q104' or
        estado == 'q111' or
        estado == 'q116' or
        estado == 'q122' or
        estado == 'q130' or
        estado == 'q132' or
        estado == 'q137'
       ):
        f.write(cadena+": "+path)
        f.write("\n")
        f.close()
        return 1
    else:
        return 0

transitions = {
    ('q1', 'a'):'q2', 
    ('q2', 'u'):'q3', 
    ('q3', 't'):'q4', 
    ('q4', 'o'):'q5', #auto 
    ('q1', 'b'):'q6', 
    ('q6', 'r'):'q7', 
    ('q7', 'e'):'q8', 
    ('q8', 'a'):'q9', 
    ('q9', 'k'):'q10', #break 
    ('q1', 'c'):'q11', 
    ('q11', 'a'):'q12', 
    ('q12', 's'):'q13', 
    ('q13', 'e'):'q14', #case
    ('q11', 'h'):'q15', 
    ('q15', 'a'):'q16', 
    ('q16', 'r'):'q17', #char 
    ('q11', 'o'):'q18', 
    ('q18', 'n'):'q19', 
    ('q19', 's'):'q20', 
    ('q20', 't'):'q21', #const
    ('q19', 't'):'q22', 
    ('q22', 'i'):'q23', 
    ('q23', 'n'):'q24', 
    ('q24', 'u'):'q25', 
    ('q25', 'e'):'q26', #continue 
    ('q1', 'd'):'q27', 
    ('q27', 'e'):'q28', 
    ('q28', 'f'):'q29', 
    ('q29', 'a'):'q30', 
    ('q30', 'u'):'q31', 
    ('q31', 'l'):'q32', 
    ('q32', 't'):'q33', #default 
    ('q27', 'o'):'q34', #do 
    ('q34', 'u'):'q35', 
    ('q35', 'b'):'q36', 
    ('q36', 'l'):'q37', 
    ('q37', 'e'):'q38', #double 
    ('q1', 'e'):'q39', 
    ('q39', 'l'):'q40', 
    ('q40', 's'):'q41', 
    ('q41', 'e'):'q42', #else 
    ('q39', 'n'):'q43', 
    ('q43', 'u'):'q44', 
    ('q44', 'm'):'q45', #enum 
    ('q39', 'x'):'q46', 
    ('q46', 't'):'q47', 
    ('q47', 'e'):'q48', 
    ('q48', 'r'):'q49', 
    ('q49', 'n'):'q50', #extern 
    ('q1', 'f'):'q51', 
    ('q51', 'l'):'q52', 
    ('q52', 'o'):'q53', 
    ('q53', 'a'):'q54', 
    ('q54', 't'):'q55', #float
    ('q51', 'o'):'q56', 
    ('q56', 'r'):'q57', #for 
    ('q1', 'g'):'q58', 
    ('q58', 'o'):'q59', 
    ('q59', 't'):'q60', 
    ('q60', 'o'):'q61', #goto
    ('q1', 'i'):'q62', 
    ('q62', 'f'):'q63', #if 
    ('q62', 'n'):'q64', 
    ('q62', 't'):'q65', #int 
    ('q1', 'l'):'q66', 
    ('q66', 'o'):'q67', 
    ('q67', 'n'):'q68', 
    ('q68', 'g'):'q69', #long
    ('q1', 'r'):'q70', 
    ('q70', 'e'):'q71', 
    ('q71', 'g'):'q72', 
    ('q72', 'i'):'q73', 
    ('q73', 's'):'q74', 
    ('q74', 't'):'q75', 
    ('q75', 'e'):'q76', 
    ('q76', 'r'):'q77',#register 
    ('q71', 't'):'q78', 
    ('q78', 'u'):'q79', 
    ('q79', 'r'):'q80', 
    ('q80', 'n'):'q81',#return 
    ('q1', 's'):'q82', 
    ('q82', 'h'):'q83', 
    ('q83', 'o'):'q84', 
    ('q84', 'r'):'q85', 
    ('q85', 't'):'q86', #short
    ('q86', 'i'):'q87', 
    ('q87', 'g'):'q88', 
    ('q88', 'n'):'q89', 
    ('q89', 'e'):'q90', 
    ('q90', 'd'):'q91', #signed
    ('q87', 'z'):'q92', 
    ('q92', 'e'):'q93', 
    ('q93', 'o'):'q94', 
    ('q94', 'f'):'q95', #sizeof 
    ('q82', 't'):'q96', 
    ('q96', 'a'):'q97', 
    ('q97', 't'):'q98', 
    ('q98', 'i'):'q99', 
    ('q99', 'c'):'q100', #static 
    ('q96', 'r'):'q101',
    ('q101', 'u'):'q102',
    ('q102', 'c'):'q103',
    ('q103', 't'):'q104', #struct
    ('q1', 't'):'q105', 
    ('q105', 'y'):'q106', 
    ('q106', 'p'):'q107', 
    ('q107', 'e'):'q108', 
    ('q108', 'd'):'q109', 
    ('q109', 'e'):'q110', 
    ('q110', 'f'):'q111', #typedef 
    ('q1', 'u'):'q112', 
    ('q112', 'n'):'q113', 
    ('q113', 'i'):'q114', 
    ('q114', 'o'):'q115', 
    ('q115', 'n'):'q116', #union
    ('q113', 's'):'q117',
    ('q117', 'i'):'q118',
    ('q118', 'g'):'q119',
    ('q119', 'n'):'q120',
    ('q120', 'e'):'q121',
    ('q121', 'd'):'q122', #unsigned
    ('q1', 'v'):'q123', 
    ('q123', 'o'):'q124', 
    ('q124', 'l'):'q125', 
    ('q125', 'a'):'q126', 
    ('q126', 't'):'q127', 
    ('q127', 'i'):'q128', 
    ('q128', 'l'):'q129', 
    ('q129', 'e'):'q130', #volatile
    ('q124', 'i'):'q131', 
    ('q131', 'd'):'q132', #void
    ('q1', 'w'):'q133', 
    ('q133', 'h'):'q134', 
    ('q134', 'i'):'q135', 
    ('q135', 'l'):'q136', 
    ('q136', 'e'):'q137', #while 
    }

def processString(cadena):
    cadena = cadena.replace("\n","")
    cadena = cadena.replace("(","")
    cadena = cadena.replace(")","")
    cadena = cadena.replace("{","")
    cadena = cadena.replace("}","")
    cadena = cadena.replace("[","")
    cadena = cadena.replace("]","")
    cadena = cadena.replace(";","")
    cadena = cadena.replace("*","")

    return cadena
palabra = 0

f = open("programa.c","r")
f2 = open("resultado.txt","w")
f3 = open("transitions.txt","w")
f3.close()
linea=1
for line in f.readlines():
    aux = line.split()
    palabra = 1
    for cadena in aux:
        cadena = processString(cadena)
        try:
            if validarCad(cadena) == 1:
                f2.write("Palabra: " + cadena + " Linea: " + str(linea) + " No.Palabra en linea: " + str(palabra) + '\n')
        except KeyError:
            print("Palabra procesada no valida")
        palabra = palabra + 1
    linea = linea + 1

f.close()
f2.close()
