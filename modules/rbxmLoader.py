
def getCFrame(node):
  try: pivot = node["WorldPivotData"]
  except KeyError:
    try: pivot = node["CFrame"]
    except KeyError: return
  type, value = pivot
  if type == 0x10: return value # CFrame
  if type == 0x1e: # OptionalCoordinateFrame
    useful, cframe = value
    if useful: return cframe

def checkString(data):
  type, value = data
  if type != 0x01: exit("Это не String: %s" % data)
  return value
def checkColor3(data):
  type, value = data
  if type != 0x0c: exit("Это не Color3: %s" % data)
  return value

def modelLoader(root):
  def recurs(node, root_pos):
    id, parent, childs, className, name = node["_id"], node["_parent"], node["_childs"], node["_class"], checkString(node["Name"])
    data = {k: v for k, v in node.items() if k not in {"_id", "_parent", "_childs", "_class", "Name"}}
    if root_pos is None:
      pos = getCFrame(node)
      if pos is not None:
        mat = CFrame2mat(pos)
        root_pos = FLOAT.new_array(16)
        invertM(root_pos, 0, mat, 0)
    if className == "MeshPart":
      # print("%s %s %s\n" % (id, name, data))
      #print(node["size"][1], node["VertexCount"][1], node["TextureID"][1], node["MeshId"][1], node["Transparency"][1], node["DoubleSided"][1], "\n")
      accessory = parent["_class"] == "Accessory"
      if accessory: name = checkString(parent["Name"])
      print("LOADING:", name)
      pos = CFrame2mat(getCFrame(node))
      multiplyMM(pos, 0, root_pos, 0, pos, 0)
      mesh = cdnLoader(checkString(node["MeshId"]))
      tex = cdnLoader(checkString(node["TextureID"]))
      if mesh:
        model = meshReader(mesh)
        if model:
          VBOdata, IBOdata = model
          models.append((VBOdata, IBOdata, tex, pos, accessory))
    elif className == "BodyColors":
      bodyColors = {
        "head": checkColor3(data["HeadColor3"]),
        "leftArm": checkColor3(data["LeftArmColor3"]),
        "leftLeg": checkColor3(data["LeftLegColor3"]),
        "rightArm": checkColor3(data["RightArmColor3"]),
        "rightLeg": checkColor3(data["RightLegColor3"]),
        "torso": checkColor3(data["TorsoColor3"]),
      }
      print("🏵️:", bodyColors) # на деле ненужный параметр, т.к. у всех частей тела (а их больше, чем здесь 6 штук) цвета прописаны отдельно
    elif className == "Shirt":
      print("SHIRT:", name)
      color = checkColor3(data["Color3"])
      asset = cdnLoader(checkString(data["ShirtTemplate"]))
      shirts.append((color, asset))
    elif className == "Pants":
      print("PANTS:", name)
      color = checkColor3(data["Color3"])
      asset = cdnLoader(checkString(data["PantsTemplate"]))
      pantss.append((color, asset))
    for child in childs: recurs(child, root_pos)
  models = []
  shirts = []
  pantss = []
  recurs(root, None)

  pants = newTexture2(pantss[0][1])
  print("🐾pants texture:", pants)

  models2 = []
  for VBOdata, IBOdata, tex, pos, accessory in models:
    model = Model(VBOdata, IBOdata)
    model = MatrixModel(model, pos)
    model = TranslateModel(model, (3, 0, 0))
    if not accessory: texture = pants
    else: texture = newTexture2(tex) if tex else None
    if texture: model = TexturedModel(model, texture)
    models2.append(model)
  return models2
