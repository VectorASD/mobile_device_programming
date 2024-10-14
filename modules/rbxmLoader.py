
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
def checkColor3uint8(prop):
  type, value = prop
  if type != 0x1a: exit("Это не Color3uint8: %s" % prop)
  return value



def modelHandler(root):
  def recurs(node, root_pos):
    id, parent, childs, className, name = node["_id"], node["_parent"], node["_childs"], node["_class"], node["_name"]
    props = node["_props"]
    if root_pos is None:
      pos = getCFrame(props)
      if pos is not None:
        mat = CFrame2mat(pos)
        root_pos = FLOAT.new_array(16)
        invertM(root_pos, 0, mat, 0)
    if className == "MeshPart":
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
        print("👣", SA_props)
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
            PBR_models.append((VBOdata, IBOdata, pos, PBR_textures, accessory))
      else:
        # r, g, b = checkColor3uint8(props["Color3uint8"])
        r = g = b = 255
        tex = (0, 0, 0, 1), ((cdnLoader(checkString(props["TextureID"])), (r/255, g/255, b/255, 1)),)
        if mesh:
          model = meshReader(mesh, False)
          if model:
            VBOdata, IBOdata = model
            models.append((VBOdata, IBOdata, pos, tex, accessory))
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
  recurs(root, None)

  return models, PBR_models, shirts, pantss



dbgTextures = 0, 0

def modelLoader(root, name, textureChain):
  global dbgTextures

  cache = STORAGE("rbxm_modelHandler_cache")
  try: models, PBR_models, shirts, pantss = cache[name]
  except KeyError:
    models, PBR_models, shirts, pantss = record = modelHandler(root)
    cache[name] = record

  # pants = newTexture2(pantss[0][1])
  # print("🐾pants texture:", pants)
  bodyTexture = textureChain.use((1, 1), (0.9, 0.95, 1, 1), ())

  models2 = []
  for VBOdata, IBOdata, pos, tex, accessory in models:
    model = Model(VBOdata, IBOdata)
    model = MatrixModel(model, pos)
    #model = RotateModel(model, (45, 0, 0))
    #model = TranslateModel(model, (5, 0, 0))
    if not accessory: texture = bodyTexture
    elif tex:
      color, texArr = tex
      texArr = ((newTexture2(tex), color) for tex, color in texArr)
      if texArr: size = texture2size[texArr[0][0]]
      else: size = 1, 1
      print("🤗 SIZE:", size, color, texArr)
      texture = textureChain.use(size, color, texArr)
      if texArr: dbgTextures = texArr[0][0], texture
    else: texture = None
    if texture: model = TexturedModel(model, texture)
    models2.append(model)

  PBR_models2 = []
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
    #model = RotateModel(model, (45, 0, 0))
    #model = TranslateModel(model, (5, 0, 0))
    PBR_models2.append(model)

  union = UnionModel(models2)
  PBR_model = UnionModel(PBR_models2)

  return union, (PBR_model,)
