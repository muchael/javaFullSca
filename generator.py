#!/usr/bin/python
# coding: utf-8
'''
Created on 08/03/2018

@author: Newton Muchael
'''

import re, os
import sys
import json

config = {};

serviceMethods = {
'create': """    /**
	 * Método para inserir {entityName}
	 *
	 * @param {entityNameLowerCamelCase}
	 * @return
	 */
	@Override
	public {entityName} insert{entityName}( {entityName} {entityNameLowerCamelCase} )
	{{ 
        return this.{entityNameLowerCamelCase}Repository.save( {entityNameLowerCamelCase} );
	}}\n
""",
'read': """    /**
	 * Método para listar {entityName}
	 *
	 * @param {entityNameLowerCamelCase}
	 * @return
	 */
	@Override
	public {entityName} list{entityName}( String filter )
	{{ 
        return this.{entityNameLowerCamelCase}Repository.list{entityName}ByFilters( filter );
	}}\n
""",
'update':"""    /**
	 * Método para atualizar {entityName}
	 *
	 * @param {entityNameLowerCamelCase}
	 * @return
	 */
	@Override
	public {entityName} update{entityName}( {entityName} {entityNameLowerCamelCase} )
	{{ 
        return this.{entityNameLowerCamelCase}Repository.save( {entityNameLowerCamelCase} );
	}}\n
""",
'delete':"""    /**
	 * Método para remover {entityName}
	 *
	 * @param {entityNameLowerCamelCase}
	 * @return
	 */
	@Override
	public void remove{entityName}( Long id )
	{{ 
        return this.{entityNameLowerCamelCase}Repository.delete( id );
	}}\n
"""
}

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

    directory = 'generated/' + entity['package'].replace('.', '/') + '/entity/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open( 'template/entity.java', 'r' ) as file:

        resultFile = open(directory + entity['entityName'] + '.java', 'w')
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

def generateRepositoryFields( entity ):
    result = ''

    for atribute in entity['attributes']:
        if atribute['filter']:
            result += "\t\t\t\t\"(FILTER(" + entity['entityNameLowerCamelCase'] + '.' + atribute['name'] + ", :filter) = TRUE) \" + \n"

    if len(result) > 0:
        return result[0: -4] + '\n'
    
    return result


def generateRepository( entity ):

    directory = 'generated/' + entity['package'].replace('.', '/') + '/repository/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open( 'template/repository.java', 'r' ) as file:

        resultFile = open( directory + 'I' + entity['entityName'] + 'Repository.java', 'w')

        entityNameLowerCamelCase = entity['entityName'][0].lower() + entity['entityName'][1:]

        entity['entityNameLowerCamelCase'] = entityNameLowerCamelCase

        for line in file:
            match = re.search(r"\{\w+\}", line);
            if match:
                attribute = match.group(0)[1:-1]

                if attribute == 'attributes':
                    resultFile.write( generateRepositoryFields( entity ) )
                else:
                    resultFile.write( line.format( **entity ) )
            else:
                resultFile.write(line)

        resultFile.close()

def generateServiceMethods( entity ):
    result = ''

    for method in entity['service']:
        if method == 'C':
            result += serviceMethods['create']
        if method == 'R':
            result += serviceMethods['read']
        if method == 'U':
            result += serviceMethods['update']
        if method == 'D':
            result += serviceMethods['delete']

    return result.format( **entity )

def generateService( entity ):

    if 'service' not in entity:
        return

    directory = 'generated/' + entity['package'].replace('.', '/') + '/service/'
    if not os.path.exists(directory):
        os.makedirs(directory)


    with open( 'template/service.java', 'r' ) as file:

        resultFile = open(directory + entity['entityName'] + 'Service.java', 'w')

        entityNameLowerCamelCase = entity['entityName'][0].lower() + entity['entityName'][1:]

        entity['entityNameLowerCamelCase'] = entityNameLowerCamelCase

        for line in file:
            match = re.search(r"\{\w+\}", line);
            if match:
                attribute = match.group(0)[1:-1]

                if attribute == 'methods':
                    resultFile.write( generateServiceMethods( entity ) )
                else:
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
        generateService( entity )

main()