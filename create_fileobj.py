import sys
from mtypes.creators.file_factory import FileFactory

f = FileFactory()
fname="/debianMirror/Warehouse/Warehouse/DOCUMENTOS IMPORTANTES/Inteco Dev machines/lab/home/jmfoces/workspace/refactor_svn"
fileobj = f.create_file(fname)

print fileobj
print fileobj.is_source_container()




