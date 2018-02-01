from ..datas import operacao_datas,converter_periodo
from ..exceptions.exception import infoerroexception,tratamento_excessao
from ...instancias.Instancias import add_instancia


class operacoes_pre_processamento:

    # geters e seters

    def get_simpletimeserie(self, data_inicial, data_final, index, **kwargs):
        try:
            index_inicio = int(operacao_datas('-', self.data_inicial, data_inicial) / (converter_periodo(self.periodo, 'dia') * self.time_steps))
            index_fim = int(operacao_datas('-', self.data_inicial, data_final) / (converter_periodo(self.periodo, 'dia') * self.time_steps))
            if(index_inicio!=None and index_fim!=None):
                serie_y = self.tabela.copiar_planilha(0, index_inicio+1, index_fim, index, index, self.orientacao_data)[0]
                serie_x = [valor+index_inicio for valor in range(0, len(serie_y)) if(serie_y[valor]!=None)]
                serie_y = [valor for valor in serie_y if(valor!=None)]
                return serie_x, serie_y
            else:
                raise infoerroexception("Data inicial ou data final incorretas")
        except infoerroexception as e:
            tratamento_excessao('Info')
        except Exception as e:
            print(str(e))

    def _set_parameter(self, array, tabela, orientacao_data, periodo, time_steps, data_inicial, keys_array, **kwargs):
        try:
            self.array = array
            self.tabela = tabela
            self.orientacao_data = orientacao_data
            self.periodo = periodo
            self.time_steps = time_steps
            self.data_inicial = data_inicial
            self.keys_array = keys_array
            for key, arg in zip(kwargs.keys(), kwargs.values()):
                if (arg != None):
                    self.keys[key] = arg
        except Exception as e:
            tratamento_excessao('Erro')

    def __init__(self):
        self.array = None
        self.tabela = None
        self.orientacao_data = None
        self.periodo = None
        self.time_steps = None
        self.data_inicial = None
        self.planilha_index = 0
        self.keys_array = [""]
        self.keys = {}


def criar_instancia_pre_processamento():
    inst_pre_preocessamento=operacoes_pre_processamento()
    add_instancia("pre_processamento",inst_pre_preocessamento)
