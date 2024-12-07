import myGL



class Model:
  type = "Model"
  def __init__(self, VBOdata, IBOdata = None, shaderProgram = None, printer = True):
    self.colorama_func = None
    if IBOdata is None and len(VBOdata) == 5:
      self.data = VBOdata
      self.matrix = None
      return
    if shaderProgram is None: exit("shader program not defined :/")

    buffers = INT.new_array(2)
    glGenBuffers(2, buffers, 0)
    VBO, IBO = buffers

    sizes = len(VBOdata), len(IBOdata)
    # 3d-координаты, раскраска вершин и 2d-UV вершин
    VBOdata = FloatBuffer(VBOdata)
    # сами полигоны = сетка
    IBOdata = IntBuffer(IBOdata)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, VBOdata.capacity() * 4, VBOdata.fb, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, IBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, IBOdata.capacity() * 4, IBOdata.fb, GL_STATIC_DRAW)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    if printer: print2("✅ OK buffers:", VBO, IBO, "(%s, %s words)" % sizes)
    self.data = VBO, IBO, IBOdata.capacity(), shaderProgram, shaderProgram.renderer
    self.matrix = None

  def recalc(self, mat):
    self.matrix = mat

  def draw(self):
    VBO, IBO, indexes, shaderProgram, renderer = self.data

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, IBO)

    if renderer.colorDimension:
      colorama_func = self.colorama_func
      if colorama_func:
        colorama_func()
        shaderProgram = renderer.colorama
      else: return
    else: shaderProgram.func()

    mat = self.matrix
    if mat is not None:
      location = shaderProgram.location
      if type(location) is tuple:
        location, location2 = location
        inv = FLOAT.new_array(16)
        invertM(inv, 0, mat, 0)
        glUniformMatrix4fv(location2, 1, True, inv, 0)
      glUniformMatrix4fv(location, 1, False, mat, 0)

    glDrawElements(GL_TRIANGLES, indexes, GL_UNSIGNED_INT, 0)
    #glBindBuffer(GL_ARRAY_BUFFER, 0)
    #glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

  def delete(self):
    VBO, IBO, indexes = self.data
    buffers = (VBO, IBO)._a_int
    glDeleteBuffers(2, buffers, 0)
    print2("♻️ buffers:", buffers[:])
  
  def clone(self):
    return Model(self.data)

  def setColor(self, color):
    renderer = self.data[4]
    func = renderer.colorama.func
    self.colorama_func = lambda: func(color)



def buildModel(faces):
  VBOdata = []
  VBOdict = {}
  IBOdata = []
  VBOextend = VBOdata.extend
  IBOextend = IBOdata.extend
  for xyz, xyz2, xyz3 in faces:
    try: index = VBOdict[xyz]
    except KeyError:
      index = VBOdict[xyz] = len(VBOdict)
      VBOextend(xyz)
    try: index2 = VBOdict[xyz2]
    except KeyError:
      index2 = VBOdict[xyz2] = len(VBOdict)
      VBOextend(xyz2)
    try: index3 = VBOdict[xyz3]
    except KeyError:
      index3 = VBOdict[xyz3] = len(VBOdict)
      VBOextend(xyz3)
    IBOextend((index, index2, index3))
  return VBOdata, IBOdata



class TranslateModel:
  type = "TranslateModel"
  def __init__(self, model, translate):
    self.model = model
    self.translate = translate
    self.draw = model.draw
    self.delete = model.delete
    self.setColor = model.setColor

  def recalc(self, mat):
    self.mat = mat
    self.update()
  def update(self):
    tMat = FLOAT.new_array(16)
    x, y, z = self.translate
    translateM2(tMat, 0, self.mat, 0, x, y, z)
    self.model.recalc(tMat)
  def update2(self, translate):
    self.translate = translate
    try: self.update()
    except AttributeError: pass # если update2 вызван до recalc, то self.mat просто нет

  def clone(self):
    return TranslateModel(self.model.clone(), self.model)



class ScaleModel:
  type = "ScaleModel"
  def __init__(self, model, scale):
    self.model = model
    self.scale = scale
    self.draw = model.draw
    self.delete = model.delete
    self.setColor = model.setColor

  def recalc(self, mat):
    self.mat = mat
    self.update()
  def update(self):
    sMat = FLOAT.new_array(16)
    x, y, z = self.scale
    scaleM2(sMat, 0, self.mat, 0, x, y, z)
    self.model.recalc(sMat)
  def update2(self, scale):
    self.scale = scale
    try: self.update()
    except AttributeError: pass # если update2 вызван до recalc, то self.mat просто нет

  def clone(self):
    return ScaleModel(self.model.clone(), self.scale)



class RotateModel:
  type = "RotateModel"
  def __init__(self, model, YPR):
    self.model = model
    self.YPR = YPR
    self.draw = model.draw
    self.delete = model.delete
    self.setColor = model.setColor

  def recalc(self, mat):
    self.mat = mat
    self.update()

  def update(self):
    yaw, pitch, roll = self.YPR
    q = Quaternion.fromYPR(yaw, pitch, roll)
    q2 = q.conjugated()
    sMat = q2.toMatrix()
    multiplyMM(sMat, 0, self.mat, 0, sMat, 0)
    self.model.recalc(sMat)
  def update2(self, YPR):
    self.YPR = YPR
    try: self.update()
    except AttributeError: pass # если update2 вызван до recalc, то self.mat просто нет

  def clone(self):
    clone = RotateModel(self.model.clone(), self.YPR)
    clone.location = self.location
    clone.mat = self.mat
    return clone



class MatrixModel:
  type = "MatrixModel"
  def __init__(self, model, matrix, info):
    self.model = model
    self.matrix = matrix
    self.info = info
    self.draw = model.draw
    self.delete = model.delete
    self.setColor = model.setColor

  def recalc(self, mat):
    sMat = FLOAT.new_array(16)
    multiplyMM(sMat, 0, mat, 0, self.matrix, 0)
    self.model.recalc(sMat)

  def clone(self):
    return MatrixModel(self.model.clone(), self.matrix)



class UnionModel:
  type = "UnionModel"
  def __init__(self, models):
    self.models = models

  def recalc(self, mat):
    for model in self.models: model.recalc(mat)

  def draw(self):
    for model in self.models: model.draw()

  def delete(self):
    for model in self.models: model.delete()
    self.models = ()

  def clone(self):
    models = self.models
    models = tuple(models.copy() if type(models) is list else models)
    return UnionModel(models)

  def setColor(self, color):
    for model in self.models: model.setColor(color)



class TexturedModel:
  type = "TexturedModel"
  def __init__(self, model, textureID):
    self.model = model
    self.textureID = textureID
    self.delete = model.delete
    self.recalc = model.recalc
    self.setColor = model.setColor

  def draw(self):
    texture = self.textureID
    if texture.isdef(): texture = texture()
    glBindTexture(GL_TEXTURE_2D, texture)
    self.model.draw()

  def clone(self):
    return TexturedModel(self.model.clone(), self.textureID)



class NoCullFaceModel:
  type = "NoCullFaceModel"
  def __init__(self, model):
    self.model = model
    self.delete = model.delete
    self.recalc = model.recalc
    self.setColor = model.setColor

  def draw(self):
    glDisable(GL_CULL_FACE)
    self.model.draw()
    glEnable(GL_CULL_FACE)

  def clone(self):
    return NoCullFaceModel(self.model.clone())



dbgTextures = 0, 0

class CharacterModel:
  type = "CharacterModel"
  def __init__(self, character, renderer):
    global dbgTextures

    self.motorTree, models, PBR_models = character
    alternativeMode = self.motorTree is None
    VIEW = renderer.view

    # сразу 3 шейдерные программы в одном месте 🫢
    program = renderer.noPBR # renderer.program
    textureChain = renderer.textureChain
    PBR = renderer.pbr
    #bodyTexture = await(VIEW, lambda: textureChain.use((1, 1), (1, 0.95, 0.9, 1)))
    self.models = models2 = []
    self.PBR_models = PBR_models2 = []
    model_cache = renderer.model_cache

    for node, pos, model_data, tex, isBody, info in models:
      VBOdata, IBOdata, model_name = model_data
      #if isBody: texture = bodyTexture
      #else: # tex всегда есть
      color, texArr = tex
      if not texArr and "decal" in info:
        texture, body, color2 = info["decal"]
        textureTmp = await(VIEW, lambda: newTexture2(texture))
        size = texture2size[textureTmp]
        texture = await(VIEW, lambda: textureChain.use(size, color, ((textureTmp, color2),), False))
        # print(";'-}", color, color2)
        dbgTextures = textureTmp, texture
        useDecal = True
      else:
        texArr = ((await(VIEW, lambda: newTexture2(tex)), color) for tex, color in texArr)
        size = texture2size[texArr[0][0]] if texArr else (1, 1)
        # print("🤗 SIZE%s:" % (" (body)" if isBody else ""), size, color, texArr)
        texture = await(VIEW, lambda: textureChain.use(size, color, texArr, False))
        if texArr: dbgTextures = texArr[0][0], texture
        useDecal = False

      try: model = model_cache[model_name].clone()
      except KeyError:
        model = await(VIEW, lambda: Model(VBOdata, IBOdata, program))
        model_cache[model_name] = model
      if texture: model = TexturedModel(model, texture)
      # model = PBR_Model(model, texture, None, None, None)
      # if useDecal: model = NoCullFaceModel(model)
      # print("💥🔥", pos[:])
      model = MatrixModel(model, pos, info)
      models2.append(model if alternativeMode else (node["_id"], model))

    def newTex(bin):
      texture = newTexture2(bin)
      glBindTexture(GL_TEXTURE_2D, texture)
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
      glGenerateMipmap(GL_TEXTURE_2D)
      return texture
    for node, pos, model_data, PBR_textures, isBody, info in PBR_models:
      VBOdata, IBOdata, model_name = model_data
      (r, g, b), colorMap, otherTex = PBR_textures
      if colorMap is None:
        colorMap = await(VIEW, lambda: textureChain.use((1, 1), (r, g, b, 1)))
      else:
        colorMap2 = await(VIEW, lambda: newTexture2(colorMap))
        size = texture2size[colorMap]
        colorMap = await(VIEW, lambda: textureChain.use(size, (0, 0, 0, 1), ((colorMap2, (r, g, b, 1)),), True))
      metalnessMap, normalMap, roughnessMap = (None if tex is None else await(VIEW, lambda: newTex(tex)) for tex in otherTex)

      try: model = model_cache[model_name].clone()
      except KeyError:
        model = await(VIEW, lambda: Model(VBOdata, IBOdata, PBR))
        model_cache[model_name] = model
      model = PBR_Model(model, colorMap, metalnessMap, normalMap, roughnessMap)
      model = MatrixModel(model, pos, info)
      PBR_models2.append(model if alternativeMode else (node["_id"], model))

    if alternativeMode: return

    self.saved_mat = None
    self.renderer = renderer
    self.position = 5, 0, 0
    self.setRotation(-90, 0, 0)

  def setPosition(self, x, y, z):
    self.position = x, y, z
    self.recalcChainPos()

  def setRotation(self, yaw, pitch, roll):
    self.YPR = yaw, pitch, roll
    self.rotation = Quaternion.fromYPR(yaw, pitch, roll).conjugated().toMatrix()
    self.recalcChainPos()

  def recalcChainPos(self):
    def recurs(node, mat):
      for C0, C1, id, childs in node:
        mat2 = FLOAT.new_array(16)
        multiplyMM(mat2, 0, mat, 0, C0, 0)
        multiplyMM(mat2, 0, mat2, 0, motor, 0)
        multiplyMM(mat2, 0, mat2, 0, C1, 0)
        result[id] = mat2
        recurs(childs, mat2)
    self.chainMats = result = {}
    mat = self.rotation
    mat[12:15] = self.position
    motor = CFrame2mat((0, 0, 0) + fromEulerAngles(0, 0, 0))
    recurs(self.motorTree, mat)
    # for k, v in result.items(): print(k, v[12:])
    self.recalc2()

  def recalc(self, mat):
    self.saved_mat = mat
    self.recalc2()

  def recalc2(self):
    saved_mat = self.saved_mat
    if saved_mat is None: return
    mats = self.chainMats

    for id, model in self.models:
      mat = mats[id]
      #print(id, mat[12:])
      model_mat = FLOAT.new_array(16)
      multiplyMM(model_mat, 0, saved_mat, 0, mat, 0)
      model.recalc(model_mat)

    self.PBR_models2 = arr = []
    append = arr.append
    for id, model in self.PBR_models:
      model.recalc(mats[id])
      append(model)

  def draw(self):
    for id, model in self.models: model.draw()
    self.renderer.pbr.draw(self.PBR_models2)
  
  def delete(self):
    for id, model in self.models: model.delete()
    # TODO



class WaitingModel:
  type = "WaitingModel"
  def __init__(self):
    self.saved_mat = None
    self.model = None
    self.draw = lambda: None
    self.needDelete = False
    self.saved_color = None
  def setModel(self, model):
    # print("SET MODEL:", model)
    self.model = model
    self.recalc2()

  def recalc(self, mat):
    self.saved_mat = mat
    self.recalc2()

  def recalc2(self):
    mat = self.saved_mat
    model = self.model
    if mat is None or model is None: return
    # print("GET MODEL:", model)
    model.recalc(mat)
    self.delete = model.delete
    if self.needDelete: model.delete()
    else:
      self.recalc = model.recalc
      self.draw = model.draw
      self.setColor = model.setColor
      color = self.saved_color
      if color is not None: self.setColor(color)

  def delete(self): # если удалили модель до того, как она загрузилась :/
    self.needDelete = True

  def setColor(self, color):
    self.saved_color = color



class Quaternion:
  def __init__(self, x, y, z, w):
    self.xyzw = x, y, z, w
  def fromYPR(yaw, pitch, roll):
    yaw = yaw * pi180 / 2
    pitch = pitch * pi180 / 2
    roll = roll * pi180 / 2
    sYaw, cYaw = sin(yaw), cos(yaw)
    sPitch, cPitch = sin(pitch), cos(pitch)
    sRoll, cRoll = sin(roll), cos(roll)

    x = cYaw * sPitch * cRoll - sYaw * cPitch * sRoll
    y = cYaw * sPitch * sRoll + sYaw * cPitch * cRoll
    z = cYaw * cPitch * sRoll - sYaw * sPitch * cRoll
    w = cYaw * cPitch * cRoll + sYaw * sPitch * sRoll
    return Quaternion(x, y, z, w)

  def inverted(self):
    x, y, z, w = self.xyzw
    norm = x ** 2 + y ** 2 + z ** 2 + w ** 2
    if abs(norm) < 0.000000000001: return Quaternion(0, 0, 0, 0)
    return Quaternion(-x / norm, -y / norm, -z / norm, w / norm)
  def conjugated(self): # (сопряжённый)
    x, y, z, w = self.xyzw
    return Quaternion(-x, -y, -z, w)
  def toMatrix(self):
    x, y, z, w = self.xyzw
    xx, yy, zz = 2 * x * x, 2 * y * y, 2 * z * z
    xy, xz, yz = 2 * x * y, 2 * x * z, 2 * y * z
    xw, yw, zw = 2 * x * w, 2 * y * w, 2 * z * w
    return (
      1 - yy - zz, xy + zw,     xz - yw,     0,
      xy - zw,     1 - xx - zz, yz + xw,     0,
      xz + yw,     yz - xw,     1 - xx - yy, 0,
      0, 0, 0, 1,
    )._a_float
  def multiply(self, R):
    Ax, Ay, Az, Aw = self.xyzw
    Bx, By, Bz, Bw = R.xyzw
    yy = (Aw - Ay) * (Bw + Bz)
    zz = (Aw + Ay) * (Bw - Bz)
    ww = (Az + Ax) * (Bx + By)
    xx = ww + yy + zz
    qq = 0.5 * (xx + (Az - Ax) * (Bx - By))

    w = qq - ww + (Az - Ay) * (By - Bz)
    x = qq - xx + (Ax + Aw) * (Bx + Bw)
    y = qq - yy + (Aw - Ax) * (By + Bz)
    z = qq - zz + (Az + Ay) * (Bw - Bx)
    return Quaternion(x, y, z, w)
  def rotatedVector(self, x, y, z):
    x, y, z, w = self.multiply(Quaternion(x, y, z, 0)).multiply(self.conjugated()).xyzw
    return x, y, z



class d2textureProgram():
  def __init__(self, texture, size, renderer):
    self.program = _, attribs, uniforms = checkProgram(newProgram("""
attribute vec2 vPosition;
attribute vec2 vUV;
attribute float vType;
attribute float vUp;

uniform float uAspect;
uniform int uEvent;

varying vec2 vaUV;
varying float vaActive;

bool getBit(int num, int b) {
  int bit = 0;
  int min = 128;
  for (int i = 7; i >= b; i--) {
    if (num >= min) {
      num -= min;
      if (i == b) return true;
    }
    min /= 2;
  }
  return false;
}

void main() {
  gl_Position = vec4(vPosition.x,
    vUp > 0.5 ? vPosition.y * uAspect + (1. - uAspect)
    : vPosition.y * uAspect - (1. - uAspect),
  0, 1);
  vaUV = vUV;

  int T = int(vType);
  if (T < 1 || T > 3) vaActive = 1.;
  else vaActive = getBit(uEvent, T - 1) ? 0.5 : 1.;
}
""", """
precision mediump float;

varying vec2 vaUV;
varying float vaActive;

uniform sampler2D uTexture;

void main() {
	float X = vaActive;
  vec4 clr = texture2D(uTexture, vaUV);
  gl_FragColor = vec4(clr.rgb * X, clr.a);
}
""", ('vPosition', 'vUV', 'vType', 'vUp'), ('uTexture', 'uAspect', 'uEvent')))
    vPosition = attribs["vPosition"]
    vUV       = attribs["vUV"]
    vType     = attribs["vType"]
    vUp       = attribs["vUp"]
    def func():
      glVertexAttribPointer(vPosition, 2, GL_FLOAT, False, 6 * 4, 0)
      glVertexAttribPointer(vUV,       2, GL_FLOAT, False, 6 * 4, 2 * 4)
      glVertexAttribPointer(vType,     1, GL_FLOAT, False, 6 * 4, 4 * 4)
      glVertexAttribPointer(vUp,       1, GL_FLOAT, False, 6 * 4, 5 * 4)
    self.func = func
    self.location = None

    self.uTexture = uniforms["uTexture"]
    self.uAspect = uniforms["uAspect"]
    self.uEvent = uniforms["uEvent"]
    self.models = []
    self.modelPositions = []
    self.aspect = 1
    self.texture = texture
    self.renderer = renderer
    self.size        = W, H = size
    self.textureSize = tW, tH = texture2size[texture]
    self.tileSize    = (tW + W - 1) // W, (tH + H - 1) // H
    self.printer = True
    self.up = 0
    self.dir = 0

  def setUp(self, up): self.up = up
  def setDirection(self, dir): self.dir = dir

  def createModel(self, id, posX, posY, L = 10, t = 0, invertX = False, invertY = False):
    W, H = self.size
    L /= 2
    L1 = L - 1
    pLx, pRx, pLy, pRy = (posX - L) / L, (posX - L1) / L, (posY - L) / -L, (posY - L1) / -L
    y, x = divmod(id, W)
    Lx, Rx, Ly, Ry = x / W, (x + 1) / W, y / H, (y + 1) / H
    if invertX: Lx, Rx = Rx, Lx
    if invertY: Ly, Ry = Ry, Ly
    dir = self.dir
    return Model((
      pLx, pLy, Lx, Ly, t, dir,
      pRx, pLy, Rx, Ly, t, dir,
      pRx, pRy, Rx, Ry, t, dir,
      pLx, pRy, Lx, Ry, t, dir,
    ), (
      0, 1, 2, 0, 2, 3,
    ), self, self.printer)
  def replace(self, index, id, posX, posY, L = 10, t = 0, invertX = False, invertY = False):
    model = self.createModel(id, posX, posY, L, t, invertX, invertY)
    upXY = self.up
    if type(upXY) in (int, float): upX = upY = upXY
    else: upX, upY = upXY
    self.models[index] = model
    self.modelPositions[index] = (posX - upX) / L, (posX + 1 + upX) / L, (posY - upY) / L, (posY + 1 + upY) / L, t, self.dir
  def add(self, id, posX, posY, L = 10, t = 0, invertX = False, invertY = False):
    index = len(self.models)
    self.models.append(None)
    self.modelPositions.append(None)
    self.replace(index, id, posX, posY, L, t, invertX, invertY)
    return index

  def draw(self, aspect, eventN, customModels = None):
    self.aspect = aspect

    glDisable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)
    enableProgram(self.program)
    glUniform1f(self.uAspect, aspect)
    glUniform1i(self.uEvent, eventN)
    glUniform1i(self.uTexture, 0)
    glBindTexture(GL_TEXTURE_2D, self.texture)

    models = customModels if customModels is not None else self.models
    for model in models: model.draw()

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)

  def checkPosition(self, x, y):
    # x и y от 0 до 1
    aspect = self.aspect
    yDown = (y - (1 - aspect)) / aspect
    yUp = y / aspect
    ys = yDown, yUp
    result = -1
    for x1, x2, y1, y2, t, dir in self.modelPositions:
      y = ys[dir]
      if x1 <= x and x <= x2 and y1 <= y and y <= y2: result = t
    return result



class SkyBox:
  program = None
  model = None
  def __init__(self, width, height, textureGetter, renderer):
    arr = INT.new_array(1)
    glGenTextures(1, arr, 0)
    self.textureId = textureId = arr[0]
    texture2size[textureId] = width, height
    glBindTexture(GL_TEXTURE_CUBE_MAP, textureId)
    #checkGLError() ok

    for i in range(6):
      buffer = textureGetter(i)
      glTexImage2D(GL_TEXTURE_CUBE_MAP_TARGETS[i], 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, buffer)
      buffer._m_clear()
      #checkGLError() ok

    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    #checkGLError() ok

    glBindTexture(GL_TEXTURE_CUBE_MAP, 0)
    print2("✅ OK cube map texture:", textureId)
    self.renderer = renderer
    self.genProgram()
    self.genModel()

  def genProgram(self):
    if SkyBox.program is None:
      SkyBox.program = checkProgram(newProgram("""
attribute vec3 vPosition;
uniform mat4 uVPMatrix;
varying vec3 TexCoords;

void main() {
  TexCoords = vPosition;
  vec4 pos = uVPMatrix * vec4(vPosition, 1.);
  gl_Position = pos.xyww;
}
""", """
precision mediump float;
varying vec3 TexCoords;
uniform samplerCube uSkybox;

void main() {             
    gl_FragColor = textureCube(uSkybox, TexCoords);
}
""", ('vPosition', ), ('uVPMatrix', 'uSkybox')))
    _, attribs, uniforms = SkyBox.program
    vPosition = attribs["vPosition"]
    self.uVPMatrix = uniforms["uVPMatrix"]
    self.uSkybox = uniforms["uSkybox"]
    def func():
      glVertexAttribPointer(vPosition, 3, GL_FLOAT, False, 0, 0)
    self.func = func
    self.location = None

  def genModel(self):
    if SkyBox.model is not None: return
    SkyBox.model = Model((
      -1, -1, -1, # 0
       1, -1, -1, # 1
       1, -1,  1, # 2
      -1, -1,  1, # 3
      -1,  1, -1, # 4
       1,  1, -1, # 5
       1,  1,  1, # 6
      -1,  1,  1, # 7
    ), (
       0,  2,  1,  0,  3,  2, # дно куба
       0,  1,  4,  1,  5,  4, # фронт
       1,  2,  5,  2,  6,  5, # правый бок
       2,  3,  7,  2,  7,  6, # тыл
       3,  0,  7,  0,  4,  7, # левый бок
       4,  5,  7,  5,  6,  7, # верх куба
    ), self)

  def draw(self):
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    enableProgram(SkyBox.program)
    glUniformMatrix4fv(self.uVPMatrix, 1, False, self.renderer.VPmatrix, 0)
    glUniform1i(self.uSkybox, 0)
    glBindTexture(GL_TEXTURE_CUBE_MAP, self.textureId)

    SkyBox.model.draw()

    glBindTexture(GL_TEXTURE_CUBE_MAP, 0)
    glDepthFunc(GL_LESS)

  def restart():
    SkyBox.model = None
    SkyBox.program = None



def skyBoxLoader(gridProgram, indexes, flipY = False, dbg = False):
  oldViewportParams = INT.new_array(4)
  glGetIntegerv(GL_VIEWPORT, oldViewportParams, 0)

  W, H = gridProgram.tileSize
  # print("SKYBOX TILE SIZE:", W, H) всё верно высчитывает внутри gridProgram
  fbo = newFrameBuffer(W, H, False)
  glBindFramebuffer(GL_FRAMEBUFFER, fbo[0])
  glViewport(0, 0, W, H)
  #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  #glClear(GL_DEPTH_BUFFER_BIT) а смысл, если в FBO нет рендер-буфера глубины

  def textureCutter(n):
    id = indexes[n]
    # Текстуры Skybox-сторон капризничают -> им нужны сразу обе инверсии текстурных координат
    # Но это неактуально для +Y и -Y
    invert = flipY or n not in (2, 3) # +Y, -Y
    model = gridProgram.createModel(id, 0, 0, 1, 0, invert, invert)
    gridProgram.draw(1, 0, (model,))
    model.delete()
    buffer = MyBuffer.allocateDirect(W * H * 4)
    buffer._m_order(MyBuffer.nativeOrder)
    glReadPixels(0, 0, W, H, GL_RGBA, GL_UNSIGNED_BYTE, buffer)
    if dbg:
      buffer = buffer._m_asIntBuffer()
      #assert buffer._m_remaining() == 1024
      arr = INT.new_array(buffer._m_remaining())
      buffer._m_get(arr)
      print("👍", n, arr[:])
    return buffer

  skybox = SkyBox(W, H, textureCutter, gridProgram.renderer)

  glBindFramebuffer(GL_FRAMEBUFFER, 0)
  deleteFrameBuffer(fbo)
  x, y, w, h = oldViewportParams
  glViewport(x, y, w, h)
  return skybox

glDepthFunc = GLES20._mw_glDepthFunc(int) # func
GL_LEQUAL = GLES20._f_GL_LEQUAL
GL_LESS = GLES20._f_GL_LESS



class TextureChain:
  def __init__(self, renderer):
    self.renderer = renderer
    self.genProgram()
    self.genModel()
    self.FBO = None

  def genProgram(self):
    self.program = _, attribs, uniforms = checkProgram(newProgram("""
attribute vec2 vPosition;
attribute vec2 vUV;
varying vec2 vaUV;

void main() {
  gl_Position = vec4(vPosition, 0., 1.);
  vaUV = vUV;
}
""", """
precision mediump float;
varying vec2 vaUV;
uniform sampler2D uTexture;
uniform vec4 uTextureColor;

void main() {
  vec4 color = texture2D(uTexture, vaUV) * uTextureColor;
  color.a = pow(color.a, 1. / 5.5); // усиленная гамма-коррекция альфы (5.5 вместо 2.2)
  gl_FragColor = color;
}
""", ('vPosition', 'vUV'), ('uTexture', 'uTextureColor')))
    vPosition = attribs["vPosition"]
    vUV = attribs["vUV"]
    self.uTexture = uniforms["uTexture"]
    self.uTextureColor = uniforms["uTextureColor"]
    def func():
      glVertexAttribPointer(vPosition, 2, GL_FLOAT, False, 4 * 4, 0)
      glVertexAttribPointer(vUV,       2, GL_FLOAT, False, 4 * 4, 2 * 4)
    self.func = func
    self.location = None

  def genModel(self):
    self.model = Model((
      -1, -1, 0, 0,
      -1, 1, 0, 1,
      1, -1, 1, 0,
      1, 1, 1, 1,
    ), (0, 1, 2, 1, 2, 3), self)

  def use(self, size, baseColor, textures = (), removeSources = False):
    W, H = size
    fbo, texture, _ = newFrameBuffer(W, H, False, self.FBO, GL_LINEAR)
    self.FBO = fbo

    oldViewportParams = INT.new_array(4)
    glGetIntegerv(GL_VIEWPORT, oldViewportParams, 0)

    glBindFramebuffer(GL_FRAMEBUFFER, fbo)
    glViewport(0, 0, W, H)
    glScissor(0, 0, W, H)
    r, g, b, a = baseColor
    glClearColor(r, g, b, a)
    glEnable(GL_SCISSOR_TEST)
    glClear(GL_COLOR_BUFFER_BIT)
    glDisable(GL_SCISSOR_TEST)
    glDisable(GL_CULL_FACE)
    glDisable(GL_DEPTH_TEST)

    enableProgram(self.program)
    glUniform1i(self.uTexture, 0)
    #glUniform1i(self.uUseGamma, int(gamma))
    draw = self.model.draw
    for texture2, textureColor in textures:
      r, g, b, a = textureColor
      glUniform4f(self.uTextureColor, r, g, b, a)
      glBindTexture(GL_TEXTURE_2D, texture2)
      draw()
      if removeSources: removeTexture(texture2)

    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    x, y, w, h = oldViewportParams
    glViewport(x, y, w, h)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)

    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    # GL_LINEAR_MIPMAP_LINEAR
    # GL_NEAREST_MIPMAP_NEAREST
    glGenerateMipmap(GL_TEXTURE_2D)

    return texture

  def postprocessing(self):
    enableProgram(self.program)
    glUniform1i(self.uTexture, 0)
    glUniform4f(self.uTextureColor, 1, 1, 1, 1)

    glBindTexture(GL_TEXTURE_2D, self.renderer.FBO[1])
    glDisable(GL_CULL_FACE)
    glDisable(GL_DEPTH_TEST)
    self.model.draw()
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)



class PBR:
  def __init__(self, renderer):
    self.genProgram()
    self.renderer = renderer

  def genProgram(self):
    self.program = program, attribs, uniforms = checkProgram(newProgram("""
attribute vec3 vPosition;
attribute vec3 vNormal;
attribute vec2 vUV;
attribute vec4 vTangent;

uniform mat4 uVPMatrix;
uniform mat4 uModelM;
uniform mat4 uInvModelM;
uniform vec3 uCamPos;
uniform vec3 uLightPos;

varying vec3 vaPos;
varying vec2 vaUV;
varying vec3 vaNormal;
varying vec3 vaTangentLightPos;
varying vec3 vaTangentViewPos;
varying vec3 vaTangentFragPos;

mat3 transpose(mat3 mat) {
  return mat3(
    vec3(mat[0].x, mat[1].x, mat[2].x),
    vec3(mat[0].y, mat[1].y, mat[2].y),
    vec3(mat[0].z, mat[1].z, mat[2].z));
}

float det(mat2 matrix) {
  return matrix[0].x * matrix[1].y - matrix[0].y * matrix[1].x;
}

mat3 inverse(mat3 matrix) {
  vec3 row0 = matrix[0];
  vec3 row1 = matrix[1];
  vec3 row2 = matrix[2];

  vec3 minors0 = vec3(
    det(mat2(row1.y, row1.z, row2.y, row2.z)),
    det(mat2(row1.z, row1.x, row2.z, row2.x)),
    det(mat2(row1.x, row1.y, row2.x, row2.y))
  );
  vec3 minors1 = vec3(
    det(mat2(row2.y, row2.z, row0.y, row0.z)),
    det(mat2(row2.z, row2.x, row0.z, row0.x)),
    det(mat2(row2.x, row2.y, row0.x, row0.y))
  );
  vec3 minors2 = vec3(
    det(mat2(row0.y, row0.z, row1.y, row1.z)),
    det(mat2(row0.z, row0.x, row1.z, row1.x)),
    det(mat2(row0.x, row0.y, row1.x, row1.y))
  );

  mat3 adj = transpose(mat3(minors0, minors1, minors2));

  return (1. / dot(row0, minors0)) * adj;
}

void main() {
  vec3 fragPos = vec3(uModelM * vec4(vPosition, 1.0));
  vaPos = fragPos;
  vaUV = vUV;

  // mat3 normalMatrix = transpose(inverse(mat3(uModelM)));
  mat3 normalMatrix = mat3(uInvModelM);
  vec3 T = normalize(normalMatrix * vTangent.xyz);
  vec3 N = normalize(normalMatrix * vNormal);
  T = normalize(T - dot(T, N) * N);
  vec3 B = cross(N, T);
  if (vTangent.w < 0.) B = -B;

  mat3 TBN = transpose(mat3(T, B, N));

  vaTangentLightPos = TBN * uLightPos;
  vaTangentViewPos = TBN * uCamPos;
  vaTangentFragPos = TBN * fragPos;
  vaNormal = N;

  gl_Position = uVPMatrix * uModelM * vec4(vPosition, 1);
}
""", """
precision mediump float;

varying vec3 vaPos;
varying vec2 vaUV;
varying vec3 vaNormal;
varying vec3 vaTangentLightPos;
varying vec3 vaTangentViewPos;
varying vec3 vaTangentFragPos;

uniform sampler2D uAlbedoMap;
uniform sampler2D uNormalMap;
uniform vec3 uCamPos;
uniform vec3 uLightPos;

uniform bool uUseNormalMap;

void main() {
  vec3 normal = texture2D(uNormalMap, vaUV).rgb;
  normal = uUseNormalMap ? normalize(normal * 2.0 - 1.0) : vaNormal;

  vec3 color = texture2D(uAlbedoMap, vaUV).rgb;
  // ambient
  vec3 ambient = 0.1 * color;
  // diffuse
  vec3 lightDir = normalize(vaTangentLightPos - vaTangentFragPos);
  float diff = max(dot(lightDir, normal), 0.0);
  vec3 diffuse = diff * color;
  // specular
  vec3 viewDir = normalize(vaTangentViewPos - vaTangentFragPos);
  vec3 reflectDir = reflect(-lightDir, normal);
  vec3 halfwayDir = normalize(lightDir + viewDir);
  float spec = pow(max(dot(normal, halfwayDir), 0.0), 32.0);

  vec3 specular = vec3(0.2) * spec;
  color = ambient + diffuse + specular;
  color = color / (color + vec3(1.)); // тональная компрессия
  color = pow(color, vec3(1. / 2.2)); // гамма-коррекция

  gl_FragColor = vec4(color, 1.);
}
""", ('vPosition', 'vNormal', 'vUV', 'vTangent'), ('uVPMatrix', 'uModelM', 'uInvModelM', 'uAlbedoMap', 'uNormalMap', 'uCamPos', 'uLightPos', 'uUseNormalMap')))
    self.uVPMatrix = uniforms["uVPMatrix"]
    uModelM = uniforms["uModelM"]
    uInvModelM = uniforms["uInvModelM"]
    self.uAlbedoMap = uniforms["uAlbedoMap"]
    self.uNormalMap = uniforms["uNormalMap"]
    self.uCamPos = uniforms["uCamPos"]
    self.uLightPos = uniforms["uLightPos"]
    self.uUseNormalMap = uniforms["uUseNormalMap"]
    def func():
      a = attribs # nonlocal to local
      glVertexAttribPointer(a["vPosition"], 3, GL_FLOAT, False, 12 * 4, 0)
      glVertexAttribPointer(a["vNormal"], 3, GL_FLOAT, False, 12 * 4, 3 * 4)
      glVertexAttribPointer(a["vUV"],       2, GL_FLOAT, False, 12 * 4, 6 * 4)
      glVertexAttribPointer(a["vTangent"], 4, GL_FLOAT, False, 12 * 4, 8 * 4)
    self.func = func
    self.location = uModelM, uInvModelM
    PBR_Model.PBR = self

  def draw(self, models):
    if not models: return
    renderer = self.renderer

    enableProgram(self.program)
    glUniform1i(self.uAlbedoMap, 0)
    glUniform1i(self.uNormalMap, 1)
    glUniform3f(self.uCamPos, renderer.camX, renderer.camY, renderer.camZ)
    glUniformMatrix4fv(self.uVPMatrix, 1, False, renderer.MVPmatrix, 0)
    glUniform3f(self.uLightPos, 0, 3, 0)

    try: models.draw()
    except AttributeError:
      for model in models: model.draw()

class PBR_Model:
  PBR = None

  def __init__(self, model, colorMap, metalnessMap, normalMap, roughnessMap):
    self.model = model
    if type(colorMap) is tuple and len(colorMap) == 4: self.textures = colorMap # clone
    else: self.textures = colorMap, metalnessMap, normalMap, roughnessMap
    self.recalc = model.recalc
    self.delete = model.delete
    self.setColor = model.setColor

  def draw(self):
    pbr = PBR_Model.PBR
    if pbr is None: exit("class 'PBR' not defined")

    colorMap, metalnessMap, normalMap, roughnessMap = self.textures

    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, colorMap)
    useNormalMap = normalMap is not None
    if useNormalMap:
      glActiveTexture(GL_TEXTURE1)
      glBindTexture(GL_TEXTURE_2D, normalMap)
    glUniform1i(pbr.uUseNormalMap, int(useNormalMap))
    self.model.draw()

    glActiveTexture(GL_TEXTURE0) # только в PBR используются текстурные блоки/слоты, так что возвращаем всё на свои места!

  def clone(self): return PBR_Model(self.model.clone(), self.textures)



class NoPBR:
  def __init__(self, renderer):
    self.program = _, attribs, uniforms = checkProgram(newProgram("""
attribute vec3 vPosition;
attribute vec3 vNormal;
attribute vec2 vUV;
// attribute vec4 vTangent;

uniform mat4 uVPMatrix;
uniform mat4 uModelM;
uniform mat4 uInvModelM;
uniform vec3 uCamPos;

varying vec2 vaUV;
varying vec3 vaNormal;
varying vec3 vaViewPos;
varying vec3 vaFragPos;

void main() {
  vec3 fragPos = vec3(uModelM * vec4(vPosition, 1.0));

  mat3 normalMatrix = mat3(uInvModelM);
  vec3 N = normalize(normalMatrix * vNormal);

  vaUV = vUV;
  vaNormal = N;
  vaViewPos = uCamPos;
  vaFragPos = fragPos;

  gl_Position = uVPMatrix * uModelM * vec4(vPosition, 1);
}
""", """
precision highp float;

varying vec2 vaUV;
varying vec3 vaNormal;
varying vec3 vaViewPos;
varying vec3 vaFragPos;

uniform sampler2D uTexture;
uniform vec3 uLightPos;
uniform bool uLightSource;

void main() {
  vec3 normal = vaNormal;
  // gl_FragColor = texture2D(uTexture, vaUV);
  vec4 rgba = texture2D(uTexture, vaUV);
  vec3 color = rgba.rgb;
  // ambient
  vec3 ambient = 0.03 * color;
  // diffuse
  vec3 lightDir = normalize(uLightPos - vaFragPos);
  if (uLightSource) lightDir = -lightDir;
  float diff = max(dot(lightDir, normal), 0.0);
  vec3 diffuse = diff * color;
  // specular
  vec3 viewDir = normalize(vaViewPos - vaFragPos);
  float spec = 0.0;
  // if (blinn) {
    vec3 halfwayDir = normalize(lightDir + viewDir);
    spec = pow(max(dot(normal, halfwayDir), 0.0), 32.0);
  /* } else {
    vec3 reflectDir = reflect(-lightDir, normal);
    spec = pow(max(dot(viewDir, reflectDir), 0.0), 8.0);
  } */
  vec3 specular = vec3(0.8) * spec;
  color = ambient + diffuse + specular;
  color = color / (color + vec3(1.)); // тональная компрессия
  color = pow(color, vec3(1. / 2.2)); // гамма-коррекция
  // color = color * 0.01 + spec * 0.99;

  gl_FragColor = vec4(color, rgba.a);
}
""", ('vPosition', 'vNormal', 'vUV'), ('uVPMatrix', 'uModelM', 'uInvModelM', 'uCamPos', 'uLightPos', 'uTexture', 'uLightSource')))
    self.uVPMatrix = uniforms["uVPMatrix"]
    uModelM = uniforms["uModelM"]
    uInvModelM = uniforms["uInvModelM"]
    self.uCamPos = uniforms["uCamPos"]
    self.uLightPos = uniforms["uLightPos"]
    self.uTexture = uniforms["uTexture"]
    self.uLightSource = uniforms["uLightSource"]
    attribs = attribs["vPosition"], attribs["vNormal"], attribs["vUV"]
    def func():
      vPosition, vNormal, vUV = attribs
      glVertexAttribPointer(vPosition, 3, GL_FLOAT, False, 12 * 4, 0)
      glVertexAttribPointer(vNormal, 3, GL_FLOAT, False, 12 * 4, 3 * 4)
      glVertexAttribPointer(vUV,       2, GL_FLOAT, False, 12 * 4, 6 * 4)
      # glVertexAttribPointer(vTangent, 4, GL_FLOAT, False, 12 * 4, 8 * 4)
    self.func = func
    self.renderer = renderer
    self.location = uModelM, uInvModelM
  def draw(self, model):
    enableProgram(self.program)

    renderer = self.renderer
    camX, camY, camZ = renderer.camera
    lightX, lightY, lightZ = renderer.lightPos
    glUniform3f(self.uCamPos, camX, camY, camZ)
    glUniform3f(self.uLightPos, lightX, lightY, lightZ)
    glUniformMatrix4fv(self.uVPMatrix, 1, False, renderer.MVPmatrix, 0)
    glUniform1i(self.uLightSource, 0)
    model.draw()



class Colorama:
  def __init__(self, renderer):
    self.R = tuple(shuffle(range(256)))
    self.G = tuple(shuffle(range(256)))
    self.B = tuple(shuffle(range(256)))
    self.n = 0
    self.reverse = {}
    self.renderer = renderer
    self.genProgram()
  def next(self, cb):
    n = self.n
    self.n += 1
    r = self.R[sum((n >> i * 3 & 1) << i for i in range(8))]
    g = self.G[sum((n >> i * 3 + 1 & 1) << i for i in range(8))]
    b = self.B[sum((n >> i * 3 + 2 & 1) << i for i in range(8))]
    if not (r | g | b): return self.next()
    color = r / 255, g / 255, b / 255
    self.reverse[color] = cb
    return color
  def to_n(self, rgba):
    r, g, b, a = rgba
    color = r / 255, g / 255, b / 255
    return self.reverse.get(color, None)
  def genProgram(self):
    self.program = _, attribs, uniforms = checkProgram(newProgram("""
attribute vec3 vPosition;
uniform mat4 uMVPMatrix;

void main() {
  gl_Position = uMVPMatrix * vec4(vPosition.xyz, 1);
}
""", """
precision mediump float;
uniform vec3 uColor;

void main() {
  gl_FragColor = vec4(uColor, 1.);
}
""", ('vPosition',), ('uMVPMatrix', 'uColor')))
    uMVPMatrix = uniforms["uMVPMatrix"]
    uColor = uniforms["uColor"]
    vPosition = attribs["vPosition"]
    def func(color):
      r, g, b = color
      glUniform3f(uColor, r, g, b)
      glVertexAttribPointer(vPosition, 3, GL_FLOAT, False, 12 * 4, 0)
      #glVertexAttribPointer(a["vNormal"], 3, GL_FLOAT, False, 12 * 4, 3 * 4)
      #glVertexAttribPointer(a["vUV"],       2, GL_FLOAT, False, 12 * 4, 6 * 4)
      #glVertexAttribPointer(a["vTangent"], 4, GL_FLOAT, False, 12 * 4, 8 * 4)
    self.func = func
    self.location = uMVPMatrix
  def draw(self, model):
    renderer = self.renderer
    renderer.colorDimension = True
    enableProgram(self.program)
    model.draw()
    renderer.colorDimension = False





# Дальнейший код ТОЛЬКО для примера!

ENV_MAP_FLAT_TEX_SLOT = 0 # Texture slot for the 2D HDR environment map
ENV_MAP_CUBE_TEX_SLOT = 1 # Texture slot for the 3D HDR environment cube map
DIFFUSE_IRRADIANCE_CUBE_TEX_SLOT = 2 # Texture slot for the 3D HDR diffuse irradiance map
GLOSSY_IRRADIANCE_CUBE_TEX_SLOT = 3 # Texture slot for the 3D HDR glossy irradiance map
BRDF_LUT_TEX_SLOT = 4 # Texture slot for the BRDF lookup texture

ALBEDO_TEX_SLOT = 5
METALLIC_TEX_SLOT = 6
ROUGHNESS_TEX_SLOT = 7
AO_TEX_SLOT = 8
NORMALS_TEX_SLOT = 9
DISPLACEMENT_TEX_SLOT = 10

class _PBR:
  def __init__(self):
    self.genProgram()

  def genProgram(self):
    self.program = program, attribs, uniforms = checkProgram(newProgram("""
attribute vec3 vs_Pos;
attribute vec3 vs_Nor; // Surface normal
attribute vec3 vs_Tan; // Surface tangent
attribute vec3 vs_Bit; // Surface bitangent
attribute vec2 vs_UV;

uniform mat4 u_Model;
uniform mat4 u_ModelInvTr;
uniform mat4 u_ViewProj;

uniform sampler2D u_NormalMap;
uniform bool u_UseNormalMap;
uniform sampler2D u_DisplacementMap;
uniform float u_DisplacementMagnitude;
uniform bool u_UseDisplacementMap;

varying vec3 fs_Pos;
varying vec3 fs_Nor;
varying vec3 fs_Tan;
varying vec3 fs_Bit;
varying vec2 fs_UV;

void main() {
    mat3 invTranspose = mat3(u_ModelInvTr);
    fs_Nor = normalize(invTranspose * vs_Nor);
    fs_Tan = normalize(mat3(u_Model) * vs_Tan);
    fs_Bit = normalize(mat3(u_Model) * vs_Bit);

    vec3 N = vs_Nor;
    vec3 displacedPos = vs_Pos;
    if (u_UseDisplacementMap) {
        // TODO: Apply displacement mapping with
        // u_DisplacementMap and u_DisplacementMagnitude
    }

    vec4 modelposition = u_Model * vec4(displacedPos, 1.);
    fs_Pos = modelposition.xyz;

    fs_UV = vs_UV;

    gl_Position = u_ViewProj * modelposition;
}
""", """
precision mediump float;

varying vec3 fs_Pos;
varying vec3 fs_Nor; // Surface normal
varying vec3 fs_Tan; // Surface tangent
varying vec3 fs_Bit; // Surface bitangent
varying vec2 fs_UV;

uniform vec3 u_CamPos;

// PBR material attributes
uniform vec3 u_Albedo;
uniform float u_Metallic;
uniform float u_Roughness;
uniform float u_AmbientOcclusion;
// Texture maps for controlling some of the attribs above, plus normal mapping
uniform sampler2D u_AlbedoMap;
uniform sampler2D u_MetallicMap;
uniform sampler2D u_RoughnessMap;
uniform sampler2D u_AOMap;
uniform sampler2D u_NormalMap;
// If true, use the textures listed above instead of the GUI slider values
uniform bool u_UseAlbedoMap;
uniform bool u_UseMetallicMap;
uniform bool u_UseRoughnessMap;
uniform bool u_UseAOMap;
uniform bool u_UseNormalMap;

// Image-based lighting
uniform samplerCube u_DiffuseIrradianceMap;
uniform samplerCube u_GlossyIrradianceMap;
uniform sampler2D u_BRDFLookupTexture;

const float PI = 3.141592653589793;

// -------------------------------------------------
float DistributionGGX(vec3 N, vec3 H, float a) {
    float a2     = a*a*a*a;
    float NdotH  = max(dot(N, H), 0.);
    float NdotH2 = NdotH*NdotH;

    float nom    = a2;
    float denom  = (NdotH2 * (a2 - 1.) + 1.);
    denom        = PI * denom * denom;

    return nom / denom;
}

// --------------------------------------------------
float GeometrySchlickGGX(float NdotV, float k) {
    float nom   = NdotV;
    float denom = NdotV * (1. - k) + k;

    return nom / denom;
}

float GeometrySmith(vec3 N, vec3 V, vec3 L, float k) {
    float NdotV = max(dot(N, V), 0.);
    float NdotL = max(dot(N, L), 0.);
    float ggx1 = GeometrySchlickGGX(NdotV, k);
    float ggx2 = GeometrySchlickGGX(NdotL, k);

    return ggx1 * ggx2;
}
// --------------------------------------------------
// we take the roughness into consideration now
// the rougher the surface, less fresnel effects
vec3 fresnelSchlickRoughness(float cosTheta, vec3 F0, float roughness) {
    return F0 + (max(vec3(1.0 - roughness), F0) - F0) * pow(clamp(1.0 - cosTheta, 0.0, 1.0), 5.0);
}
void main() {
    vec3 albedo = u_UseAlbedoMap ? texture2D(u_AlbedoMap, fs_UV).rgb : u_Albedo;
    float metallic = u_UseMetallicMap ? texture2D(u_MetallicMap, fs_UV).r : u_Metallic;
    float roughness = u_UseRoughnessMap ? texture2D(u_RoughnessMap, fs_UV).r : u_Roughness;
    float ambientOcclusion = u_UseAOMap ? texture2D(u_AOMap, fs_UV).r : u_AmbientOcclusion;
    vec3 N = u_UseNormalMap ? texture2D(u_NormalMap, fs_UV).rgb : fs_Nor;

    // the ray traveling from the point to camera
    vec3 wo = normalize(u_CamPos - fs_Pos);
    // microfacet surface normal to reflect wo in the direction of wi
    vec3 wh = N;
    // the ray traveling from the point to irradiance source
    vec3 wi = reflect(-wo, wh);

    vec3 baseReflectivty = mix(vec3(0.04), albedo, metallic);

    // reflectance equation
    vec3 Lo = vec3(0.);

    // ambient light
    // diffusion
    vec3 kS = fresnelSchlickRoughness(max(dot(wh, wo), 0.), baseReflectivty, roughness);
    vec3 kD = (1. - kS) ; // energy conservation
    vec3 irradiance = textureCube(u_DiffuseIrradianceMap, N).rgb;
    vec3 diffuse = irradiance * albedo ;

    // speculation: sample both the pre-filter map and the BRDF lut and combine them together as per the Split-Sum approximation to get the IBL specular part.
    // const float MAX_REFLECTION_LOD = 4.;
    // vec3 prefilteredColor = textureLod(u_GlossyIrradianceMap, wi,  roughness * MAX_REFLECTION_LOD).rgb;
    vec3 prefilteredColor = textureCube(u_GlossyIrradianceMap, wi).rgb;
    vec2 brdf  = texture2D(u_BRDFLookupTexture, vec2(max(dot(wh, wo), 0.), roughness)).rg;
    vec3 specular = prefilteredColor * (baseReflectivty * brdf.x + brdf.y);

    vec3 ambient  = (kD * diffuse + specular) * ambientOcclusion;

    vec3 color = ambient + Lo;

    // tone mapping: apply the Reinhard operator to your color term
    color = color / (color + vec3(1.));
    // gamma correction
    color = pow(color, vec3(1. / 2.2));

    gl_FragColor = vec4(color, 1.);
}
""", (), ()))
    print("OK shader!!!")
