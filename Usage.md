# Usage #

## pdf-parser.py -h ##

```
usage: Graphs PDF objects and references for malware analysis.
pdf-parser.py -h for help

...

positional arguments:
  file               pdf to graph

optional arguments:
  -h, --help         show this help message and exit
  -f                 pass stream object through filter (FlateDecode,
                     ASCIIHexDecode, ASCII85Decode, LZWDecode
  -o {dot,png,vrml}  graph output file format (default: svg)
  -n                 no obj log files or directories created

```

## Command Line Arguments ##

  * _**-h**_: Displays help.<br><br>
<ul><li><i><b>-f</b></i>: Passes PDF objects through FlateDecode,ASCIIHexDecode, ASCII85Decode, LZWDecode filters, this will slow down the processing speed of the script but the objects may yield more information with their content un-filtered. -f is the equivalent of pdf-parser -f.<br><br>
</li><li><i><b>-o</b></i>: Species the output format of the graph. If -o is not specified then the svg format will be used.<br><br></li></ul>

<blockquote><table><thead><th> <i><b>DOT:</b></i> Graph description language format, useful to use with tools that specialize in viewing or processing graphs. Some DOT viewers will allow zoom, pan and restructuring of nodes. The dot format supports html linking of nodes allowing pdf-grapher to display obj information on click.</th></thead><tbody></blockquote></tbody></table>

<blockquote><table><thead><th> <i><b>PNG:</b></i> A bitmap image format, viewers only offer a static image that degrades when zoomed and allows no interaction to restructure nodes to activate html links. PNG is widely supported by many applications and is useful if you need to insert a graph into a document or webpage. </th></thead><tbody></blockquote></tbody></table>

<blockquote><table><thead><th><i><b>SVG:</b></i> Is an XML based format which offers compatibility with a wide number of applications (E.g. web browsers) but can also offer interaction via links and restructuring of nodes (if supported by the viewer).  SVG is the default file format used by pdf-grapher.</th></thead><tbody></blockquote></tbody></table>

<blockquote><table><thead><th><i><b>VRML:</b></i> Virtual Reality Modling Language. Ok I put this in here as a bit of a joke but it kind of works. With the advent of low cost VR equipment like the Occulus Rift coming out, I'll probably be experimenting to see if 3D visualisation could be useful in this case.</th></thead><tbody></blockquote></tbody></table>

<ul><li><i><b>-n</b></i>: By default pdf-grapher.py will create a file_pdf_logs directory for every file processed by pdf-grapher.py.  These logs contain the objs dumped by pdf-parser.py and displayed when you click on a graph node.  If -n is invoked on the commandline then no directories will be created (I.e. Nodes will not display obj content when clicked on). This should also improve the processing speed of pdf-grapher.py<br>
<hr />
<h2>Dependencies</h2></li></ul>

Python (Tested with 2.7.5)<br>
<br>
Linux (Probably, haven't tried it on Windows)<br>
<br>
pydot  (<a href='https://code.google.com/p/pydot/'>https://code.google.com/p/pydot/</a>)<br>
<br>
pdf-parser (<a href='http://blog.didierstevens.com/programs/pdf-tools/'>http://blog.didierstevens.com/programs/pdf-tools/</a>)<br>
<hr />
<h2>Complex Graphs</h2>

If your dealing with small-med graphs then using your browser to view SVG files should be fine.  For more complex graphs I'd suggest using a more specialized viewer like <b>ZGRViewer</b> (  <a href='http://zvtm.sourceforge.net/zgrviewer.html'>http://zvtm.sourceforge.net/zgrviewer.html</a>).<br>
<br>
<b>HINT:</b> Press spacebar when using ZGRViewer to view obj dump.<br>
<hr />
<h2>High Volume Processing</h2>

If your dealing with large volume's of PDF's then you may want to consider the following options:<br>
<br>
<ul><li><b>-n</b><i>will give you <b>FASTER</b> performance on slower HDD's but will give a you negligible performance boost on SSD drives.</li></ul></i>

<ul><li><b>-f</b><i>will <b>SLOW</b>  performance by ~10x, this should be avoided if performance is a concern.</li></ul></i>

<ul><li><b>-o png</b>