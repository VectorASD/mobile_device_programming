import myGL



class Model:
  vPosition = vColor = vUV = None
  def calcAttribs(attribs):
    Model.vPosition = attribs["vPosition"]
    Model.vColor    = attribs["vColor"]
    Model.vUV       = attribs["vUV"]

  def __init__(self, VBOdata, IBOdata = None):
    if IBOdata is None and len(VBOdata) == 3:
      self.data = VBOdata
      self.matrix = None
      return

    buffers = INT.new_array(2)
    glGenBuffers(2, buffers, 0)
    VBO, IBO = buffers

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

    print2("✅ OK buffers:", VBO, IBO)
    self.data = VBO, IBO, IBOdata.capacity()
    self.matrix = None

  def recalc(self, location, mat):
    self.matrix = location, mat

  def draw(self, func = None):
    VBO, IBO, indexes = self.data

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, IBO)

    if func is None:
      glVertexAttribPointer(Model.vPosition, 3, GL_FLOAT, False, 9 * 4, 0)
      glVertexAttribPointer(Model.vColor,    4, GL_FLOAT, False, 9 * 4, 3 * 4)
      glVertexAttribPointer(Model.vUV,       2, GL_FLOAT, False, 9 * 4, 7 * 4)
    else: func()

    mat = self.matrix
    if mat is not None:
      location, mat = mat
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



class TranslateModel:
  def __init__(self, model, translate):
    self.model = model
    self.translate = translate

  def recalc(self, location, mat):
    tMat = FLOAT.new_array(16)
    x, y, z = self.translate
    translateM2(tMat, 0, mat, 0, x, y, z)
    self.model.recalc(location, tMat)

  def draw(self, func = None): self.model.draw(func)
  def delete(self): self.model.delete()
  def clone(self):
    return TranslateModel(self.model.clone(), self.model)



class ScaleModel:
  def __init__(self, model, scale):
    self.model = model
    self.scale = scale

  def recalc(self, location, mat):
    sMat = FLOAT.new_array(16)
    x, y, z = self.scale
    scaleM2(sMat, 0, mat, 0, x, y, z)
    self.model.recalc(location, sMat)

  def draw(self, func = None): self.model.draw(func)
  def delete(self): self.model.delete()
  def clone(self):
    return ScaleModel(self.model.clone(), self.scale)



class MatrixModel:
  def __init__(self, model, matrix):
    self.model = model
    self.matrix = matrix

  def recalc(self, location, mat):
    sMat = FLOAT.new_array(16)
    multiplyMM(sMat, 0, mat, 0, self.matrix, 0)
    self.model.recalc(location, sMat)

  def draw(self, func = None): self.model.draw(func)
  def delete(self): self.model.delete()
  def clone(self):
    return MatrixModel(self.model.clone(), self.matrix)



class TexturedModel:
  def __init__(self, model, textureID):
    self.model = model
    self.textureID = textureID

  def recalc(self, location, mat):
    self.model.recalc(location, mat)

  def draw(self, func = None):
    texture = self.textureID
    if texture.isdef(): texture = texture()
    glBindTexture(GL_TEXTURE_2D, texture)
    self.model.draw(func)

  def delete(self): self.model.delete()
  def clone(self):
    return TexturedModel(self.model.clone(), self.textureID)



class NoCullFaceModel:
  def __init__(self, model):
    self.model = model

  def recalc(self, location, mat):
    self.model.recalc(location, mat)

  def draw(self, func = None):
    glDisable(GL_CULL_FACE)
    self.model.draw(func)
    glEnable(GL_CULL_FACE)

  def delete(self): self.model.delete()
  def clone(self): return self.model.clone()





class Quaternion:
  def __init__(self, x, y, z, w):
    self.xyzw = x, y, z, w
  def fromYPR(yaw, pitch, roll):
    yaw /= 2
    pitch /= 2
    roll /= 2
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



class SkyBox:
  program = None
  model = None
  def __init__(self, width, height, textureGetter):
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
    program, attribs, uniforms = SkyBox.program
    self.vPosition = attribs["vPosition"]
    self.uVPMatrix = uniforms["uVPMatrix"]
    self.uSkybox = uniforms["uSkybox"]

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
    ))

  def draw(self, VPmatrix):
    def func():
      glVertexAttribPointer(self.vPosition, 3, GL_FLOAT, False, 0, 0)

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    enableProgram(SkyBox.program)
    glUniformMatrix4fv(self.uVPMatrix, 1, False, VPmatrix, 0)
    glUniform1f(self.uSkybox, 0)
    glBindTexture(GL_TEXTURE_CUBE_MAP, self.textureId)

    SkyBox.model.draw(func)

    glBindTexture(GL_TEXTURE_CUBE_MAP, 0)
    glDepthFunc(GL_LESS)

  def restart(self):
    print("SKYBOX RESTART!")
    SkyBox.model = None
    SkyBox.program = None



def skyBoxLoader(gridProgram, dbg = False):
  oldViewportParams = INT.new_array(4)
  glGetIntegerv(GL_VIEWPORT, oldViewportParams, 0)

  fbo = newFrameBuffer(32, 32, False)
  glBindFramebuffer(GL_FRAMEBUFFER, fbo[0])
  glViewport(0, 0, 32, 32)
  #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  #glClear(GL_DEPTH_BUFFER_BIT) а смысл, если в FBO нет рендер-буфера глубины

  def textureCutter(n):
    id = (4, 50, 384, 65, 78, 401)[n]
    model = gridProgram.createModel(id, 0, 0, 1)
    gridProgram.draw(1, 0, (model,))
    model.delete()
    buffer = MyBuffer.allocateDirect(32 * 32 * 4)
    buffer._m_order(MyBuffer.nativeOrder)
    glReadPixels(0, 0, 32, 32, GL_RGBA, GL_UNSIGNED_BYTE, buffer)
    if dbg:
      buffer = buffer._m_asIntBuffer()
      #assert buffer._m_remaining() == 1024
      arr = INT.new_array(buffer._m_remaining())
      buffer._m_get(arr)
      print("👍", n, arr[:])
    return buffer

  skybox = SkyBox(32, 32, textureCutter)

  glBindFramebuffer(GL_FRAMEBUFFER, 0)
  deleteFrameBuffer(fbo)
  x, y, w, h = oldViewportParams
  glViewport(x, y, w, h)
  return skybox

glDepthFunc = GLES20._mw_glDepthFunc(int) # func
GL_LEQUAL = GLES20._f_GL_LEQUAL
GL_LESS = GLES20._f_GL_LESS



class TextureChain:
  def __init__(self):
    self.genProgram()
    self.genModel()
    # self.FBOs = {}
    self.FBO = None

  def genProgram(self):
    self.program = program, attribs, uniforms = checkProgram(newProgram("""
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
    gl_FragColor = texture2D(uTexture, vaUV) * uTextureColor;
}
""", ('vPosition', 'vUV'), ('uTexture', 'uTextureColor')))
    self.vPosition = attribs["vPosition"]
    self.vUV = attribs["vUV"]
    self.uTexture = uniforms["uTexture"]
    self.uTextureColor = uniforms["uTextureColor"]

  def genModel(self):
    self.model = Model((
      -1, -1, 0, 0,
      -1, 1, 0, 1,
      1, -1, 1, 0,
      1, 1, 1, 1,
    ), (0, 1, 2, 1, 2, 3))
    def func():
      glVertexAttribPointer(self.vPosition, 2, GL_FLOAT, False, 4 * 4, 0)
      glVertexAttribPointer(self.vUV,       2, GL_FLOAT, False, 4 * 4, 2 * 4)
    self.func = func

  def use(self, size, baseColor, textures = ()):
    W, H = size
    # try: fbo = self.FBOs[size]
    # except KeyError: fbo = self.FBOs[size] = newFrameBuffer(W, H, False)
    fbo, texture, _ = newFrameBuffer(W, H, False, self.FBO, GL_LINEAR)
    self.FBO = fbo

    oldViewportParams = INT.new_array(4)
    glGetIntegerv(GL_VIEWPORT, oldViewportParams, 0)

    glBindFramebuffer(GL_FRAMEBUFFER, fbo)
    glViewport(0, 0, W, H)
    r, g, b, a = baseColor
    glClearColor(r, g, b, a)
    glClear(GL_COLOR_BUFFER_BIT)
    glDisable(GL_CULL_FACE)
    glDisable(GL_DEPTH_TEST)

    enableProgram(self.program)
    glUniform1f(self.uTexture, 0)
    draw, func = self.model.draw, self.func
    for texture2, textureColor in textures:
      r, g, b, a = textureColor
      glUniform4f(self.uTextureColor, r, g, b, a)
      glBindTexture(GL_TEXTURE_2D, texture2)
      draw(func)

    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    x, y, w, h = oldViewportParams
    glViewport(x, y, w, h)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)

    return texture
