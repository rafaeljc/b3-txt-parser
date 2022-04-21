
import os
import pandas as pd



APP = 'b3-txt-parser/b3-txt-parser.py'
FILE_INPUT = 'tests/DemoCotacoesHistoricas12022003.txt'


def test_json_output():
    cmd = 'python3 ' + APP + ' ' + FILE_INPUT + ' --json'
    os.system(cmd)

    json_output = FILE_INPUT[:-4] + '.json'

    df1 = pd.read_json(json_output)
    df2 = pd.read_json('tests/_test.json')
    
    assert df1.equals(df2)

    return


def test_csv_output():
    cmd = 'python3 ' + APP + ' ' + FILE_INPUT + ' --csv'
    os.system(cmd)

    csv_output = FILE_INPUT[:-4] + '.csv'
    
    df1 = pd.read_csv(csv_output)
    df2 = pd.read_csv('tests/_test.csv')
    
    assert df1.equals(df2)

    return


def test_excel_output():
    cmd = 'python3 ' + APP + ' ' + FILE_INPUT + ' --excel'
    os.system(cmd)

    excel_output = FILE_INPUT[:-4] + '.xlsx'
    
    df1 = pd.read_excel(excel_output)
    df2 = pd.read_excel('tests/_test.xlsx')
    
    assert df1.equals(df2)

    return
