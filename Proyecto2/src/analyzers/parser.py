from src.models.token import Token


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokens.append(Token("$", "EOF", "EOF", -1, -1))

    def recuperar_modo_panico(self, nombre_token_de_sincronizacion):
        while self.tokens[0].token != "$":
            token = self.tokens.pop(0)
            if token.token == nombre_token_de_sincronizacion:
                break

    # <inicio> ::= <procedimientos>
    def parse(self):
        self.procedimientos()

    # <procedimientos>: := <procedimientos> <procedimientos>
    #                     | epsilon
    def procedimientos(self):
        if self.tokens[0].token == "$":
            return
        self.procedimiento()
        self.procedimientos()

    # <procedimiento> ::= <declaración>
    #                    | <tipo de procedimiento>
    def procedimiento(self):
        if self.tokens[0].token == "tk_array":
            self.declaracion()
        else:
            self.tipo_de_procedimiento()

    # <declaracion> ::= tk_array tk_id tk_asignacion tk_new tk_array tk_corchete_izquierdo <listado items> tk_corchete_derecho tk_punto_y_coma
    def declaracion(self):
        if self.tokens[0].token == "tk_array":
            self.tokens.pop(0)
            if self.tokens[0].token == "tk_identifier":
                id = self.tokens.pop(0)
                if self.tokens[0].token == "tk_assign":
                    self.tokens.pop(0)
                    if self.tokens[0].token == "tk_new":
                        self.tokens.pop(0)
                        if self.tokens[0].token == "tk_array":
                            self.tokens.pop(0)
                            if self.tokens[0].token == "tk_corchete_apertura":
                                self.tokens.pop(0)
                                items = self.listado_items()
                                if self.tokens[0].token == "tk_corchete_cierre":
                                    self.tokens.pop(0)
                                    if self.tokens[0].token == "tk_punto_y_coma":
                                        self.tokens.pop(0)
                                        print("ID:", id.lexeme)
                                        print("Lista:")
                                        for item in items:
                                            print(item.lexeme)
                                    else:
                                        print(f"ES - Se esperaba un ; en la linea {self.tokens[0].line}, pero se obtuvo {self.tokens[0].lexeme}")
                                else:
                                    print(f"ES - Se esperaba un ] en la linea {self.tokens[0].line}, pero se obtuvo {self.tokens[0].lexeme}")
                                    self.recuperar_modo_panico("tk_punto_y_coma")
                            else:
                                print(
                                    f"ES - Se esperaba un [ en la linea {self.tokens[0].line}, pero se obtuvo {self.tokens[0].lexeme}")
                                self.recuperar_modo_panico("tk_punto_y_coma")
                        else:
                            print(f"ES - Se esperaba la palabra Array en la linea {self.tokens[0].line}, pero se obtuvo {self.tokens[0].lexeme}")
                            self.recuperar_modo_panico("tk_punto_y_coma")
                    else:
                        print(f"ES - Se esperaba la palabra new en la linea {self.tokens[0].line}, pero se obtuvo {self.tokens[0].lexeme}")
                        self.recuperar_modo_panico("tk_punto_y_coma")
                else:
                    print(f"ES - Se esperaba = en la linea {self.tokens[0].line}, pero se obtuvo {self.tokens[0].lexeme}")
                    self.recuperar_modo_panico("tk_punto_y_coma")
            else:
                print(f"ES - Se esperaba el nombre de la variable en la linea {self.tokens[0].line}, pero se obtuvo {self.tokens[0].lexeme}")
                self.recuperar_modo_panico("tk_punto_y_coma")

    # <listado de items> ::= <item> <mas_items>
    #                       | epsilon
    def listado_items(self):
        elemento = self.item()
        if elemento is None:
            return []
        lista = [elemento]
        mas_elementos = self.mas_items()
        lista.extend(mas_elementos)
        return lista

    # <mas_items> ::= tk_coma <item> <mas_items>
    #     	          | epsilon
    def mas_items(self):
        if self.tokens[0].token == "tk_coma":
            self.tokens.pop(0)
            elemento = self.item()
            if elemento is None:
                return []
            lista = [elemento]
            lista.extend(self.mas_items())
            return lista
        else:
            return []

    # <item> ::= tk_number
    #            | tk_string
    #            | tk_decimal_number
    def item(self):
        if self.tokens[0].token == "tk_number":
            return self.tokens.pop(0)
        elif self.tokens[0].token == "tk_decimal_number":
            return self.tokens.pop(0)
        elif self.tokens[0].token == "tk_string":
            return self.tokens.pop(0)
        else:
            return None

    # <tipo procedimiento> ::= tk_id tk_punto <operacion arreglo>
    def tipo_de_procedimiento(self):
        if self.tokens[0].token == "tk_identifier":
            id = self.tokens.pop(0)
            if self.tokens[0].token == "tk_punto":
                self.tokens.pop(0)
                self.operacion_arreglo()
            else:
                print(f"ES - Se esperaba . en la linea {self.tokens[0].line}, pero se obtuvo {self.tokens[0].lexeme}")
                self.recuperar_modo_panico("tk_punto_y_coma")
        else:
            print(f"ES - Se esperaba un identificador en la linea {self.tokens[0].line}, pero se obtuvo {self.tokens[0].lexeme}")

    # <operación arreglo> ::= <ordenamiento>
    #                         | <guardar>
    def operacion_arreglo(self):
        if self.tokens[0].token == "tk_sort":
            self.ordenamiento()
        else:
            self.guardar()

    # <ordenamiento> ::= tk_ordenar tk_parentesis_izquierdo tk_ascendente tk_asignacion tk_booleano tk_parentesis_derecho tk_punto_y_coma
    def ordenamiento(self):
        if self.tokens[0].token == "tk_sort":
            self.tokens.pop(0)
            if self.tokens[0].token == "tk_parentesis_apertura":
                self.tokens.pop(0)
                if self.tokens[0].token == "tk_asc":
                    self.tokens.pop(0)
                    if self.tokens[0].token == "tk_assign":
                        self.tokens.pop(0)
                        if self.tokens[0].type == "BOOLEAN":
                            asc = self.tokens.pop(0)
                            if self.tokens[0].token == "tk_parentesis_cierre":
                                self.tokens.pop(0)
                                if self.tokens[0].token == "tk_punto_y_coma":
                                    self.tokens.pop(0)
                                    # manejar instrucciones
                                    return asc.lexeme
                        else:
                            self.recuperar_modo_panico("tk_punto_y_coma")
                    else:
                        self.recuperar_modo_panico("tk_punto_y_coma")
                else:
                    self.recuperar_modo_panico("tk_punto_y_coma")
            else:
                self.recuperar_modo_panico("tk_punto_y_coma")
        else:
            self.recuperar_modo_panico("tk_punto_y_coma")

    # <guardar> ::= tk_guardar tk_parentesis_izquierdo tk_string tk_parentesis_derecho tk_punto_y_coma
    def guardar(self):
        if self.tokens[0].token == "tk_save":
            self.tokens.pop(0)
            if self.tokens[0].token == "tk_parentesis_apertura":
                self.tokens.pop(0)
                if self.tokens[0].token == "tk_string":
                    ruta = self.tokens.pop(0)
                    if self.tokens[0].token == "tk_parentesis_cierre":
                        self.tokens.pop(0)
                        if self.tokens[0].token == "tk_punto_y_coma":
                            self.tokens.pop(0)
                            return ruta.lexeme
                else:
                    self.recuperar_modo_panico("tk_punto_y_coma")
            else:
                self.recuperar_modo_panico("tk_punto_y_coma")
        else:
            self.recuperar_modo_panico("tk_punto_y_coma")
