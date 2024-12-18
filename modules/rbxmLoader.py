
def mat3rotX(s, c): return 1, 0, 0, 0, c, -s, 0, s, c
def mat3rotY(s, c): return c, 0, s, 0, 1, 0, -s, 0, c
def mat3rotZ(s, c): return c, -s, 0, s, c, 0, 0, 0, 1
def mat3mul(a, b):
  a00, a01, a02, a10, a11, a12, a20, a21, a22 = a
  b00, b01, b02, b10, b11, b12, b20, b21, b22 = b
  return (
    a00 * b00 + a01 * b10 + a02 * b20, a00 * b01 + a01 * b11 + a02 * b21, a00 * b02 + a01 * b12 + a02 * b22,
    a10 * b00 + a11 * b10 + a12 * b20, a10 * b01 + a11 * b11 + a12 * b21, a10 * b02 + a11 * b12 + a12 * b22,
    a20 * b00 + a21 * b10 + a22 * b20, a20 * b01 + a21 * b11 + a22 * b21, a20 * b02 + a21 * b12 + a22 * b22)
pi180 = 0.017453292519943295
def fromEulerAngles(x, y, z): # проверено в Roblox Studio на print(CFrame.fromEulerAngles(math.rad(10), math.rad(20), math.rad(30)))
  x, y, z = x * pi180, y * pi180, z * pi180
  sx, cx, sy, cy, sz, cz = sin(x), cos(x), sin(y), cos(y), sin(z), cos(z)
  return mat3mul(mat3mul(mat3rotX(sx, cx), mat3rotY(sy, cy)), mat3rotZ(sz, cz))
def fromEulerAnglesYXZ(x, y, z): # проверено в Roblox Studio на print(CFrame.fromEulerAnglesYXZ(math.rad(10), math.rad(20), math.rad(30)))
  x, y, z = x * pi180, y * pi180, z * pi180
  sx, cx, sy, cy, sz, cz = sin(x), cos(x), sin(y), cos(y), sin(z), cos(z)
  return mat3mul(mat3mul(mat3rotY(sy, cy), mat3rotX(sx, cx)), mat3rotZ(sz, cz))

def getRotators():
  rotators = (
    None, None, (0, 0, 0), (90, 0, 0), None, (0, 180, 180), (-90, 0, 0), (0, 180, 90), None, (0, 90, 90),
    (0, 0, 90), None, (0, -90, 90), (-90, -90, 0), (0, -90, 0), None, (90, -90, 0), (0, 90, 180),
    None, None, (0, 180, 0), (-90, -180, 0), None, (0, 0, 180), (90, 180, 0), (0, 0, -90), None, (0, -90, -90),
    (0, -180, -90), None, (0, 90, -90), (90, 90, 0), (0, 90, 0), None, (-90, 90, 0), (0, -90, 180))
  #for i, j in enumerate(rotators):
  #  if j: print(hex(i), j) всё сошлось
  return tuple((fromEulerAnglesYXZ(rotator[0], rotator[1], rotator[2]) if rotator else None) for rotator in rotators)
  # также, properties explorer в Roblox Studio преобразует поворот именно по fromEulerAnglesYXZ, а не fromEulerAngles!
CFrameRotators = getRotators()
# print(CFrameRotators)

def transposedMul(mat):
  # только матрицы вращения дают единичную матрицу = transposed(mat) * mat
  r00, r01, r02, r10, r11, r12, r20, r21, r22 = mat
  return (
    r00 * r00 + r10 * r10 + r20 * r20, r00 * r01 + r10 * r11 + r20 * r21, r00 * r02 + r10 * r12 + r20 * r22,
    r01 * r00 + r11 * r10 + r21 * r20, r01 * r01 + r11 * r11 + r21 * r21, r01 * r02 + r11 * r12 + r21 * r22,
    r02 * r00 + r12 * r10 + r22 * r20, r02 * r01 + r12 * r11 + r22 * r21, r02 * r02 + r12 * r12 + r22 * r22)
def linalgNorm(a, b):
  return sum((a - b) ** 2 for a, b in zip(a, b)) ** 0.5
def isRotateMat(mat):
  return linalgNorm(transposedMul(mat), (1, 0, 0, 0, 1, 0, 0, 0, 1)) < 1e-14





def CFrame2mat(CFrame):
  if CFrame is None: return (1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)._a_float
  x, y, z, r00, r01, r02, r10, r11, r12, r20, r21, r22 = CFrame
  return (r00, r10, r20, 0, r01, r11, r21, 0, r02, r12, r22, 0, x, y, z, 1)._a_float
def CFrame2mat_onlyPos(CFrame):
  if CFrame is None: return (1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)._a_float
  return (1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, CFrame[0], CFrame[1], CFrame[2], 1)._a_float

def getCFrame(props):
  try: pivot = props["WorldPivotData"]
  except KeyError:
    try: pivot = props["CFrame"]
    except KeyError: return
  type, value = pivot
  if type == 0x10: return value # CFrame
  if type == 0x1e: # OptionalCoordinateFrame
    useful, cframe = value
    # if useful: return cframe
    return cframe

def getHumanoid(node):
  res = None
  for child in node["_childs"]:
    if child["_class"] == "Humanoid": res = child
  return res

def getSurfaceAppearance(node):
  res = None
  for child in node["_childs"]:
    if child["_class"] == "SurfaceAppearance": res = child
  return res

def getDecals(node):
  res = []
  for child in node["_childs"]:
    if child["_class"] == "Decal": res.append(child)
  return res

def checkString(prop):
  type, value = prop
  if type != 0x01: HALT("Это не String: %s" % prop)
  return value
def checkFloat32(prop):
  type, value = prop
  if type != 0x04: HALT("Это не Float32: %s" % prop)
  return value
def checkColor3(prop):
  type, value = prop
  if type != 0x0c: HALT("Это не Color3: %s" % prop)
  return value
def checkVector3(prop):
  type, value = prop
  if type != 0x0e: HALT("Это не Vector3: %s" % prop)
  return value
def checkCFrame(prop):
  type, value = prop
  if type != 0x10: HALT("Это не CFrame: %s" % prop)
  return value
def checkEnum(prop, arr):
  type, value = prop
  if type != 0x12: HALT("Это не Enum: %s" % prop)
  if value < 0 or value >= len(arr): HALT("Значение Enum за пределами: %s (0..%s)" % (value, len(arr) - 1))
  return value, arr[value]
def checkReferent(prop):
  type, value = prop
  if type != 0x13: HALT("Это не Referent: %s" % prop)
  return value
def checkColor3uint8(prop):
  type, value = prop
  if type != 0x1a: HALT("Это не Color3uint8: %s" % prop)
  return value



def mat_invertor(mat):
  invertM(mat, 0, mat, 0)
  return mat

def makeChainTree(node, used, level = ""):
  id = node["_id"]
  if id in used: return
  used.add(id)
  # print("%s%s %s" % (level, node["_name"], id))
  # level += "| "
  return tuple((CFrame2mat(C0), mat_invertor(CFrame2mat(C1)), ref_node["_id"], makeChainTree(ref_node, used, level)) for ref_node, C0, C1 in node["_refs1"])



def getCube():
  frags = []
  fragsAppend = frags.append
  def add_poly(a, b, c):
    x1, y1, z1, u1, v1 = edges[a]
    x2, y2, z2, u2, v2 = edges[b]
    x3, y3, z3, u3, v3 = edges[c]
    dx1 = x1 - x2
    dy1 = y1 - y2
    dz1 = z1 - z2
    dx2 = x1 - x3
    dy2 = y1 - y3
    dz2 = z1 - z3
    nx = dy1 * dz2 - dz1 * dy2
    ny = dz1 * dx2 - dx1 * dz2
    nz = dx1 * dy2 - dy1 * dx2
    fragsAppend((
      (x1, y1, z1, nx, ny, nz, u1, v1, 0, 0, 0, 0),
      (x2, y2, z2, nx, ny, nz, u2, v2, 0, 0, 0, 0),
      (x3, y3, z3, nx, ny, nz, u3, v3, 0, 0, 0, 0),
    ))
  def add_square(a, b, c, a2, b2, c2):
    add_poly(a, b, c)
    add_poly(a2, b2, c2)
  edges = (
    (-1, -1, -1,   0, 0), # 0
    ( 1, -1, -1,   1, 0), # 1
    ( 1, -1,  1,   1, 1), # 2
    (-1, -1,  1,   0, 1), # 3
    (-1,  1, -1,   0, 0), # 4
    ( 1,  1, -1,   1, 0), # 5
    ( 1,  1,  1,   1, 1), # 6
    (-1,  1,  1,   0, 1), # 7
  )
  add_square(0,  1,  2,  0,  2,  3) # дно куба
  add_square(0,  1,  4,  1,  4,  5) # фронт
  add_square(1,  5,  2,  2,  5,  6) # правый бок
  add_square(2,  7,  3,  2,  6,  7) # тыл
  add_square(3,  7,  0,  0,  7,  4) # левый бок
  add_square(4,  7,  5,  5,  7,  6) # верх куба
  return buildModel(frags)



def modelHandler(root, root_pos):
  mesh_cache = STORAGE("mesh_cache")

  def mesh2model(mesh_id):
    try:
      model = mesh_cache[mesh_id]
      # print("Cached mesh:", mesh_id)
    except KeyError:
      mesh = cdnLoader(mesh_id)
      if not mesh: return

      model = meshReader(mesh, True)
      if not model: return

      mesh_cache[mesh_id] = model
    return model

  def meshPart(node, pos, accessory, is_character_part):
    props = node["_props"]
    id = node["_id"]
    isBody = is_character_part and not accessory
    isPart = node["_class"] == "Part"

    #print("...", checkVector3(props["size"]), checkVector3(props["InitialSize"]))
    x, y, z = checkVector3(props["size"])
    ix, iy, iz = (2, 2, 2) if isPart else checkVector3(props["InitialSize"])
    info = {"size": (x / ix, y / iy, z / iz), "node": node}
    scaleMat = (x / ix, 0, 0, 0, 0, y / iy, 0, 0, 0, 0, z / iz, 0, 0, 0, 0, 1)._a_float
    multiplyMM(pos, 0, pos, 0, scaleMat, 0)
    # multiplyMM(pos, 0, scaleMat, 0, pos, 0) не просёк разницы. Возможно, порядок действительно не играет никакой роли

    if isPart:
      shape, shapeName = checkEnum(props["shape"], ("Ball", "Block", "Cylinder", "Wedge", "CornerWedge")) # в роблоксе: Enum.PartType
      # print(shape, shapeName)
      model = getCube()
      return
      if shape != 1: HALT("Пока поддерживается только форма Block, а не " + shapeName)
      model_name = "cube"
    else:
      model_name = checkString(props["MeshId"])
      model = mesh2model(model_name)
      if model is None: return
    VBOdata, IBOdata = model

    decals = getDecals(node)
    if decals:
      decal_props = decals[0]["_props"]
      texture = cdnLoader(checkString(decal_props["Texture"]))
      face = checkEnum(decal_props["Face"], ("Right", "Top", "Back", "Left", "Bottom", "Front")) # в роблоксе: Enum.NormalId
      r, g, b = checkColor3(decal_props["Color3"])
      a = checkFloat32(decal_props["Transparency"])
      # print("•", len(texture), texture[:32], face, (r, g, b, 1 - a))
      info["decal"] = texture, face, (r, g, b, 1 - a)

    model_data = VBOdata, IBOdata, model_name
    SA = getSurfaceAppearance(node)
    if SA:
      if isPart: HALT("Пока не поддерживается Part + SA :/")
      SA_props = SA["_props"]
      color = checkColor3(SA_props["Color"])
      colorMap = cdnLoader(checkString(SA_props["ColorMap"]))
      metalnessMap = cdnLoader(checkString(SA_props["MetalnessMap"]))
      normalMap = cdnLoader(checkString(SA_props["NormalMap"]))
      roughnessMap = cdnLoader(checkString(SA_props["RoughnessMap"]))
      PBR_textures = color, colorMap, (metalnessMap, normalMap, roughnessMap)
      tex = PBR_textures
    else:
      r, g, b = checkColor3uint8(props["Color3uint8"])
      a = checkFloat32(props["Transparency"])
      texture = None if isPart else cdnLoader(checkString(props["TextureID"]))
      #texture = ((texture, (1, 1, 1, 1)),) if texture else ()
      #tex = (r / 255, g / 255, b / 255, 0), texture
      if texture:
        texture = texture, (1, 1, 1, 1 - a)
        tex = (0, 0, 0, 0), (texture,)
      else: tex = (r / 255, g / 255, b / 255, 1 - a), ()

    result = node, pos, model_data, tex, isBody, info
    return SA, result

  def recurs(node, root_pos, lvl):
    nonlocal motorTree

    id, parent, childs, className, name = node["_id"], node["_parent"], node["_childs"], node["_class"], node["_name"]
    props = node["_props"]
    print("  " * lvl, name, className)

    if root_pos is None:
      pos = getCFrame(props)
      if pos is not None:
        # print("POS FIND", pos, root_pos is None)
        mat = CFrame2mat_onlyPos(pos)
        root_pos = FLOAT.new_array(16)
        invertM(root_pos, 0, mat, 0)

    if className in ("Model", "Tool"):
      humanoid = getHumanoid(node)
      # humanoid = None
      if humanoid is not None:
        # print("👤", humanoid["_props"])
        primary = node["_refs"]["PrimaryPart"]
        motorTree = makeChainTree(primary, used_in_tree)
        # print("🌴", motorTree)
        # huPosit = recalcChainPos((0, 0, 0), motorTree)
    elif className in ("Part", "MeshPart"):
      # print("%s %s %s\n" % (id, name, props))
      #print(props["size"][1], props["VertexCount"][1], props["TextureID"][1], props["MeshId"][1], props["Transparency"][1], props["DoubleSided"][1], "\n")
      accessory = parent["_class"] == "Accessory"
      if accessory: name = parent["_name"]
      # print("LOADING:", name)

      is_character_part = id in used_in_tree

      if is_character_part: pos = (1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)._a_float
      else:
        pos = CFrame2mat(getCFrame(props))
        multiplyMM(pos, 0, root_pos, 0, pos, 0)
        # print("POS:", pos[:])

      data = meshPart(node, pos, accessory, is_character_part)
      if data is not None:
        isSA, mesh = data
        if is_character_part:
          if isSA: characterPBR_models.append(mesh)
          else: characterModels.append(mesh)
        else:
          if isSA: PBR_models.append(mesh)
          else: models.append(mesh)

    elif className == "BodyColors":
      bodyColors = {
        "head": checkColor3(props["HeadColor3"]),
        "leftArm": checkColor3(props["LeftArmColor3"]),
        "leftLeg": checkColor3(props["LeftLegColor3"]),
        "rightArm": checkColor3(props["RightArmColor3"]),
        "rightLeg": checkColor3(props["RightLegColor3"]),
        "torso": checkColor3(props["TorsoColor3"]),
      }
      # print("🏵️:", bodyColors) # на деле ненужный параметр, т.к. у всех частей тела (а их больше, чем здесь 6 штук) цвета прописаны отдельно
    elif className == "Shirt":
      print("SHIRT:", name)
      color = checkColor3(props["Color3"])
      asset = cdnLoader(checkString(props["ShirtTemplate"]))
      shirts.append((color, asset))
    elif className == "Pants":
      print("PANTS:", name)
      color = checkColor3(props["Color3"])
      asset = cdnLoader(checkString(props["PantsTemplate"]))
      pantss.append((color, asset))

    lvl += 1
    for child in childs: recurs(child, root_pos, lvl)

  models = []
  PBR_models = []
  shirts = []
  pantss = []

  motorTree = None
  used_in_tree = set()
  characterModels = []
  characterPBR_models = []

  recurs(root, root_pos, 0)
  character = motorTree, characterModels, characterPBR_models

  return models, PBR_models, shirts, pantss, character



def modelLoader(root, name, renderer, root_pos):
  global dbgTextures

  cache = STORAGE("rbxm_modelHandler_cache")
  try: models, PBR_models, shirts, pantss, character = cache[name]
  except KeyError:
    models, PBR_models, shirts, pantss, character = record = modelHandler(root, root_pos)
    cache[name] = record

  # pants = newTexture2(pantss[0][1])
  # print("🐾pants texture:", pants)

  notCharacter = CharacterModel((None, models, PBR_models), renderer)
  union = UnionModel(notCharacter.models)
  PBR_union = UnionModel(notCharacter.PBR_models)

  charModel = None if character[0] is None else CharacterModel(character, renderer)
  print("🐕", len(models), len(PBR_models), len(character[1]), len(character[2]))

  return union, PBR_union, charModel
