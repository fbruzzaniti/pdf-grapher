# pdf-grapher (Beta Release) #

pdf-grapher is a Python script that utilises the [pydot](https://code.google.com/p/pydot/) library and Dider Stevens [pdf-parser](http://blog.didierstevens.com/programs/pdf-tools/) script to graph basic elements of a PDF file. pdf-grapher helps analysts understand the relationships of objects to each other and to suspicious elements of a malecious PDF file. The graph nodes represent PDF objects (Obj). Red nodes contain or reference elements that are commonly used in malicious PDF's. Yellow nodes denote suspicious elements, which may be malicious.  The edges (arrows) represent References from one Obj to another.  The graphs can be created as svg, png, vmrl and .dot files. If your viewer supports html links then clicking on nodes within the svg and dot graphs will display an ascii dump of the obj (node) clicked.

**Download:**
Browse the source or download the latest pdf-grapher.py [here](https://code.google.com/p/pdf-grapher/source/browse/pdf-grapher.py)

**Basic Example, malicious elements in red, suspecious yellow and normal green:**

| ![https://pdf-grapher.googlecode.com/svn/wiki/test-js.png](https://pdf-grapher.googlecode.com/svn/wiki/test-js.png) |
|:--------------------------------------------------------------------------------------------------------------------|


**An example of viewing a graph produced by pdf-grapher using ZRGViewer:**
| ![https://pdf-grapher.googlecode.com/svn/wiki/zgrviewer.png](https://pdf-grapher.googlecode.com/svn/wiki/zgrviewer.png) |
|:------------------------------------------------------------------------------------------------------------------------|