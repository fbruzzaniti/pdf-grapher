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
	#0.5	SVG is default format, added ability to click on obj and see extracted object
	#0.6	changed log dir to file_log 
	#0.6	used hex notation to correct colour in SVG
	#0.6    added VRML so I now I have a work reason to buy the Occulus Rift 				
	#0.6	added command line options for png, vrml and dot
	#0.6	fixed a bug that prevented obj type from displaying correctly
	#0.6	added check for pdf-parser.py and error w/ help if not found
	#0.6	updated graph legend with concise explanations
	#0.6    added -n arg to disable generation of obj log folders
	#0.7	added initial support for detecting embedded files

# BUGS:
  #If you get the error "Couldn't import dot_parser, loading of dot files will not be possible." try this:
    #pip uninstall pyparsing
    #pip install -Iv https://pypi.python.org/packages/source/p/pyparsing/pyparsing-1.5.7.tar.gz#md5=9be0fcdcc595199c646ab317c1d9a709
    #pip install pydot

#TODO: Test with objects that have revisions.
#TODO: Cache getObjType lookups in a list do pdf-parser is not called again later to resolve ref's
#TODO: Tidy up code
#TODO: Create html template for obj's in log dir
#TODO: Test on windows
#TODO: Add stream extraction
#TODO: Add embedded file extraction
#TODO: squash popen err printing on console E.e. pdf-parser errors (non-fatal) with some embedded files


import pydot, os, sys, shutil, argparse, subprocess, string

#awesome argparse tute https://docs.python.org/2/howto/argparse.html
parser = argparse.ArgumentParser(usage='pdf-grapher, graphs objects and references from .pdf files.\n\nGraph Legend:\nRed = Contains or references JavaScript\nYellow = Contains Stream\nWhite = Referenced Obj not found\nGreen = No JS or stream detected\n')
parser.add_argument('file', help='pdf to graph')
parser.add_argument('-o',type=str, help="graph output file format (default: svg)", choices=['dot', 'png', 'vrml'])
parser.add_argument('-n', help='no obj log files or directories created', action='store_true')
args = parser.parse_args()

if not args.n:

	log_path = "./" + sys.argv[1] + "_log/" #set log path for extracted elements

	if os.path.exists(log_path): #check if log dir already exsists, if so delete it
		shutil.rmtree(log_path)

	os.mkdir(log_path) #create new log directories	
	os.mkdir(log_path + "obj/")

if not os.path.isfile('pdf-parser.py'):
	print 'pdf-grapher requires pdf-parser.py from http://blog.didierstevens.com/programs/pdf-tools\n'
	sys.exit()

graph = pydot.Dot(graph_type='digraph') #set graph type

def toAscii(s): #filter out nom-printables caused by embedded files
	return filter(lambda x: x in string.printable, s)

def getObjType(objNum): 

	p = subprocess.Popen(["python", "pdf-parser.py",sys.argv[1],"-o",str(objNum.split()[0])], stdout=subprocess.PIPE) #Only uses major not revision number
	
	if not args.n:
		f = open(log_path + "obj/" + sys.argv[1] + '.obj' + str(objNum.split()[0]),'w') #save extracted obj to file in log directory
		f.writelines(os.popen("python pdf-parser.py " + sys.argv[1] + " -o " + str(objNum.split()[0])))
		f.close()	

	for line in iter(p.stdout.readline,''):
		line = toAscii(line.rstrip()) 
		if "Type:" in line:
			if len(line.split()) > 1: 
				return str(line.split()[1]) #return obj type. E.g. /Page
		

for line in os.popen("python pdf-parser.py " + sys.argv[1]): #I could just read the pdf as text, but pdf-parser outputs it's own parsed results so they might be saner
	line = toAscii(line)
	if len(line.split()) == 3 and line.split()[0] == "obj": #Look for an object and if found set the obj variable to it's value I.e. "<obj> <rev>"
		obj = str(line).replace("obj","").strip() #get object
		objType = getObjType(obj) #Get object type
		obj = obj + " (" + str(objType) + ")" #combine obj and type into var obj

		if not args.n:
			objUrl = '"' + log_path + "obj/" + sys.argv[1] + '.obj' + obj.split()[0] + '"' #set local URL for extracted obj's
		else:
			objUrl = ''

		graph.add_node(pydot.Node("Obj " + obj, style="filled", fillcolor="#00ff00", URL=(objUrl))) #add noded named "Obj <obj> <rev>				
	
	if " /JS " in line or " /JavaScript " in line: #look for javascript tags if so colour the node red
		graph.add_node(pydot.Node("Obj " + obj, style="filled", fillcolor="red", URL=(objUrl))) #pdf-parse should take care of octal and hex obfuscation

	if "Contains stream" in line: #Look for stream tag if so colour the node yellow
		graph.add_node(pydot.Node("Obj " + obj, style="filled", fillcolor="yellow", URL=(objUrl)))
	

	if len(line.split()) > 1 and line.split()[0] == "Referencing:": #Only print obj's that have ref's I.E. > 1
		for item in line.split(","):
			ref = item.replace("Referencing:","").replace("R","").strip() #get ref obj
			ref = ref + " (" + str(getObjType(ref)) + ")" #Combine re and ref type into var ref
			graph.add_edge(pydot.Edge("Obj " + obj, "Obj " + ref, label="")) #add edges


# Create graph, format selected by user

if args.o == 'dot':	
	graph.write_dot(os.path.splitext(sys.argv[1])[0] + ".dot")

if args.o == 'png':
	graph.write_png(os.path.splitext(sys.argv[1])[0] + ".png")

if args.o == 'vrml':
	graph.write_vrml(os.path.splitext(sys.argv[1])[0] + ".vrml")

if not args.o:
	graph.write_svg(os.path.splitext(sys.argv[1])[0] + ".svg")




		
		
		


