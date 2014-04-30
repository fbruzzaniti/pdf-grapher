#!/usr/bin/python

#Source code put in the public domain by Frank Bruzzaniti, no Copyright
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

# History  
  #0.5 rev7 alligning version numbers with repo
  #0.5 rev8 added other indicators from PDFiD split between redNodeList[] (commmonly in malware) and yellowNodeList[] (suspicious)
  #0.5 rev9 added detection of non printable text in objects
  #0.5 rev9 added /EmbeddedFile to redNodeList[]
  #0.5 rev9 squashed pdf-parser errors when encountering files embeded with non-printable characters
  #0.5 rev10 fixed a bug where Type: of node was not displaying because of changes I had made in Rev9				

# BUGS:
  #If you get the error "Couldn't import dot_parser, loading of dot files will not be possible." try this:
    #pip uninstall pyparsing
    #pip install -Iv https://pypi.python.org/packages/source/p/pyparsing/pyparsing-1.5.7.tar.gz#md5=9be0fcdcc595199c646ab317c1d9a709
    #pip install pydot

# TODO:
  #Test with objects that have revisions.
  #Cache getObjType lookups in a list do pdf-parser is not called again later to resolve ref's
  #Tidy up code
  #Create html template for obj's in log dir. E.g. click in node takes u to html links to pdf-parser output, raw dump, file results, hex, strings, etc
  #Test on windows
  #Add stream/binary object extraction
  #Automated analysis of node relationships/patterns E.g. /AA -> /JS is more suspicious than just /JS or /AA	


import pydot, os, sys, shutil, argparse, subprocess, string

redNodeList = ['/Encrypt','/AA','/OpenAction','/RichMedia','/Launch','/JS','/JavaScript','/EmbeddedFile'] #commonly found in malware
yellowNodeList = ['Contains stream','/JBIG2Decode','/ObjStm','/XFA'] #suspicious

#awesome argparse tute https://docs.python.org/2/howto/argparse.html
parser = argparse.ArgumentParser(usage='pdf-grapher, graphs objects and references from .pdf files.\n\nGraph Legend:\nRed = Contains or references JavaScript\nYellow = Contains Stream\nWhite = Referenced Obj not found\nGreen = No JS or stream detected\n\nWritten by Frank Bruzzaniti <frank.bruzzaniti@gmail.com>, no Copyright.\nThis program is free software: you can redistribute it and/or modify it\nunder the terms of the GNU General Public License.\nUse at your own risk.\n')
parser.add_argument('file', help='pdf to graph')
parser.add_argument('-o',type=str, help="graph output file format (default: svg)", choices=['dot', 'png', 'vrml'])
parser.add_argument('-n', help='no obj log files or directories created', action='store_true')
args = parser.parse_args()

if not args.n:

	log_path = "./" + args.file + "_log/" #set log path for extracted elements

	if os.path.exists(log_path): #check if log dir already exsists, if so delete it
		shutil.rmtree(log_path)

	os.mkdir(log_path) #create new log directories	
	os.mkdir(log_path + "obj/")

if not os.path.isfile('pdf-parser.py'):
	print 'pdf-grapher requires pdf-parser.py from http://blog.didierstevens.com/programs/pdf-tools\n'
	sys.exit()



def toAscii(s): #filter out nom-printables caused by embedded files
	return filter(lambda x: x in string.printable, s)

def isPrintable(s): #test if all characters are printable (they all should be in a PDF file)
	return all(c in string.printable for c in s)

def getObjType(objNum): 
	p2 = subprocess.Popen(["python", "pdf-parser.py",args.file,"-o",str(objNum.split()[0])], stdout=subprocess.PIPE,stderr=subprocess.PIPE) #Only uses major not revision number
	if not args.n:
		f = open(log_path + "obj/" + args.file + '.obj' + str(objNum.split()[0]),'w') #save extracted obj to file in log directory
		p3 = subprocess.Popen(["python", "pdf-parser.py",args.file,"-o",str(objNum.split()[0])], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		f.writelines(iter(p3.stdout.readline,''))
		f.close()	

	for line in iter(p2.stdout.readline,''):
		line = toAscii(line.rstrip()) 
		if "Type:" in line:
			if len(line.split()) > 1: 
				return str(line.split()[1]) #return obj type. E.g. /Page


graph = pydot.Dot(graph_type='digraph') #set graph type
		
p1 = subprocess.Popen(["python", "pdf-parser.py",args.file],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
for line in iter(p1.stdout.readline,''):
	#line = toAscii(line) #throw this back in if we start getting errors handling binary
	if len(line.split()) == 3 and line.split()[0] == "obj": #Look for an object and if found set the obj variable to it's value I.e. "<obj> <rev>"
		obj = str(line).replace("obj","").strip() #get object
		objType = getObjType(obj) #Get object type
		obj = obj + " (" + str(objType) + ")" #combine obj and type into var obj

		if not args.n:
			objUrl = '"' + log_path + "obj/" + args.file + '.obj' + obj.split()[0] + '"' #set local URL for extracted obj's
		else:
			objUrl = ''

		graph.add_node(pydot.Node("Obj " + toAscii(obj), style="filled", fillcolor="#00ff00", URL=(objUrl))) #add noded named "Obj <obj> <rev>				
	
	for item in yellowNodeList: #If list item found in line create yellow node
		if item in line: 
			graph.add_node(pydot.Node("Obj " + toAscii(obj), style="filled", fillcolor="yellow", URL=(objUrl)))


	for item in redNodeList: #If list item found in line create red node
		if item in line or not isPrintable(line): #if we find non printable text in the node mark it red
			graph.add_node(pydot.Node("Obj " + toAscii(obj), style="filled", fillcolor="red", URL=(objUrl))) #pdf-parse should take care of octal and hex obfuscation
	
	
	if len(line.split()) > 1 and line.split()[0] == "Referencing:": #Only print obj's that have ref's I.E. > 1
		for item in line.split(","):
			ref = item.replace("Referencing:","").replace("R","").strip() #get ref obj
			ref = ref + " (" + str(getObjType(ref)) + ")" #Combine re and ref type into var ref
			graph.add_edge(pydot.Edge("Obj " + toAscii(obj), "Obj " + toAscii(ref), label="")) #add edges


# Create graph, format selected by user

if args.o == 'dot':	
	graph.write_dot(os.path.splitext(args.file)[0] + ".dot")

if args.o == 'png':
	graph.write_png(os.path.splitext(args.file)[0] + ".png")

if args.o == 'vrml':
	graph.write_vrml(os.path.splitext(args.file)[0] + ".vrml") #this is in here so I have a work excuse to buy an occulus rift

if not args.o:
	graph.write_svg(os.path.splitext(args.file)[0] + ".svg")




		
		
		



