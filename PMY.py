if True: # __name__ == "__main__":
  from executor import main, load_codes # пока нереализован доступный всем способ компиляции БЕЗ доступа к компилятору (облачные технологии)
  import os
  load_codes(os.path.basename(__file__))
  main("pmy")
  exit()

###~~~### pmy

import myGL
import myGLclasses
import rbxmReader



def mainProgram():
  return checkProgram(newProgram("""
attribute vec3 vPosition;
attribute vec4 vColor;
attribute vec2 vUV;

uniform mat4 uMVPMatrix;

varying vec4 vaColor;
varying vec2 vaUV;

void main() {
  gl_Position = uMVPMatrix * vec4(vPosition.xyz, 1);
  vaColor = vColor;
  vaUV = vUV;
}
""", """
precision mediump float;

uniform sampler2D uTexture;

varying vec4 vaColor;
varying vec2 vaUV;

void main() {
  if (vaUV.x < 0.) gl_FragColor = vaColor;
  else gl_FragColor = texture2D(uTexture, vaUV);
}
""", ('vPosition', 'vColor', 'vUV'), ('uMVPMatrix', 'uTexture')))



class d2textureProgram():
  def __init__(self, texture, size):
    self.program = program = checkProgram(newProgram("""
attribute vec2 vPosition;
attribute vec2 vUV;
attribute float vType;

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
  gl_Position = vec4(vPosition.x, vPosition.y * uAspect - (1. - uAspect), 0, 1);
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
""", ('vPosition', 'vUV', 'vType'), ('uTexture', 'uAspect', 'uEvent')))
    uniforms = program[2]
    self.uTexture = uniforms["uTexture"]
    self.uAspect = uniforms["uAspect"]
    self.uEvent = uniforms["uEvent"]
    self.models = []
    self.modelPositions = []
    self.aspect = 1
    self.texture = texture
    self.size        = W, H = size
    self.textureSize = tW, tH = texture2size[texture]
    self.tileSize    = (tW + W - 1) // W, (tH + H - 1) // H

  def createModel(self, id, posX, posY, L = 10, t = 0, invertX = False, invertY = False):
    W, H = self.size
    L /= 2
    L1 = L - 1
    pLx, pRx, pLy, pRy = (posX - L) / L, (posX - L1) / L, (posY - L) / -L, (posY - L1) / -L
    y, x = divmod(id, W)
    Lx, Rx, Ly, Ry = x / W, (x + 1) / W, y / H, (y + 1) / H
    if invertX: Lx, Rx = Rx, Lx
    if invertY: Ly, Ry = Ry, Ly
    return Model((
      pLx, pLy, Lx, Ly, t,
      pRx, pLy, Rx, Ly, t,
      pRx, pRy, Rx, Ry, t,
      pLx, pRy, Lx, Ry, t,
    ), (
      0, 1, 2, 0, 2, 3,
    ))
  def add(self, id, posX, posY, L = 10, t = 0, invertX = False, invertY = False):
    model = self.createModel(id, posX, posY, L, t, invertX, invertY)
    self.models.append(model)
    self.modelPositions.append((posX / L, (posX + 1) / L, posY / L, (posY + 1) / L, t))

  def draw(self, aspect, eventN, customModels = None):
    self.aspect = aspect
    def func():
      glVertexAttribPointer(vPosition, 2, GL_FLOAT, False, 5 * 4, 0)
      glVertexAttribPointer(vUV,       2, GL_FLOAT, False, 5 * 4, 2 * 4)
      glVertexAttribPointer(vType,     1, GL_FLOAT, False, 5 * 4, 4 * 4)
    attribs = self.program[1]
    vPosition, vUV, vType = attribs["vPosition"], attribs["vUV"], attribs["vType"]

    glDisable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)
    enableProgram(self.program)
    glUniform1f(self.uAspect, aspect)
    glUniform1i(self.uEvent, eventN)
    glUniform1i(self.uTexture, 0)
    glBindTexture(GL_TEXTURE_2D, self.texture)

    models = customModels if customModels is not None else self.models
    for model in models: model.draw(func)
  
  def checkPosition(self, x, y, up):
    # x и y от 0 до 1
    aspect = self.aspect
    """
    1x2 aspect=0.5
    y = 0.5 -> 0
    y = 1 -> 1
    1x3 aspect=0.33
    y = 0.66 -> 0
    y = 1 -> 1
    """
    y = (y - (1 - aspect)) / aspect
    result = -1
    for x1, x2, y1, y2, t in self.modelPositions:
      if x1 - up <= x and x <= x2 + up and y1 - up <= y and y <= y2 + up: result = t
    return result



def figures():
  ratio = (2 ** 2 - 1) ** 0.5
  ratio2 = ratio * 0.6

  triangles = Model((
      0,  ratio, 4, 1, 0, 0, 1, -1, -1,
     -2, -ratio, 4, 0, 1, 0, 1, -1, -1,
      2, -ratio, 4, 0, 0, 1, 1, -1, -1,
   -1.6,  ratio, 4, 1, 1, 0, 1, -1, -1,
   -1.2, ratio2, 4, 1, 0, 1, 1, -1, -1,
     -2, ratio2, 4, 0, 1, 1, 1, -1, -1,
   -1.2,  ratio, 4, 0, 0, 0, 0, -1, -1,
  ), (
    0, 2, 1, 3, 4, 5, 0, 4, 6, # старые 3 треугольника
  ))

  cube = Model((
    -1, -1, -1,   1, 1, 1, 1,   -1, -1, #  0
     1, -1, -1,   1, 0, 0, 1,   -1, -1, #  1
     1, -1,  1,   1, 1, 0, 1,   -1, -1, #  2
    -1, -1,  1,   0, 0, 1, 1,   -1, -1, #  3
    -1,  1, -1,   0, 1, 0, 1,   -1, -1, #  4
     1,  1, -1,   0, 1, 1, 1,   -1, -1, #  5
     1,  1,  1,   0, 0, 0, 0,   -1, -1, #  6
    -1,  1,  1,   1, 0, 1, 1,   -1, -1, #  7
    -1, -1, -1,   1, 1, 1, 1,    1, 0, # 8
     1, -1, -1,   1, 0, 0, 1,    0, 0, # 9
    -1,  1, -1,   0, 1, 0, 1,    1, 1, # 10
     1,  1, -1,   0, 1, 1, 1,    0, 1, # 11
  ), (
     0,  1,  2,  0,  2,  3, # дно куба
   # 0,  1,  4,  1,  4,  5, # фронт
     8, 10,  9,  9, 10, 11, # фронт
     1,  5,  2,  2,  5,  6, # правый бок
     2,  7,  3,  2,  6,  7, # тыл
     3,  7,  0,  0,  7,  4, # левый бок
     4,  7,  5,  5,  7,  6, # верх куба
  ))

  gridN = 8
  gridRange = range(gridN)
  faces = []
  facesAppend = faces.append
  for x in gridRange:
    for z in gridRange:
      x1, x2 = x / gridN * 2 - 1, (x + 1) / gridN * 2 - 1
      z1, z2 = z / gridN * 2 - 1, (z + 1) / gridN * 2 - 1
      a, b, c, d = (x1, -1, z1, x1, z1), (x1, -1, z2, x1, z2), (x2, -1, z1, x2, z1), (x2, -1, z2, x2, z2)
      facesAppend((a, c, b))
      facesAppend((b, c, d))
      a, b, c, d = (x1, 1, z1, x1, z1), (x1, 1, z2, x1, z2), (x2, 1, z1, x2, z1), (x2, 1, z2, x2, z2)
      facesAppend((a, b, c))
      facesAppend((b, d, c))
      a, b, c, d = (-1, x1, z1, x1, z1), (-1, x1, z2, x1, z2), (-1, x2, z1, x2, z1), (-1, x2, z2, x2, z2)
      facesAppend((a, b, c))
      facesAppend((b, d, c))
      a, b, c, d = (1, x1, z1, x1, z1), (1, x1, z2, x1, z2), (1, x2, z1, x2, z1), (1, x2, z2, x2, z2)
      facesAppend((a, c, b))
      facesAppend((b, c, d))
      a, b, c, d = (x1, z1, -1, x1, z1), (x1, z2, -1, x1, z2), (x2, z1, -1, x2, z1), (x2, z2, -1, x2, z2)
      facesAppend((a, b, c))
      facesAppend((b, d, c))
      a, b, c, d = (x1, z1, 1, x1, z1), (x1, z2, 1, x1, z2), (x2, z1, 1, x2, z1), (x2, z2, 1, x2, z2)
      facesAppend((a, c, b))
      facesAppend((b, c, d))
  VBOdata, IBOdata = buildModel(faces)
  VBOdata2 = []
  VBOextend = VBOdata2.extend
  for n in range(len(VBOdata)):
    x, y, z, U, V = VBOdata[n]
    L = (x * x + y * y + z * z) ** 0.5
    # r, g, b = (sin(n * 3) + 2) / 3, (sin(n * 4) + 2) / 3, (sin(n * 5) + 2) / 3
    VBOextend((x / L, y / L, z / L, 0, 0, 0, 0, (U + 1) / 2, (V + 1) / 2))
  sphere = Model(VBOdata2, IBOdata)
  return triangles, cube, sphere



class myRenderer:
  def __init__(self):
    self.frames = self.last_frames = 0
    self.last_time = time() + 0.1
    self.frame_pos = 0
    self.frame_arr = []
    self.fpsS = "?"
    self.yaw, self.pitch, self.roll = 180, 0, 0
    self.camX, self.camY, self.camZ = 0, 0, -3.5
    self.eventN = 0
    self.time, self.td = time(), 0

    self.W = self.H = self.WH_ratio = -1
    self.FBO = None
    self.ready = False

    textures = rm.get("drawable/textures")
    skybox_labeled = rm.get("drawable/skybox_labeled")
    skybox_space = rm.get("drawable/skybox_space")
    self.texture_base = textures, skybox_labeled, skybox_space

  def fps(self):
    T = time()
    arr = self.frame_arr
    if T >= self.last_time:
      self.last_time = T + 0.1
      fd = self.frames - self.last_frames
      self.last_frames = self.frames
      if len(arr) < 10: self.frame_arr.append(fd)
      else:
        pos = self.frame_pos
        arr[pos] = fd
        self.frame_pos = (pos + 1) % 10
      self.fpsS = S = sum(arr) * 10 // len(arr)
      print(S)
    return self.fpsS

  def onSurfaceCreated(self, gl10, config):
    self.ready = False
    print("📽️ onSurfaceCreated", gl10, config)
    self.time, self.td = time(), 0

    # glClearColor(0.9, 0.95, 1, 0)
    self.program = program, attribs, uniforms = mainProgram()
    Model.calcAttribs(attribs)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # glActiveTexture(GL_TEXTURE0) и так по умолчанию

    self.viewM = FLOAT.new_array(16)
    self.projectionM = FLOAT.new_array(16)
    self.MVPmatrix = FLOAT.new_array(16)
    self.VPmatrix = FLOAT.new_array(16)

    self.calcViewMatrix()

    textures, skybox_labeled, skybox_space = self.texture_base
    self.mainTexture = mainTextures = newTexture(ctxResources, textures)
    skyboxLabeled = newTexture(ctxResources, skybox_labeled)
    skyboxSpace   = newTexture(ctxResources, skybox_space)
    print("textures:",       hex(textures),       mainTextures)
    print("skybox_labeled:", hex(skybox_labeled), skyboxLabeled)
    print("skybox_space:",   hex(skybox_space),   skyboxSpace)

    self.program2 = gridProgram = d2textureProgram(mainTextures, (8, 64))
    gridProgram.add(160, 0.25, 5.5,  8, 1)
    gridProgram.add(142, 0.25, 6.75, 8, 2)
    gridProgram.add(45,  6.75, 6.75, 8, 3)
    self.skyboxes = (
      skyBoxLoader(gridProgram, (4, 50, 384, 65, 78, 401)),
      skyBoxLoader(d2textureProgram(skyboxLabeled, (1, 6)), (0, 1, 2, 3, 4, 5)),
      skyBoxLoader(d2textureProgram(skyboxSpace, (4, 3)), (6, 4, 3, 11, 7, 5), True),
      None,
    )
    self.skyboxN       = 2
    self.currentSkybox = self.skyboxes[self.skyboxN]

    self.textureChain = TextureChain()

    union, PBR_models, character = loadRBXM(__resource("avatar.rbxm"), "avatar.rbxm", self.textureChain)

    union = RotateModel(union, (45, 0, 0))
    union = TranslateModel(union, (5, 0, 0))
    PBR_models2 = []
    for model in PBR_models:
      model = RotateModel(model, (45, 0, 0))
      PBR_models2.append(TranslateModel(model, (5, 0, 0)))
    self.rbxModel, self.rbxPBRModels, self.character = union, PBR_models2, character

    triangles, cube, sphere = figures()
    fboTex = lambda: self.FBO[1]
    self.models = (
      NoCullFaceModel(triangles),
      TexturedModel(ScaleModel(cube, (0.5, 1, 0.5)), fboTex),
      TexturedModel(TranslateModel(ScaleModel(cube.clone(), (1, 1, 0.5)), (-2, 0, 0)), dbgTextures[0]),
      TexturedModel(TranslateModel(ScaleModel(cube.clone(), (1, 1, 0.5)), (-4.5, 0, 0)), dbgTextures[1]),
      TexturedModel(TranslateModel(sphere, (0, 3, 0)), fboTex),
    )

    self.pbr = PBR()

  def onSurfaceChanged(self, gl10, width, height):
    print("📽️ onSurfaceChanged", gl10, width, height)
    if width == self.W and height == self.H: return

    glViewport(0, 0, width, height)
    self.W, self.H, self.WH_ratio = width, height, width / height

    perspectiveM(self.projectionM, 0, 90, self.WH_ratio, 0.01, 1000)
    self.calcMVPmatrix()

    if self.FBO is not None: deleteFrameBuffer(self.FBO)
    self.FBO = newFrameBuffer(width, height)
    self.ready = True

  def calcMVPmatrix(self):
    MVPmatrix = self.MVPmatrix
    multiplyMM(MVPmatrix, 0, self.projectionM, 0, self.viewM, 0)
    # print("MVP:", self.MVPmatrix[:])
    multiplyMM(self.VPmatrix, 0, self.projectionM, 0, self.viewNotTranslatedM, 0)
    self.updMVP = False

    location = self.program[2]["uMVPMatrix"]
    location2 = self.pbr.uModelM, self.pbr.uInvModelM
    pbr_mat = FLOAT.new_array(16)
    setIdentityM(pbr_mat, 0)

    for model in self.models: model.recalc(location, MVPmatrix)
    self.rbxModel.recalc(location, MVPmatrix)
    for model in self.rbxPBRModels: model.recalc(location2, pbr_mat)
    self.character.recalc(location, location2, MVPmatrix)

  def calcViewMatrix(self):
    q = Quaternion.fromYPR(self.yaw, self.pitch, self.roll)
    q2 = q.conjugated()
    self.viewNotTranslatedM = mat = q2.toMatrix()

    translateM2(self.viewM, 0, mat, 0, -self.camX, -self.camY, -self.camZ)

    self.updMVP = True
    self.forward = q.rotatedVector(0, 0, -1)

  def eventHandler(self):
    td, event = self.td, self.eventN
    if event in (1, 2):
      if event == 2: td = -td
      x, y, z = self.forward
      td *= 5
      self.camX += x * td
      self.camY += y * td
      self.camZ += z * td
      self.calcViewMatrix()

  def drawScene(self):
    # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)

    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)

    program = self.program
    enableProgram(program)
    #checkGLError() TODO
    #glUniform1i(program[2]["uTexture"], 0)
    #checkGLError()

    for model in self.models: model.draw()
    self.rbxModel.draw()
    camPos = self.camX, self.camY, self.camZ
    self.pbr.draw(self.rbxPBRModels, camPos, self.MVPmatrix)

    enableProgram(program)
    self.character.draw(self.pbr, camPos, self.MVPmatrix)

    skybox = self.currentSkybox
    if skybox is not None: skybox.draw(self.VPmatrix)

    self.program2.draw(self.WH_ratio, self.eventN)

  def onDrawFrame(self, gl10):
    self.frames += 1
    T = time()
    self.td = T - self.time
    self.time = T
    #print("📽️ onDraw", gl)

    self.eventHandler()
    if self.updMVP: self.calcMVPmatrix()

    character = self.character
    yaw, pitch, roll = character.YPR
    yaw = (yaw + 15 * self.td) % 360
    character.setRotation(yaw, pitch, roll)

    glBindFramebuffer(GL_FRAMEBUFFER, self.FBO[0])
    self.drawScene()
    glBindFramebuffer(GL_FRAMEBUFFER, 0)

    #self.textureChain.use2(self.FBO[1])
    self.drawScene()
    #self.fps()

  def move(self, dx, dy):
    if not self.ready: return
    self.yaw -= dx * 0.5
    self.pitch = max(-90, min(self.pitch - dy * 0.5, 90))
    self.calcViewMatrix()

  def event(self, up, down, misc):
    self.eventN = up | down << 1 | misc << 2

  def getTByPosition(self, x, y, up):
    if not self.ready: return -1
    return self.program2.checkPosition(x / self.W, y / self.H, up)

  def click(self, x, y, click_td):
    if not self.ready: return
    if click_td > 0.5: return
    t = self.getTByPosition(x, y, 0.01)
    if t == 3:
      self.skyboxN = N = (self.skyboxN + 1) % len(self.skyboxes)
      self.currentSkybox = self.skyboxes[N]
    # print("🐾 click:", x, y, t)

  def restart(self):
    print2("~" * 53)
    self.W = self.H = self.WH_ratio = -1
    self.FBO = None
    SkyBox.restart()

  reverse = {
    "cr": onSurfaceCreated,
    "ch": onSurfaceChanged,
    "df": onDrawFrame,
  }



main_xml = """
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:orientation="vertical"
    android:layout_width="match_parent"
    android:layout_height="match_parent">
    <TextView
        android:textSize="29dp"
        android:textColor="#40ad80"
        android:layout_gravity="center"
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="TEXT"/>
</LinearLayout>
""".strip()

class activityHandler:
  def onCreate(self, activity):
    ctx = activity._m_getApplicationContext().cast(Context)
    print("onCreate", self, activity)

    activity._m_requestWindowFeature(FEATURE_NO_TITLE) # Remove title bar
    activity._m_getWindow()._m_setFlags(FLAG_FULLSCREEN, FLAG_FULLSCREEN) # Remove notification bar

    view = GLSurfaceView(ctx)
    renderer = myRenderer()
    renderer2 = rm.renderer(renderer)
    print("V:", view)
    print("R:", renderer2)
    view._m_setEGLContextClientVersion(2)
    view._m_setRenderer(renderer2)
    activity._mw_setContentView(View)(view)

    self.viewResume = view._mw_onResume()
    self.viewPause = view._mw_onPause()
    self.renderer = renderer
    self.prevXY = {}
    self.startXYT = {}
    self.eventA = set()
    self.eventB = set()
    self.eventC = set()

    return True # lock setContentView

  def onStart(self): print("onStart")
  def onRestart(self):
    print("onRestart")
    self.renderer.restart()
  def onResume(self):
    print("onResume")
    self.viewResume()
  def onPause(self):
    print("onPause")
    self.viewPause()
  def onStop(self): print("onStop")
  def onDestroy(self): print("onDestroy")
  def onTouchEvent(self, e):
    action = e._m_getAction()
    getX = e._mw_getX(int)
    getY = e._mw_getY(int)
    getPointerId = e._mw_getPointerId(int)
    prevXY, startXYT, renderer = self.prevXY, self.startXYT, self.renderer
    actionN = action >> 8
    action &= 255
    W32 = renderer.W / 32
    W5_5, W6 = W32 * 5.5, W32 * 6
    H8 = renderer.H - W5_5
    H8b = H8 - W5_5
    T = time()
    if action in ACTION_DOWN:
      x, y, id = getX(actionN), getY(actionN), getPointerId(actionN)
      t = renderer.getTByPosition(x, y, 0.01)
      """
      if x < W6 and y > H8b:
        prevXY[id] = None
        if y > H8: self.eventB.add(id)
        else: self.eventA.add(id)
        renderer.event(bool(self.eventA), bool(self.eventB))
      else: prevXY[id] = x, y
      """
      if t > 0:
        prevXY[id] = None
        if t == 1: self.eventA.add(id)
        elif t == 2: self.eventB.add(id)
        elif t == 3: self.eventC.add(id)
        renderer.event(bool(self.eventA), bool(self.eventB), bool(self. eventC))
      else: prevXY[id] = x, y
      startXYT[id] = [x, y, T, True]
    elif action == ACTION_MOVE:
      for p in range(e._m_getPointerCount()):
        x, y, id = getX(p), getY(p), getPointerId(p)
        prevv = prevXY[id]
        if prevv is None: continue
        prevX, prevY = prevv
        prevXY[id] = x, y
        self.renderer.move(x - prevX, y - prevY)

        xx, yy, t, ok = startXYT[id]
        if ok and (xx - x) ** 2 + (yy - y) ** 2 > 100: startXYT[id][3] = False
    elif action in ACTION_UP:
      x, y, id = getX(actionN), getY(actionN), getPointerId(actionN)
      prevXY[id] = 0, 0 # del prevXY[id] пока нет :/
      self.eventA.remove(id)
      self.eventB.remove(id)
      self.eventC.remove(id)
      renderer.event(bool(self.eventA), bool(self.eventB), bool(self.eventC))

      xx, yy, t, ok = startXYT[id]
      if ok and (xx - x) ** 2 + (yy - y) ** 2 < 100:
        renderer.click(xx, yy, T - t)
    elif action == ACTION_CANCEL:
      self.eventA.clear()
      self.eventB.clear()
      self.eventC.clear()
      renderer.event(False, False, False)
    return True
  def onKeyDown(self, num, e):
    print("onKeyDown", num, e)
    return True
  def onKeyUp(self, num, e):
    print("onKeyUp", num, e)
    return True
  reverse = {
    "cr": onCreate,
    "st": onStart,
    "re": onRestart,
    "res": onResume,
    "pa": onPause,
    "sto": onStop,
    "de": onDestroy,
    "to": onTouchEvent,
    "kd": onKeyDown,
    "ku": onKeyUp,
  }



rm = ctxResources = None
def Activity():
  global rm, ctxResources
  rm = ResourceManager()
  rm.xml("main", "main.xml", main_xml)
  rm.drawable("textures", "textures.png", __resource("textures.png"))
  rm.drawable("skybox_labeled", "skybox_labeled.png", __resource("skybox_labeled.png"))
  rm.drawable("skybox_space", "skybox_space.webp", __resource("skybox_space.webp"))
  #print("•", rm)
  ress = rm.release()
  ctx = ress.ctx
  ctxResources = ctx._m_getResources()
  #print("•", ress, ctx)

  activityManager = ctx._m_getSystemService(ACTIVITY_SERVICE)
  config = activityManager._m_getDeviceConfigurationInfo()
  #print("•", activityManager, config)
  #for name in config.methods().keys(): print(name)
  vers = config._f_reqGlEsVersion
  a, b, c = vers >> 16, vers >> 8 & 255, vers & 255
  print("GL: v%s.%s.%s" % (a, b, c))
  if a < 2:
    print("GLv2 not supported :/")
    return
  print("~" * 53)

  H = activityHandler()
  ress.activity("layout/main", H)

Activity()
