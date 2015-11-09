pdf-grapher is a Python script that utilises the pydot library and Dider Stevens pdf-parser script to graph basic elements of a PDF file. pdf-grapher helps analysts understand the relationships of objects to each other and to suspicious elements of a malicious PDF file. The graph nodes represent PDF objects (Obj). Red nodes contain or reference elements that are commonly used in malicious PDF's. Yellow nodes denote suspicious elements, which may be malicious. The edges (arrows) represent References from one Obj to another. The graphs can be created as svg, png, vmrl and .dot files. If your viewer supports html links then clicking on nodes within the svg and dot graphs will display an ascii dump of the obj (node) clicked.

Basic Example, malicious elements in red, suspecious yellow and normal green:
https://raw.githubusercontent.com/fbruzzaniti/pdf-grapher/wiki/test-js.png

Complex Example, viewing a graph produced by pdf-grapher using ZRGViewer:
https://raw.githubusercontent.com/fbruzzaniti/pdf-grapher/wiki/zgrviewer.png

Install Instructions:               
https://github.com/fbruzzaniti/pdf-grapher/blob/wiki/Installation.md

Usage Instructions:             
https://github.com/fbruzzaniti/pdf-grapher/blob/wiki/Usage.md

Graph Colour Refrence:             
https://github.com/fbruzzaniti/pdf-grapher/blob/wiki/GraphReference.md

