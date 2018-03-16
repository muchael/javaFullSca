#!/usr/bin/python
# coding: utf-8
'''
Created on 08/03/2018

@author: Newton Muchael
'''

import re
import sys
import json

config = {};

def readConf( fileName ):
    with open(fileName) as json_data:
        global config
        config = json.load(json_data)

def generateAttributes( attributes ):
    result = ""

    for i in attributes:
        result += ('\t/**\n'
	            '\t * Representa o ' + i['name'] + '\n'
	            '\t */\n')
        
        if i['notNull']:
            if i['type'] == 'String':
                result += '\t@NotEmpty\n'
            else:
                result += '\t@NotNull\n'

        result += '\tprivate ' + i['type'] + ' ' + i['name'] + ';\n\n'
    
    return result

def generateEntity( entity ):

    print entity
    with open( 'template/entity.java', 'r' ) as file:

        resultFile = open('generated/' + entity['entityName'] + '.java', 'w')
        for line in file:
            match = re.search(r"\{\w+\}", line);
            if match:
                attribute = match.group(0)[1:-1]

                if attribute == 'attributes':
                    resultFile.write( generateAttributes( entity['attributes'] ) )
                else:
                    resultFile.write( line.format( **entity ) )
            else:
                resultFile.write(line)

        resultFile.close()

def generateRepository( entity ):

    with open( 'template/repository.java', 'r' ) as file:

        resultFile = open('generated/I' + entity['entityName'] + 'Repository.java', 'w')
        for line in file:
            match = re.search(r"\{\w+\}", line);
            if match:
                attribute = match.group(0)[1:-1]

                resultFile.write( line.format( **entity ) )
            else:
                resultFile.write(line)

        resultFile.close()

def main():
    if len(sys.argv) < 2:
        print "Deve ser passado o arquivo de configuração como parâmetro."
        return

    readConf( sys.argv[1] )

    for entity in config['entities']:
        generateEntity( entity )
        generateRepository( entity )

main()