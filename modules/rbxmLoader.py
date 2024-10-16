
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



def getCFrame(props):
  try: pivot = props["WorldPivotData"]
  except KeyError:
    try: pivot = props["CFrame"]
    except KeyError: return
  type, value = pivot
  if type == 0x10: return value # CFrame
  if type == 0x1e: # OptionalCoordinateFrame
    useful, cframe = value
    if useful: return cframe

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

def checkString(prop):
  type, value = prop
  if type != 0x01: exit("Это не String: %s" % prop)
  return value
def checkColor3(prop):
  type, value = prop
  if type != 0x0c: exit("Это не Color3: %s" % prop)
  return value
def checkCFrame(prop):
  type, value = prop
  if type != 0x10: exit("Это не CFrame: %s" % prop)
  return value
def checkReferent(prop):
  type, value = prop
  if type != 0x13: exit("Это не Referent: %s" % prop)
  return value
def checkColor3uint8(prop):
  type, value = prop
  if type != 0x1a: exit("Это не Color3uint8: %s" % prop)
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

def modelHandler(root):
  def recurs(node, root_pos):
    nonlocal motorTree

    id, parent, childs, className, name = node["_id"], node["_parent"], node["_childs"], node["_class"], node["_name"]
    props = node["_props"]
    is_character_part = id in used_in_tree

    if root_pos is None:
      pos = getCFrame(props)
      if pos is not None:
        mat = CFrame2mat(pos)
        root_pos = FLOAT.new_array(16)
        invertM(root_pos, 0, mat, 0)

    if className == "Model":
      humanoid = getHumanoid(node)
      if humanoid is not None:
        # print("👤", humanoid["_props"])
        primary = node["_refs"]["PrimaryPart"]
        motorTree = makeChainTree(primary, used_in_tree)
        # print("🌴", motorTree)
        # huPosit = recalcChainPos((0, 0, 0), motorTree)
    elif className == "MeshPart":
      # print("%s %s %s\n" % (id, name, props))
      #print(props["size"][1], props["VertexCount"][1], props["TextureID"][1], props["MeshId"][1], props["Transparency"][1], props["DoubleSided"][1], "\n")
      accessory = parent["_class"] == "Accessory"
      if accessory: name = parent["_name"]
      print("LOADING:", name)

      pos = CFrame2mat(getCFrame(props))
      multiplyMM(pos, 0, root_pos, 0, pos, 0)

      mesh = cdnLoader(checkString(props["MeshId"]))
      SA = getSurfaceAppearance(node)
      if SA:
        SA_props = SA["_props"]
        color = checkColor3(SA_props["Color"])
        colorMap = cdnLoader(checkString(SA_props["ColorMap"]))
        metalnessMap = cdnLoader(checkString(SA_props["MetalnessMap"]))
        normalMap = cdnLoader(checkString(SA_props["NormalMap"]))
        roughnessMap = cdnLoader(checkString(SA_props["RoughnessMap"]))
        PBR_textures = color, colorMap, (metalnessMap, normalMap, roughnessMap)
        if mesh:
          model = meshReader(mesh, True)
          if model:
            VBOdata, IBOdata = model
            if is_character_part: characterPBR_models.append((node, VBOdata, IBOdata, PBR_textures, accessory))
            else: PBR_models.append((VBOdata, IBOdata, pos, PBR_textures, accessory))
      else:
        r, g, b = checkColor3uint8(props["Color3uint8"])
        texture = cdnLoader(checkString(props["TextureID"]))
        texture = ((texture, (1, 1, 1, 1)),) if texture else ()
        tex = (r, g, b, 1), texture
        if mesh:
          model = meshReader(mesh, False)
          if model:
            VBOdata, IBOdata = model
            if is_character_part: characterModels.append((node, VBOdata, IBOdata, tex, accessory))
            else: models.append((VBOdata, IBOdata, pos, tex, accessory))
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
    for child in childs: recurs(child, root_pos)

  models = []
  PBR_models = []
  shirts = []
  pantss = []

  motorTree = None
  used_in_tree = set()
  characterModels = []
  characterPBR_models = []

  recurs(root, None)
  character = motorTree, characterModels, characterPBR_models

  return models, PBR_models, shirts, pantss, character



def modelLoader(root, name, textureChain):
  global dbgTextures

  cache = STORAGE("rbxm_modelHandler_cache")
  try: models, PBR_models, shirts, pantss, character = cache[name]
  except KeyError:
    models, PBR_models, shirts, pantss, character = record = modelHandler(root)
    cache[name] = record

  # pants = newTexture2(pantss[0][1])
  # print("🐾pants texture:", pants)
  bodyTexture = textureChain.use((1, 1), (0.9, 0.95, 1, 1), ())

  models2 = []
  PBR_models2 = []

  for VBOdata, IBOdata, pos, tex, accessory in models:
    if not accessory: texture = bodyTexture
    else: # tex всегда есть
      color, texArr = tex
      texArr = ((newTexture2(tex), color) for tex, color in texArr)
      if texArr: size = texture2size[texArr[0][0]]
      else: size = 1, 1
      print("🤗 SIZE:", size, color, texArr)
      texture = textureChain.use(size, color, texArr)

    model = Model(VBOdata, IBOdata)
    if texture: model = TexturedModel(model, texture)
    model = MatrixModel(model, pos)
    models2.append(model)

  for VBOdata, IBOdata, pos, PBR_textures, accessory in PBR_models:
    (r, g, b), colorMap, otherTex = PBR_textures
    if colorMap is None:
      colorMap = textureChain.use((1, 1), (r, g, b, 1), ())
    else:
      colorMap = newTexture2(colorMap)
      size = texture2size[colorMap]
      colorMap = textureChain.use(size, (0, 0, 0, 1), ((colorMap, (r, g, b, 1)),))
    metalnessMap, normalMap, roughnessMap = (None if tex is None else newTexture2(tex) for tex in otherTex)

    model = Model(VBOdata, IBOdata)
    model = PBR_Model(model, colorMap, metalnessMap, normalMap, roughnessMap)
    model = MatrixModel(model, pos)
    PBR_models2.append(model)

  union = UnionModel(models2)
  PBR_model = UnionModel(PBR_models2)

  charModel = CharacterModel(character, textureChain)

  return union, (PBR_model,), charModel
