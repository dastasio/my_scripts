def LoadOBJ(path):
    File = open(path, 'r')
    vLines = ['filler']
    vtLines = ['filler']
    vnLines = ['filler']
    fLines = []
    Vertices = []
    for Line in File.readlines():
        if Line[0] == 'v':
            if Line[1] == 't':
                vtLines.append(Line)
            elif Line[1] == 'n':
                vnLines.append(Line)
            else:
                vLines.append(Line)
        elif Line[0] == 'f':
            fLines.append(Line)
    for fLine in fLines:
        VerticesStrings = fLine.replace('f', '').strip().split(' ')
        for VertexString in VerticesStrings:
            Data = VertexString.split('/')
            VertexPositionIndex = Data[0]
            VertexTextureIndex = Data[1]
            VertexNormalIndex = Data[2]
            Vertex = [0, 0, 0]
            Vertex[0] = vLines[int(VertexPositionIndex)].replace('v', '').strip()
            if VertexTextureIndex != '':
                Vertex[2] = vtLines[int(VertexTextureIndex)].replace('vt','').strip()
            if VertexNormalIndex != '':
                Vertex[1] = vnLines[int(VertexNormalIndex)].replace('vn','').strip()
            Vertices.append(Vertex)
    
    n = 0
    for v in Vertices:
        print(n, v)
        n += 1
        

LoadOBJ('scene.obj')