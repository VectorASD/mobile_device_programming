if True: # __name__ == "__main__":
  from executor import main, load_codes # пока нереализован доступный всем способ компиляции БЕЗ доступа к компилятору (облачные технологии)
  import os
  load_codes(os.path.basename(__file__))
  main("pmy")
  exit()

###~~~### pmy

import random
import myGL
import myGLclasses
import myGL31
import myGLtext
import rbxmReader



class mainProgram:
  def __init__(self, renderer):
    self.program = _, attribs, uniforms = checkProgram(newProgram("""
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
    vPosition = attribs["vPosition"]
    vColor    = attribs["vColor"]
    vUV       = attribs["vUV"]
    uMVPMatrix    = uniforms["uMVPMatrix"]
    self.uTexture = uniforms["uTexture"]
    def func():
      glVertexAttribPointer(vPosition, 3, GL_FLOAT, False, 9 * 4, 0)
      glVertexAttribPointer(vColor,    4, GL_FLOAT, False, 9 * 4, 3 * 4)
      glVertexAttribPointer(vUV,       2, GL_FLOAT, False, 9 * 4, 7 * 4)
    self.func = func
    self.renderer = renderer
    self.location = uMVPMatrix



""" перепись населения (шейдерных программ):
def mainProgram()      - стартовая балванка
class d2textureProgram - резак сеточных атласов текстур
class SkyBox           - без неба сейчас нынче никак
class TextureChain     - комбинатор текстур
class PBR              - физическая не физика
class GlyphProgram     - отрисовка глифов
"""

def figures(shaderProgram):
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
  ), shaderProgram)

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
  ), shaderProgram)

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
    L = 1 / L * 0.5 + L * 0.5
    VBOextend((x / L, y / L, z / L, 0, 0, 0, 0, (U + 1) / 2, (V + 1) / 2))
  sphere = Model(VBOdata2, IBOdata, shaderProgram)
  return triangles, cube, sphere



def hierarchy(model, level = ""): # TODO
  try: next = model.model
  except AttributeError: next = None
  try: models = model.models
  except AttributeError: models = None
  level += "| "
  if next: hierarchy(next, level)
  if models:
    for model in models: hierarchy(model, level)



def planetProcessor(models, renderer):
  def hypot(size):
    x, y, z = size
    return x ** 2 + y ** 2 + z ** 2
  def haloSort():
    def dist(pos):
      x, y, z = pos
      # return (x - cX) ** 2 + (y - cY) ** 2 + (z - cZ) ** 2
      return (x - cX) * fwX + (y - cY) * fwY + (z - cZ) * fwZ
    Re = renderer # nonlocal to local
    cX, cY, cZ = Re.camX, Re.camY, Re.camZ
    fwX, fwY, fwZ = Re.forward
    nonlocal haloDraws
    halos2 = sorted(halos, key = lambda halo: dist(halo._pos), reverse = True)
    haloDraws = [halo.draw for halo in halos2]
  def drawer():
    for draw in planetDraws: draw()
    glDepthMask(False)
    for draw in haloDraws: draw()
    glDepthMask(True)

  unionM, PBR_unionM, charModelM = models
  #     unionM.type = UnionModel
  # PBR_unionM.type = UnionModel
  #     unionM.models[i].type = MatrixModel
  # PBR_unionM.models[i].type = MatrixModel
  # charModelM.type = None | CharacterModel
  models = sorted(unionM.models, key = lambda model: hypot(model.info["size"]))
  groups = {}
  order = []
  for model in models:
    key = model.info["node"]["_parent"]
    if key in groups: groups[key].append(model)
    else:
      groups[key] = [model]
      order.append(key)
  planetDraws = []
  halos = []
  haloDraws = []
  result = []
  X = 0
  for node in order:
    group = groups[node]
    print("🐾🐾🐕", len(group), node["_name"])

    size = group[-1].info["size"][0]
    if X: X += size
    pos = (X, -10, 0)
    X += size

    for model in group:
      if "decal" in model.info:
        halos.append(model)
        model._pos = pos
      else: planetDraws.append(model.draw)
    union = UnionModel(group)

    result.append(
      TranslateModel(union, pos)
    )
  renderer.camMoveEvent = haloSort
  unionM = UnionModel(result)
  unionM.draw = drawer
  return unionM, PBR_unionM, charModelM



class myRenderer:
  glVersion = 2

  def __init__(self, activity, view):
    self.activity  = activity
    self.view      = view
    self.frames    = self.last_frames = 0
    self.last_time = time() + 0.1
    self.frame_pos = 0
    self.frame_arr = []
    self.fpsS      = "?"
    self.yaw, self.pitch, self.roll = 180, 0, 0
    self.camX, self.camY, self.camZ = 0, 0, -3.5
    self.eventN = 0
    self.time, self.td = time(), 0
    self.moveTd = 0
    self.moveTd2 = 0

    self.W = self.H = self.WH_ratio = -1
    self.FBO = None
    self.ready = False
    self.camMoveEvent = lambda: None

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
      glyphs = self.glyphs
      glyphs.setHeight(self.W / 16)
      glyphs.setColor(0xadddff)
      glyphs.replace(self.fpsText, 0, self.W - self.H, self.W, "fps: %s" % S)
    return self.fpsS

  def onSurfaceCreated(self, gl10, config):
    self.ready = False
    print("📽️ onSurfaceCreated", gl10, config)
    self.time, self.td = time(), 0

    # основные настройки по умолчанию

    # glClearColor(0.9, 0.95, 1, 0)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # glActiveTexture(GL_TEXTURE0) и так по умолчанию

    # матрицы

    self.viewM       = FLOAT.new_array(16)
    self.projectionM = FLOAT.new_array(16)
    self.MVPmatrix   = FLOAT.new_array(16)
    self.VPmatrix    = FLOAT.new_array(16)

    # все негенерированные (из ресурсника) текстуры в одном месте

    textures, skybox_labeled, skybox_space = self.texture_base
    self.mainTexture = mainTextures = newTexture(ctxResources, textures)
    skyboxLabeled = newTexture(ctxResources, skybox_labeled)
    skyboxSpace   = newTexture(ctxResources, skybox_space)
    print("textures:",       hex(textures),       mainTextures)
    print("skybox_labeled:", hex(skybox_labeled), skyboxLabeled)
    print("skybox_space:",   hex(skybox_space),   skyboxSpace)

    # все шейдерные программы в одном месте

    self.program = firstProgram = mainProgram(self)
    self.gridProgram = gridProgram = d2textureProgram(mainTextures, (8, 64), self)
    self.skyboxes = (
      skyBoxLoader(gridProgram, (4, 50, 384, 65, 78, 401)),
      skyBoxLoader(d2textureProgram(skyboxLabeled, (1, 6), self), (0, 1, 2, 3, 4, 5)),
      skyBoxLoader(d2textureProgram(skyboxSpace, (4, 3), self), (6, 4, 3, 11, 7, 5), True),
      None,
    )
    self.textureChain = TextureChain(self)
    self.pbr = PBR(self)
    self.noPBR = NoPBR(self)
    self.glyphs = glyphs = glyphTextureGenerator(self)
    glyphs.printer = False

    # настройка шейдерных программ

    gridProgram.setUp(0.25)
    gridProgram.add(160, 0.25, 5.5,  8, 1)
    gridProgram.add(142, 0.25, 6.75, 8, 2)
    gridProgram.add(45,  6.75, 6.75, 8, 3)

    self.skyboxN       = 2
    self.currentSkybox = self.skyboxes[self.skyboxN]

    glyphs.setHeight(self.W / 16)
    glyphs.setColor(0xadddff)
    self.fpsText = glyphs.add(0, self.W - self.H, self.W, "fps: ?")

    # загрузка моделей

    triangles, cube, sphere = figures(firstProgram)
    fboTex = lambda: self.FBO[1]
    self.models = (
      NoCullFaceModel(triangles),
      TexturedModel(TranslateModel(ScaleModel(cube, (0.5, 1, 0.5)), (2.5, 0, 0)), fboTex),
      TexturedModel(TranslateModel(ScaleModel(cube.clone(), (1, 1, 0.5)), (0.5, 0, 0)), lambda: dbgTextures[0]),
      TexturedModel(TranslateModel(ScaleModel(cube.clone(), (1, 1, 0.5)), (-2, 0, 0)), lambda: dbgTextures[1]),
      TexturedModel(TranslateModel(sphere, (0, 3, 0)), fboTex),
    )

    if False:
      union, PBR_model, character = loadRBXM(__resource("avatar.rbxm"), "avatar.rbxm", None, self)
      SolarSystem = WaitingModel()
    else:
      SolarSystem, _, _ = loadRBXM(__resource("SolarSystem.rbxm"), "SolarSystem.rbxm", planetProcessor, self)
      union = PBR_model = character = WaitingModel()
    hierarchy(SolarSystem)

    union = RotateModel(union, (45, 0, 0))
    PBR_model = RotateModel(PBR_model, (45, 0, 0))
    self.rbxModel = TranslateModel(union, (5, 0, 0))
    self.rbxPBRmodel = TranslateModel(PBR_model, (5, 0, 0))
    self.character = character
    self.SolarSystem = SolarSystem

    # первый сигнал перерасчёта матриц модели во всей иерархии моделей

    self.calcViewMatrix()

    pbr_mat = FLOAT.new_array(16)
    setIdentityM(pbr_mat, 0)
    self.rbxPBRmodel.recalc(pbr_mat)

  def onSurfaceChanged(self, gl10, width, height):
    print("📽️ onSurfaceChanged", gl10, width, height)
    if width == self.W and height == self.H: return

    glViewport(0, 0, width, height)
    self.W, self.H, self.WH_ratio = width, height, width / height

    perspectiveM(self.projectionM, 0, 90, self.WH_ratio, 0.01, 10000)
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

    for model in self.models: model.recalc(MVPmatrix)
    self.rbxModel.recalc(MVPmatrix)
    if self.character: self.character.recalc(MVPmatrix)
    self.SolarSystem.recalc(MVPmatrix)

  def calcViewMatrix(self):
    q = Quaternion.fromYPR(self.yaw, self.pitch, self.roll)
    q2 = q.conjugated()
    self.viewNotTranslatedM = mat = q2.toMatrix()

    translateM2(self.viewM, 0, mat, 0, -self.camX, -self.camY, -self.camZ)

    self.updMVP = True
    self.forward = q.rotatedVector(0, 0, -1)
    self.camMoveEvent()

  def eventHandler(self):
    td, event = self.td, self.eventN
    if event in (1, 2):
      self.moveTd += td
      if self.moveTd >= 1:
        self.moveTd2 = min(self.moveTd2 + td, 5)

      if event == 2: td = -td
      x, y, z = self.forward
      td *= 5
      td *= 3 ** self.moveTd2

      self.camX += x * td
      self.camY += y * td
      self.camZ += z * td
      self.calcViewMatrix()
    else:
      self.moveTd = 0
      self.moveTd2 = max(0, self.moveTd2 - td)

  def drawScene(self):
    # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)

    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)

    program = self.program
    #checkGLError() TODO
    #glUniform1i(program[2]["uTexture"], 0)
    #checkGLError()

    self.rbxModel.draw()

    self.pbr.draw(self.rbxPBRmodel)

    character = self.character
    if character:
      enableProgram(program.program)
      character.draw()

    skybox = self.currentSkybox
    if skybox is not None: skybox.draw()

    enableProgram(program.program)
    for model in self.models: model.draw()

    self.SolarSystem.draw()

    self.gridProgram.draw(self.WH_ratio, self.eventN)
    self.glyphs.draw(self.WH_ratio)

  def onDrawFrame(self, gl10):
    self.frames += 1
    T = time()
    self.td = T - self.time
    self.time = T
    #print("📽️ onDraw", gl)

    self.fps()
    self.eventHandler()
    if self.updMVP: self.calcMVPmatrix()

    try: character = self.character.model
    except AttributeError: character = None
    if character is not None:
      yaw, pitch, roll = character.YPR
      yaw = (yaw + 15 * self.td) % 360
      character.setRotation(yaw, pitch, roll)

    glBindFramebuffer(GL_FRAMEBUFFER, self.FBO[0])
    self.drawScene()
    glBindFramebuffer(GL_FRAMEBUFFER, 0)

    self.textureChain.postprocessing()
    #print("🫢", glGetError())

  def move(self, dx, dy):
    if not self.ready: return
    self.yaw -= dx * 0.5
    self.pitch = max(-90, min(self.pitch - dy * 0.5, 90))
    self.calcViewMatrix()

  def event(self, up, down, misc):
    self.eventN = up | down << 1 | misc << 2

  def getTByPosition(self, x, y):
    if not self.ready: return -1
    return self.gridProgram.checkPosition(x / self.W, y / self.H)

  def click(self, x, y, click_td):
    if not self.ready: return
    if click_td > 0.5: return
    t = self.getTByPosition(x, y)
    if t == 3:
      self.skyboxN = N = (self.skyboxN + 1) % len(self.skyboxes)
      self.currentSkybox = self.skyboxes[N]
    # print("🐾 click:", x, y, t)

  def restart(self):
    print2("~" * 53)
    self.ready = False
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
    renderer = myRenderer(activity, view)
    # renderer = gpuRenderer(activity, view)
    renderer2 = rm.renderer(renderer)
    print("V:", view)
    print("R:", renderer2)
    view._m_setEGLContextClientVersion(renderer.glVersion)
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
    T = time()
    if action in ACTION_DOWN:
      x, y, id = getX(actionN), getY(actionN), getPointerId(actionN)
      t = renderer.getTByPosition(x, y)
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
