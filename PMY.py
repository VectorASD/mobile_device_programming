if True: # __name__ == "__main__":
  from executor import main, load_codes # пока нереализован доступный всем способ компиляции БЕЗ доступа к компилятору (облачные технологии)
  import os
  load_codes(os.path.basename(__file__))
  main("pmy")
  exit()

###~~~### pmy

import myGL



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
  else gl_FragColor = texture2D(uTexture, vaUV).bgra;
}
""", ('vPosition', 'vColor', 'vUV'), ('uMVPMatrix', 'uTexture')))



class d2textureProgram():
  def __init__(self):
    self.program = program = checkProgram(newProgram("""
attribute vec2 vPosition;
attribute vec2 vUV;
attribute float vType;

uniform float uAspect;

varying vec2 vaUV;
varying float vaType;

void main() {
  gl_Position = vec4(vPosition.x, vPosition.y * uAspect - uAspect, 1, 1);
  vaUV = vUV;
  vaType = vType;
}
    """, """
precision mediump float;

varying vec2 vaUV;
varying float vaType;

uniform sampler2D uTexture;
uniform int uEvent;

void main() {
	 int b2 = uEvent / 2;
	 int b1 = uEvent - b2 * 2;
	 float X = 1.;
  if (vaType == 1. && b1 > 0 || vaType == 2. && b2 > 0) X = 0.5;
  vec4 clr = texture2D(uTexture, vaUV).bgra;
  gl_FragColor = vec4(clr.rgb * X, clr.a);
}
    """, ('vPosition', 'vUV', 'vType'), ('uTexture', 'uAspect', 'uEvent')))
    uniforms = program[2]
    self.uTexture = uniforms["uTexture"]
    self.uAspect = uniforms["uAspect"]
    self.uEvent = uniforms["uEvent"]
    self.models = []
    self.add(160, 0.25, 5.5, 8, 1)
    self.add(142, 0.25, 6.75, 8, 2)

  def add(self, id, posX, posY, L = 10, t = 0):
    L //= 2
    L1 = L - 1
    pLx, pRx, pLy, pRy = (posX - L) / L, (posX - L1) / L, (posY - L) / -L, (posY - L1) / -L
    y, x = divmod(id, 8)
    Lx, Rx, Ly, Ry = x / 8, (x + 1) / 8, y / 64, (y + 1) / 64
    model = Model((
      pLx, pLy, Lx, Ly, t,
      pRx, pLy, Rx, Ly, t,
      pRx, pRy, Rx, Ry, t,
      pLx, pRy, Lx, Ry, t,
    ), (
      0, 1, 2, 0, 2, 3,
    ))
    self.models.append(model)

  def draw(self, aspect, eventN):
    def func():
      glVertexAttribPointer(vPosition, 2, GL_FLOAT, False, 5 * 4, 0)
      glVertexAttribPointer(vUV,       2, GL_FLOAT, False, 5 * 4, 2 * 4)
      glVertexAttribPointer(vType,     1, GL_FLOAT, False, 5 * 4, 4 * 4)
    enableProgram(self.program)
    attribs = self.program[1]
    vPosition, vUV, vType = attribs["vPosition"], attribs["vUV"], attribs["vType"]
    glUniform1f(self.uAspect, aspect)
    glUniform1i(self.uEvent, eventN)
    for model in self.models: model.draw(func)



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
    -1, -1, -1,   1, 1, 1, 1,    1, 2/8, # 8
     1, -1, -1,   1, 0, 0, 1,    0, 2/8, # 9
    -1,  1, -1,   0, 1, 0, 1,    1, 1/8, # 10
     1,  1, -1,   0, 1, 1, 1,    0, 1/8, # 11
  ), (
     0,  1,  2,  0,  2,  3, # дно куба
   # 0,  1,  4,  1,  4,  5, # фронт
     8, 10,  9,  9, 10, 11, # фронт
     1,  5,  2,  2,  5,  6, # правый бок
     2,  7,  3,  2,  6,  7, # тыл
     3,  7,  0,  0,  7,  4, # левый бок
     4,  7,  5,  5,  7,  6, # верх куба
  ))

  return triangles, cube



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

class myRenderer:
  def __init__(self):
    self.frames = self.last_frames = 0
    self.last_time = time() + 0.1
    self.frame_pos = 0
    self.frame_arr = []
    self.fpsS = "?"
    self.yaw = self.pitch = self.roll = 0
    self.eventN = 0

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
    print("📽️ onSurfaceCreated", gl10, config)
    glClearColor(0.9, 0.95, 1, 0)
    self.program = program, attribs, uniforms = mainProgram()
    Model.calcAttribs(attribs)

    #glUniform4f(uniforms["vColor"], 0, 0, 1, 1)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    self.modelM = modelM = FLOAT.new_array(16)
    self.viewM = FLOAT.new_array(16)
    self.projectionM = FLOAT.new_array(16)
    self.MVPmatrix = FLOAT.new_array(16)

    setIdentityM(modelM, 0)
    self.calcViewMatrix()

    textures = rm.get("drawable/textures")
    textureId = newTexture(ctxResources, textures)
    print("textures:", hex(textures), textureId)

    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, textureId)

    self.program2 = prog2 = d2textureProgram()

    glUniform1i(uniforms["uTexture"], 0)
    glUniform1i(prog2.uTexture, 0)

  def onSurfaceChanged(self, gl10, width, height):
    print("📽️ onSurfaceChanged", gl10, width, height)
    glViewport(0, 0, width, height)
    self.WHAspect = self.W, self.H, self.WH_ratio = width, height, width / height
    self.models = figures()

    perspectiveM(self.projectionM, 0, 90, self.WH_ratio, 0.01, 1000)
    self.calcMVPmatrix()

  def calcMVPmatrix(self):
    MVPmatrix = self.MVPmatrix
    multiplyMM(MVPmatrix, 0, self.projectionM, 0, self.viewM, 0)
    multiplyMM(MVPmatrix, 0, MVPmatrix, 0, self.modelM, 0)
    # print("MVP:", self.MVPmatrix[:])
    self.updMVP = False

  def calcViewMatrix(self):
    viewM = self.viewM
    yaw = self.yaw * PI180
    pitch = self.pitch * PI180
    sYaw, cYaw = sin(yaw), cos(yaw)
    sPitch, cPitch = sin(pitch), cos(pitch)
    R = -3.5
    setLookAtM(viewM, 0,
      sYaw * cPitch * R, sPitch * R, cYaw * cPitch * R, # eye
      0, 0, 0, # center
      0, 1, 0, # up
    )
    self.updMVP = True

  def onDrawFrame(self, gl10):
    self.frames += 1
    #print("📽️ onDraw", gl)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    if self.updMVP: self.calcMVPmatrix()

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)

    program = self.program
    enableProgram(program)
    glUniformMatrix4fv(program[2]["uMVPMatrix"], 1, False, self.MVPmatrix, 0)

    for model in self.models: model.draw()

    glDisable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)
    self.program2.draw(self.WH_ratio, self.eventN)

    #self.fps()

  def move(self, dx, dy):
    self.yaw -= dx * 0.5
    self.pitch = max(-89, min(self.pitch - dy * 0.5, 89))
    self.calcViewMatrix()

  def event(self, up, down):
    self.eventN = up | down * 2

  reverse = {
    "cr": onSurfaceCreated,
    "ch": onSurfaceChanged,
    "df": onDrawFrame,
  }



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
    self.eventA = set()
    self.eventB = set()

    return True # lock setContentView

  def onStart(self): print("onStart")
  def onRestart(self): print("onRestart")
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
    prevXY, renderer = self.prevXY, self.renderer
    actionN = action >> 8
    action &= 255
    W32 = renderer.W / 32
    W5_5, W6 = W32 * 5.5, W32 * 6
    H8 = renderer.H - W5_5
    H8b = H8 - W5_5
    if action in ACTION_DOWN:
      x, y, id = getX(actionN), getY(actionN), getPointerId(actionN)
      if x < W6 and y > H8b:
        prevXY[id] = None
        if y > H8: self.eventB.add(id)
        else: self.eventA.add(id)
        renderer.event(bool(self.eventA), bool(self.eventB))
      else: prevXY[id] = x, y
    elif action == ACTION_MOVE:
      for p in range(e._m_getPointerCount()):
        x, y, id = getX(p), getY(p), getPointerId(p)
        prevv = prevXY[id]
        if prevv is None: continue
        prevX, prevY = prevv
        prevXY[id] = x, y
        self.renderer.move(x - prevX, y - prevY)
    elif action in ACTION_UP:
      id = getPointerId(actionN)
      prevXY[id] = 0, 0
      self.eventA.remove(id)
      self.eventB.remove(id)
      renderer.event(bool(self.eventA), bool(self.eventB))
      # del prevXY[id] :/
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
