if True: # __name__ == "__main__":
  from executor import main, load_codes # пока нереализован доступный всем способ компиляции БЕЗ доступа к компилятору (облачные технологии)
  import os
  load_codes(os.path.basename(__file__))
  main("pmy")
  exit()

###~~~### pmy

import myGL



def mainProgram():
  program = newProgram("""
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
""", ('vPosition', 'vColor', 'vUV'), ('uMVPMatrix', 'uTexture'))
  if type(program) is str:
    print("💥 shader program error:")
    print(program)
    exit()
  print("✅ OK shader program:", program)
  return program



def figures():
  buffers = INT.new_array(2)
  glGenBuffers(2, buffers, 0)
  VBO, IBO = buffers

  ratio = (2 ** 2 - 1) ** 0.5
  ratio2 = ratio * 0.6

  VBOdata = FloatBuffer((
      0,  ratio, 4, 1, 0, 0, 1, -1, -1,
     -2, -ratio, 4, 0, 1, 0, 1, -1, -1,
      2, -ratio, 4, 0, 0, 1, 1, -1, -1,
   -1.6,  ratio, 4, 1, 1, 0, 1, -1, -1,
   -1.2, ratio2, 4, 1, 0, 1, 1, -1, -1,
     -2, ratio2, 4, 0, 1, 1, 1, -1, -1,
   -1.2,  ratio, 4, 0, 0, 0, 0, -1, -1,
     -1, -1, -1,    1, 1, 1, 1, -1, -1, #  7
      1, -1, -1,    1, 0, 0, 1, -1, -1, #  8
      1, -1,  1,    1, 1, 0, 1, -1, -1, #  9
     -1, -1,  1,    0, 0, 1, 1, -1, -1, # 10
     -1,  1, -1,    0, 1, 0, 1, -1, -1, # 11
      1,  1, -1,    0, 1, 1, 1, -1, -1, # 12
      1,  1,  1,    0, 0, 0, 0, -1, -1, # 13
     -1,  1,  1,    1, 0, 1, 1, -1, -1, # 14
     -1, -1, -1,    1, 1, 1, 1,  1, 2/8, # 15
      1, -1, -1,    1, 0, 0, 1,  0, 2/8, # 16
     -1,  1, -1,    0, 1, 0, 1,  1, 1/8, # 17
      1,  1, -1,    0, 1, 1, 1,  0, 1/8, # 18
  )) # 3d-координаты и раскраска вершин
  IBOdata = IntBuffer((
     0,  1,  2,  5,  4,  3, 0, 4, 6, # старые 3 треугольника
     7,  8,  9,  7,  9, 10, # дно куба
   # 7,  8, 11,  8, 11, 12, # фронт
    15, 16, 17, 16, 17, 18, # фронт
     8,  9, 12,  9, 12, 13, # правый бок
     9, 10, 14,  9, 13, 14, # тыл
    10,  7, 14,  7, 14, 11, # левый бок
    11, 12, 14, 12, 14, 13, # верх куба
  )) # сами полигоны = сетка, 2d-UV вершин

  glBindBuffer(GL_ARRAY_BUFFER, VBO)
  glBufferData(GL_ARRAY_BUFFER, VBOdata.capacity() * 4, VBOdata.fb, GL_STATIC_DRAW)
  glBindBuffer(GL_ARRAY_BUFFER, 0)

  glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, IBO)
  glBufferData(GL_ELEMENT_ARRAY_BUFFER, IBOdata.capacity() * 4, IBOdata.fb, GL_STATIC_DRAW)
  glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

  print("✅ OK buffers:", VBO, IBO)
  return VBO, IBO, IBOdata.capacity()

  """
  Бортанули нас с этими списками отображения: в OpenGL ES их неть

  gl._m_glBegin(GL_TRIANGLE_STRIP)
  glVertex3f = gl._mw_glVertex3f(float, float, float)
  glVertex3f(-1, -1, 0)
  glVertex3f( 1, -1, 0)
  glVertex3f( 1,  1, 0)
  glVertex3f(-1,  1, 0)
  gl._m_glEnd()
  """





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
    glUseProgram(program)
    #glUniform4f(uniforms["vColor"], 0, 0, 1, 1)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_DEPTH_TEST)

    self.modelM = modelM = FLOAT.new_array(16)
    self.viewM = FLOAT.new_array(16)
    self.projectionM = FLOAT.new_array(16)
    self.MVPmatrix = FLOAT.new_array(16)

    setIdentityM(modelM, 0)
    self.calcViewMatrix()

    textures = rm.get("drawable/textures")
    textureId = newTexture(ctxResources, textures)
    print("textures:", hex(textures), textureId)
      
    glUniform1i(uniforms["uTexture"], 0);
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, textureId)

  def onSurfaceChanged(self, gl10, width, height):
    print("📽️ onSurfaceChanged", gl10, width, height)
    glViewport(0, 0, width, height)
    self.W, self.H, self.WH_ratio = width, height, width / height
    self.buffers = figures()

    perspectiveM(self.projectionM, 0, 90, self.WH_ratio, 0.01, 1000)
    self.calcMVPmatrix()

  def calcMVPmatrix(self):
    MVPmatrix = self.MVPmatrix
    multiplyMM(MVPmatrix, 0, self.projectionM, 0, self.viewM, 0)
    multiplyMM(MVPmatrix, 0, MVPmatrix, 0, self.modelM, 0)
    # print("MVP:", self.MVPmatrix[:])
    uniforms = self.program[2]
    glUniformMatrix4fv(uniforms["uMVPMatrix"], 1, False, MVPmatrix, 0)
    self.updMVP = True

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

    program, attribs, uniforms = self.program
    vPosition = attribs["vPosition"]
    vColor    = attribs["vColor"]
    vUV       = attribs["vUV"]
    VBO, IBO, indexes = self.buffers

    glEnableVertexAttribArray(vPosition)
    glEnableVertexAttribArray(vColor)
    glEnableVertexAttribArray(vUV)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, IBO)

    glVertexAttribPointer(vPosition, 3, GL_FLOAT, False, 9 * 4, 0)
    glVertexAttribPointer(vColor,    4, GL_FLOAT, False, 9 * 4, 3 * 4)
    glVertexAttribPointer(vUV,       2, GL_FLOAT, False, 9 * 4, 7 * 4)
    glDrawElements(GL_TRIANGLES, indexes, GL_UNSIGNED_INT, 0)
    self.fps()

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
    glDisableVertexAttribArray(vPosition)
    glDisableVertexAttribArray(vColor)
    glDisableVertexAttribArray(vUV)

  def move(self, dx, dy):
    self.yaw -= dx * 0.5
    self.pitch = max(-89, min(self.pitch - dy * 0.5, 89))
    self.calcViewMatrix()

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
    if action == ACTION_DOWN:
      x, y = e._m_getX(), e._m_getY()
      self.prevX, self.prevY = x, y
    elif action == ACTION_MOVE:
      x, y = e._m_getX(), e._m_getY()
      self.renderer.move(x - self.prevX, y - self.prevY)
      self.prevX, self.prevY = x, y
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
