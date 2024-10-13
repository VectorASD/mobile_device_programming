
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
    #if i < 10: printVertex(px, py, pz, nx, ny, nz, tU, tV, tx, ty, tz, ts)
  return VBOdata

def readVertexes40(mesh, numVerts):
  VBOdata = []
  for i in range(numVerts):
    px, py, pz, nx, ny, nz, tU, tV, tx, ty, tz, ts, r, g, b, a = mesh.unpack("<8f4b4B")
    tx /= 127; ty /= 127; tz /= 127; ts /= 127
    # tU = tV = -1
    VBOdata.extend((px, py, pz, r / 255, g / 255, b / 255, a / 255, tU, tV))
    #if i < 10: printVertex(px, py, pz, nx, ny, nz, tU, tV, tx, ty, tz, ts, r, g, b, a)
  return VBOdata

def meshFaces(mesh, numFaces):
  IBOdata = mesh.unpack("<%sI" % (numFaces * 3))
  #print(IBOdata[:30])
  return IBOdata

def Envelope(mesh, numVerts):
  return [(mesh.read(4), mesh.read(4)) for i in range(numVerts)]



def meshReader2_00(mesh):
  sizeof_MeshHeader, sizeof_Vertex, sizeof_Face, numVerts, numFaces = mesh.unpack("<HBBII")
  if sizeof_MeshHeader != 12: exit("Странный sizeof_MeshHeader v2.00: %s" % sizeof_MeshHeader)
  if sizeof_Vertex not in (36, 40): exit("Странный sizeof_Vertex: %s" % sizeof_Vertex)
  if sizeof_Face != 12: exit("Странный sizeof_Face: %s" % sizeof_Face)
  VBOdata = readVertexes36(mesh, numVerts) if sizeof_Vertex == 36 else readVertexes40(mesh, numVerts)
  IBOdata = meshFaces(mesh, numFaces)
  what = mesh.read()
  if what: exit("Не до конца считанная сетка v2.00: %s" % mesh.hex())
  return VBOdata, IBOdata

def meshReader3_00(mesh):
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
  print("Вершин:", numVerts, "Полигонов:", numFaces, "Уровней детализации:", numLODs - 1)
  VBOdata = readVertexes36(mesh, numVerts) if sizeof_Vertex == 36 else readVertexes40(mesh, numVerts)
  IBOdata = meshFaces(mesh, numFaces)
  LODs = mesh.unpack("<%sI" % numLODs)
  print("LODs:", LODs)
  what = mesh.read()
  if what: exit("Не до конца считанная сетка v3.00: %s" % mesh.hex())
  a, b = LODs[0], LODs[1]
  IBOdata = IBOdata[a*3 : b*3]
  return VBOdata, IBOdata

def meshReaderBase4_5(mesh, numVerts, numFaces, numLODs, numBones):
  VBOdata = readVertexes40(mesh, numVerts)
  if numBones: Envelope(mesh, numVerts)
  IBOdata = meshFaces(mesh, numFaces)
  LODs = mesh.unpack("<%sI" % numLODs)
  print("LODs:", LODs)
  a, b = LODs[0], LODs[1] # выбираю LOD с самым высоким разрешением
  IBOdata = IBOdata[a*3 : b*3]
  return VBOdata, IBOdata

def meshReader4_00(mesh):
  print("🙂‍↔️🙂‍↔️🙂‍↔️")
  sizeof_MeshHeader, lodType, numVerts, numFaces, numLODs, numBones, sizeof_boneNamesBuffer, numSubsets, numHighQualityLODs, unused = mesh.unpack("<HHIIHHIHBB")
  if sizeof_MeshHeader != 24: exit("Странный sizeof_MeshHeader v4.00: %s" % sizeof_MeshHeader)
  if unused: exit("Странный unused: %s" % unused)

  lodTypeName = {0: "None", 1: "Unknown", 2: "RbxSimplifier", 3: "ZeuxMeshOptimizer"}.get(lodType, "?%s" % lodType)
  print("LOD type:", lodTypeName)
  print("Вершин:", numVerts, "Полигонов:", numFaces, "Уровней детализации:", numLODs - 1)
  print("Костей:", numBones, "...", sizeof_boneNamesBuffer, numSubsets, numHighQualityLODs)

  VBOdata, IBOdata = meshReaderBase4_5(mesh, numVerts, numFaces, numLODs, numBones)
  print("🙂‍↔️🙂‍↔️🙂‍↔️")
  return VBOdata, IBOdata

def meshReader5_00(mesh):
  print("🙂‍↔️🔥🙂‍↔️")
  sizeof_MeshHeader, lodType, numVerts, numFaces, numLODs, numBones, sizeof_boneNamesBuffer, numSubsets, numHighQualityLODs, unusedPadding, facsDataFormat, facsDataSize = mesh.unpack("<HHIIHHIHBBII")
  if sizeof_MeshHeader != 32: exit("Странный sizeof_MeshHeader v5.00: %s" % sizeof_MeshHeader)
  if unusedPadding: exit("Странный unusedPadding: %s" % unusedPadding)

  lodTypeName = {0: "None", 1: "Unknown", 2: "RbxSimplifier", 3: "ZeuxMeshOptimizer"}.get(lodType, "?%s" % lodType)
  print("LOD type:", lodTypeName)
  print("Вершин:", numVerts, "Полигонов:", numFaces, "Уровней детализации:", numLODs - 1)
  print("Костей:", numBones, "...", sizeof_boneNamesBuffer, numSubsets, numHighQualityLODs)
  print("Facial Action Coding System:", facsDataFormat, facsDataSize)

  VBOdata, IBOdata = meshReaderBase4_5(mesh, numVerts, numFaces, numLODs, numBones)
  print("🙂‍↔️🔥🙂‍↔️")
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
  elif version in (b"version 3.00", b"version 3.01"): model = meshReader3_00(mesh)
  elif version in (b"version 4.00", b"version 4.01"): model = meshReader4_00(mesh)
  elif version == b"version 5.00": model = meshReader5_00(mesh)
  else: print("UNKNOWN MESH VERSION: %s" % version)
  return model
