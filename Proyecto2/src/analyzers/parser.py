import os

from src.graphviz.graph_dot import GraphDot
from src.models.syntax_error import SyntacticalError
from src.models.token import Token


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokens.append(Token("$", "EOF", "EOF", -1, -1))
        self.syntactical_errors = []
        self.listado_ids = {}
        self.count = 0
        self.graph = GraphDot()

    def recuperar_modo_panico(self, nombre_token_de_sincronizacion):
        while self.tokens[0].token != "$":
            token = self.tokens.pop(0)
            if token.token == nombre_token_de_sincronizacion:
                break

    # <inicio> ::= <procedimientos>
    def parse(self):
        self.graph.create_node(self.count, "<inicio>")
        self.procedimientos()
        return self.syntactical_errors, self.graph

    # <procedimientos>: := <procedimiento> <procedimientos>
    #                     | epsilon
    def procedimientos(self):
        if self.tokens[0].token == "$":
            return
        # self.graph.create_node(self.count, "<procedimientos>")
        # self.graph.create_connection(self.count, 1)
        # self.count += 1
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
                                        self.listado_ids[id.lexeme] = items
                                        for elemento in self.listado_ids:
                                            print(elemento)
                                            print(self.listado_ids[elemento])
                                    else:
                                        tmp_se = SyntacticalError(self.tokens[0].lexeme,
                                                                  self.tokens[0].line,
                                                                  self.tokens[0].column,
                                                                  "tk_punto_y_coma")
                                        self.syntactical_errors.append(tmp_se)
                                        self.recuperar_modo_panico("tk_punto_y_coma")
                                else:
                                    tmp_se = SyntacticalError(self.tokens[0].lexeme,
                                                              self.tokens[0].line,
                                                              self.tokens[0].column,
                                                              "tk_corchete_cierre")
                                    self.syntactical_errors.append(tmp_se)
                                    self.recuperar_modo_panico("tk_punto_y_coma")
                            else:
                                tmp_se = SyntacticalError(self.tokens[0].lexeme,
                                                          self.tokens[0].line,
                                                          self.tokens[0].column,
                                                          "tk_corchete_apertura")
                                self.syntactical_errors.append(tmp_se)
                                self.recuperar_modo_panico("tk_punto_y_coma")
                        else:
                            tmp_se = SyntacticalError(self.tokens[0].lexeme,
                                                      self.tokens[0].line,
                                                      self.tokens[0].column,
                                                      "tk_array")
                            self.syntactical_errors.append(tmp_se)
                            self.recuperar_modo_panico("tk_punto_y_coma")
                    else:
                        tmp_se = SyntacticalError(self.tokens[0].lexeme,
                                                  self.tokens[0].line,
                                                  self.tokens[0].column,
                                                  "tk_new")
                        self.syntactical_errors.append(tmp_se)
                        self.recuperar_modo_panico("tk_punto_y_coma")
                else:
                    tmp_se = SyntacticalError(self.tokens[0].lexeme,
                                              self.tokens[0].line,
                                              self.tokens[0].column,
                                              "tk_assign")
                    self.syntactical_errors.append(tmp_se)
                    self.recuperar_modo_panico("tk_punto_y_coma")
            else:
                tmp_se = SyntacticalError(self.tokens[0].lexeme,
                                          self.tokens[0].line,
                                          self.tokens[0].column,
                                          "tk_identifier")
                self.syntactical_errors.append(tmp_se)
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
            return int(self.tokens.pop(0).lexeme)
        elif self.tokens[0].token == "tk_decimal_number":
            return float(self.tokens.pop(0).lexeme)
        elif self.tokens[0].token == "tk_string":
            return self.tokens.pop(0).lexeme.replace('"', '')
        else:
            tmp_se = SyntacticalError(self.tokens[0].lexeme,
                                      self.tokens[0].line,
                                      self.tokens[0].column,
                                      "tk_numer | tk_decimal_number | tk_string")
            self.syntactical_errors.append(tmp_se)
            return None

    # <tipo procedimiento> ::= tk_id tk_punto <operacion arreglo>
    def tipo_de_procedimiento(self):
        if self.tokens[0].token == "tk_identifier":
            id = self.tokens.pop(0)
            if self.tokens[0].token == "tk_punto":
                self.tokens.pop(0)
                self.operacion_arreglo(id)
            else:
                tmp_se = SyntacticalError(self.tokens[0].lexeme,
                                          self.tokens[0].line,
                                          self.tokens[0].column,
                                          "tk_punto")
                self.syntactical_errors.append(tmp_se)
                self.recuperar_modo_panico("tk_punto_y_coma")
        else:
            tmp_se = SyntacticalError(self.tokens[0].lexeme,
                                      self.tokens[0].line,
                                      self.tokens[0].column,
                                      "tk_identifier")
            self.syntactical_errors.append(tmp_se)
            self.recuperar_modo_panico("tk_punto_y_coma")

    # <operación arreglo> ::= <ordenamiento>
    #                         | <guardar>
    def operacion_arreglo(self, id):
        if self.tokens[0].token == "tk_sort":
            self.ordenamiento(id)
        else:
            self.guardar(id)

    # <ordenamiento> ::= tk_ordenar tk_parentesis_izquierdo tk_ascendente tk_asignacion tk_booleano tk_parentesis_derecho tk_punto_y_coma
    def ordenamiento(self, id):
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
                                    if id.lexeme in self.listado_ids:
                                        bubble_sort(asc.lexeme, self.listado_ids[id.lexeme])
                                        # print(self.listado_ids[id.lexeme])
                                    # print(id.lexeme, asc.lexeme)
                                    else:
                                        print(f"err: variable no inicializada {id.lexeme}")
                                else:
                                    tmp_se = SyntacticalError(self.tokens[0].lexeme,
                                                              self.tokens[0].line,
                                                              self.tokens[0].column,
                                                              "tk_punto_y_coma")
                                    self.syntactical_errors.append(tmp_se)
                            else:
                                tmp_se = SyntacticalError(self.tokens[0].lexeme,
                                                          self.tokens[0].line,
                                                          self.tokens[0].column,
                                                          "tk_parentesis_cierre")
                                self.syntactical_errors.append(tmp_se)
                                self.recuperar_modo_panico("tk_punto_y_coma")
                        else:
                            tmp_se = SyntacticalError(self.tokens[0].lexeme,
                                                      self.tokens[0].line,
                                                      self.tokens[0].column,
                                                      "FALSE | TRUE")
                            self.syntactical_errors.append(tmp_se)
                            self.recuperar_modo_panico("tk_punto_y_coma")
                    else:
                        tmp_se = SyntacticalError(self.tokens[0].lexeme,
                                                  self.tokens[0].line,
                                                  self.tokens[0].column,
                                                  "tk_assign")
                        self.syntactical_errors.append(tmp_se)
                        self.recuperar_modo_panico("tk_punto_y_coma")
                else:
                    tmp_se = SyntacticalError(self.tokens[0].lexeme,
                                              self.tokens[0].line,
                                              self.tokens[0].column,
                                              "tk_asc")
                    self.syntactical_errors.append(tmp_se)
                    self.recuperar_modo_panico("tk_punto_y_coma")
            else:
                tmp_se = SyntacticalError(self.tokens[0].lexeme,
                                          self.tokens[0].line,
                                          self.tokens[0].column,
                                          "tk_parentesis_apertura")
                self.syntactical_errors.append(tmp_se)
                self.recuperar_modo_panico("tk_punto_y_coma")
        else:
            tmp_se = SyntacticalError(self.tokens[0].lexeme,
                                      self.tokens[0].line,
                                      self.tokens[0].column,
                                      "tk_sort")
            self.syntactical_errors.append(tmp_se)
            self.recuperar_modo_panico("tk_punto_y_coma")

    # <guardar> ::= tk_guardar tk_parentesis_izquierdo tk_string tk_parentesis_derecho tk_punto_y_coma
    def guardar(self, id):
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
                            if id.lexeme in self.listado_ids:
                                save_file_csv(ruta.lexeme.replace('"', ''), self.listado_ids[id.lexeme])
                                # print(ruta.lexeme)
                            # print(id.lexeme, ruta.lexeme)
                        else:
                            tmp_se = SyntacticalError(self.tokens[0].lexeme,
                                                      self.tokens[0].line,
                                                      self.tokens[0].column,
                                                      "tk_punto_y_coma")
                            self.syntactical_errors.append(tmp_se)
                            self.recuperar_modo_panico("tk_punto_y_coma")
                    else:
                        tmp_se = SyntacticalError(self.tokens[0].lexeme,
                                                  self.tokens[0].line,
                                                  self.tokens[0].column,
                                                  "tk_parentesis_cierre")
                        self.syntactical_errors.append(tmp_se)
                        self.recuperar_modo_panico("tk_punto_y_coma")
                else:
                    tmp_se = SyntacticalError(self.tokens[0].lexeme,
                                              self.tokens[0].line,
                                              self.tokens[0].column,
                                              "tk_string")
                    self.syntactical_errors.append(tmp_se)
                    self.recuperar_modo_panico("tk_punto_y_coma")
            else:
                tmp_se = SyntacticalError(self.tokens[0].lexeme,
                                          self.tokens[0].line,
                                          self.tokens[0].column,
                                          "tk_parentesis_apertura")
                self.syntactical_errors.append(tmp_se)
                self.recuperar_modo_panico("tk_punto_y_coma")
        else:
            tmp_se = SyntacticalError(self.tokens[0].lexeme,
                                      self.tokens[0].line,
                                      self.tokens[0].column,
                                      "tk_save")
            self.syntactical_errors.append(tmp_se)
            self.recuperar_modo_panico("tk_punto_y_coma")


def bubble_sort(asc, arr):
    n = len(arr)
    if asc == "TRUE":
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
    else:
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] < arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]


def save_file_csv(ruta, arr):
    #save_file_path = os.path.join(f"C:/Users/edyrr/PycharmProjects/LFP_Junio_2024_201730511/Proyecto2/src/assets",
    #                              f"{ruta}")
    #print(save_file_path)

    text = "data\n"
    for i in arr:
        text += str(i)
        text += "\n"
    print(text)
    with open(ruta, "w") as file_csv:
        file_csv.write(text)
        file_csv.close()
