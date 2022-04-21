'''
    B3 TXT Parser
    https://github.com/rafaeljc/b3-txt-parser
'''


import argparse
import pandas as pd



VERSION = '0.1.0'


class TXTParser():
    def __init__(self):
        self._init_argparse()
        self.prog = self.args_parser.prog
        self.file_path = self.args.txt_file_path
        # checando a extensão do arquivo
        if self.file_path[-4:].lower() != '.txt':
            raise SystemExit(f'{self.prog}: {self.file_path}: A extensão não '
                + 'é a de um arquivo TXT')
        self.data = pd.DataFrame()


    def _init_argparse(self):
        parser = argparse.ArgumentParser(
            description=('Converte arquivo TXT de cotações históricas do '
                + 'mercado à vista da B3.')
        )
        parser.add_argument(
            '-v', '--version', action='version',
            version=f'{parser.prog} version {VERSION}'
        )
        parser.add_argument(
            'txt_file_path',
            help='caminho para o arquivo TXT'
        )
        # opções de conversão
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--json', action='store_true',
            help='converte o TXT para JSON'
        )
        group.add_argument(
            '--csv', action='store_true',
            help='converte o TXT para CSV'
        )
        group.add_argument(
            '--excel', action='store_true',
            help='converte o TXT para EXCEL'
        )
        self.args_parser = parser
        self.args = self.args_parser.parse_args()


    def _str_to_float(self, str):
        # conforme layout do arquivo TXT
        # os dois últimos dígitos são os decimais   
        return float(str[:-2] + '.' + str[-2:])


    def parse_txt(self):
        try:
            with open(self.file_path, 'r') as file:
                data = []
                for line in file:
                    if line[:2] != '01':
                        continue
                    data.append({
                        'DATE': int(line[2:10]),
                        'CODBDI': line[10:12],
                        'CODNEG': line[12:24],
                        'TPMERC': int(line[24:27]),
                        'NOMRES': line[27:39],
                        'ESPECI': line[39:49],
                        'PRAZOT': line[49:52],
                        'MODREF': line[52:56],
                        'PREABE': self._str_to_float(line[56:69]),
                        'PREMAX': self._str_to_float(line[69:82]),
                        'PREMIN': self._str_to_float(line[82:95]),
                        'PREMED': self._str_to_float(line[95:108]),
                        'PREULT': self._str_to_float(line[108:121]),
                        'PREOFC': self._str_to_float(line[121:134]),
                        'PREOFV': self._str_to_float(line[134:147]),
                        'TOTNEG': int(line[147:152]),
                        'QUATOT': int(line[152:170]),
                        'VOLTOT': self._str_to_float(line[170:188]),
                        'PREEXE': self._str_to_float(line[188:201]),
                        'INDOPC': int(line[201:202]),
                        'DATVEN': int(line[202:210]),
                        'FATCOT': int(line[210:217]),
                        'PTOEXE': self._str_to_float(line[217:230]),
                        'CODISI': line[230:242],
                        'DISMES': int(line[242:245])
                    })
                self.data = pd.DataFrame(data)        
        except FileNotFoundError as err:
            raise SystemExit(f'{self.prog}: {self.file_path}: {err.strerror}')


    def export(self):
        # caso não seja escolhido um formato de saída, será utilizado JSON
        is_default = ((not self.args.json) and (not self.args.csv) 
                        and (not self.args.excel))
        if is_default or self.args.json:
            self.data.to_json(self.file_path[:-4] + '.json', orient='records')
            return
        else:
            if self.args.csv:
                self.data.to_csv(self.file_path[:-4] + '.csv', index=False)
                return
            if self.args.excel:
                try:
                    self.data.to_excel(self.file_path[:-4] + '.xlsx', 
                        index=False)
                # quando as dimensões do DataFrame é maior que o suportado
                # pelo formato .xlsx
                except ValueError as err:
                    raise SystemExit(f'{self.prog}: {self.file_path}: '
                        + f'{err.args[0]}')
                return


def main():
    txt_parser = TXTParser()
    txt_parser.parse_txt()
    txt_parser.export()
    print('Done!')
    

if __name__ == '__main__':
    main()
