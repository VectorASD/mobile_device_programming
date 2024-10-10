
def printVertex(px, py, pz, nx, ny, nz, tU, tV, tx, ty, tz, ts, r = None, g = None, b = None, a = None):
  print("pos:", px, py, pz)
  print("norm:", nx, ny, nz)
  print("UV:", tU, tV)
  print("tangent:", tx, ty, tz, ts)
  if r is not None: print("color:", r, g, b, a)
  print()

def readVertexes36(mesh, numVerts):
  VBOdata = []
  for i in range(numVerts):
    px, py, pz, nx, ny, nz, tU, tV, tx, ty, tz, ts = mesh.unpack("<8f4b")
    tx /= 127; ty /= 127; tz /= 127; ts /= 127
    VBOdata.extend((px, py, pz, 1, 1, 1, 1, tU, tV))
    if i < 10: printVertex(px, py, pz, nx, ny, nz, tU, tV, tx, ty, tz, ts)
  return VBOdata

def readVertexes40(mesh, numVerts):
  VBOdata = []
  for i in range(numVerts):
    px, py, pz, nx, ny, nz, tU, tV, tx, ty, tz, ts, r, g, b, a = mesh.unpack("<8f4b4B")
    tx /= 127; ty /= 127; tz /= 127; ts /= 127
    r /= 255; g /= 255; b /= 255; a /= 255
    VBOdata.extend((px, py, pz, r, g, b, a, tU, tV))
    if i < 10: printVertex(px, py, pz, nx, ny, nz, tU, tV, tx, ty, tz, ts, r, g, b, a)
  return VBOdata

def meshFaces(mesh, numFaces):
  IBOdata = mesh.unpack("<%sI" % (numFaces * 3))
  #print(IBOdata[:30])
  return IBOdata



def meshReader2_00(mesh):
  sizeof_MeshHeader, sizeof_Vertex, sizeof_Face, numVerts, numFaces = mesh.unpack("<HBBII")
  if sizeof_MeshHeader != 12: exit("Странный sizeof_MeshHeader v2.00: %s" % sizeof_MeshHeader)
  if sizeof_Vertex not in (36, 40): exit("Странный sizeof_Vertex: %s" % sizeof_Vertex)
  if sizeof_Face != 12: exit("Странный sizeof_Face: %s" % sizeof_Face)
  VBOdata = readVertexes36(mesh, numVerts) if sizeof_Vertex == 36 else readVertexes40(mesh, numVerts)
  IBOdata = meshFaces(mesh, numFaces)
  return VBOdata, IBOdata

def meshReader3_00(mesh):
  print("🙂‍↔️🙂‍↔️🙂‍↔️")
  sizeof_MeshHeader, sizeof_Vertex, sizeof_Face, sizeof_LOD, numLODs, numVerts, numFaces = mesh.unpack("<HBBHHII")
  if sizeof_MeshHeader != 16: exit("Странный sizeof_MeshHeader v3.00: %s" % sizeof_MeshHeader)
  if sizeof_Vertex not in (36, 40): exit("Странный sizeof_Vertex: %s" % sizeof_Vertex)
  if sizeof_Face != 12: exit("Странный sizeof_Face: %s" % sizeof_Face)
  if sizeof_LOD != 4: exit("Странный sizeof_LOD: %s" % sizeof_LOD)
  # a, b, c = sizeof_Vertex * numVerts, sizeof_Face * numFaces, sizeof_LOD * numLODs
  # print("Vertexes size:", a)
  # print("Faces size:", b)
  # print("LODs size:", c)
  # print("all:", a + b + c)
  # print("доступно:", len(mesh.read())) сошлось с параметром "all"
  VBOdata = readVertexes36(mesh, numVerts) if sizeof_Vertex == 36 else readVertexes40(mesh, numVerts)
  IBOdata = meshFaces(mesh, numFaces)
  LODs = mesh.unpack("<%sI" % numLODs)
  print("LODs:", LODs)
  print("🙂‍↔️🙂‍↔️🙂‍↔️")
  return VBOdata, IBOdata



def meshReader(mesh):
  mesh = BytesIO(mesh)
  s = []
  while True:
    let = mesh.read(1)
    if let == b"\n": break
    s.append(let)
  version = b"".join(s)

  model = None
  if version == b"version 2.00": model = meshReader2_00(mesh)
  elif version == b"version 3.00": model = meshReader3_00(mesh)
  else: print("UNKNOWN MESH VERSION: %s" % version)
  return model
