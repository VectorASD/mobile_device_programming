if True: # __name__ == "__main__":
  from executor import main, load_codes # пока нереализован доступный всем способ компиляции БЕЗ доступа к компилятору (облачные технологии)
  import os
  load_codes(os.path.split(__file__)[-1])
  main("pmy")
  exit()

###~~~### pmy

from int import INT
from float import FLOAT 
from double import DOUBLE

from android.content.Context import Context
from android.view.View import View
from android.view.Window import Window
from android.view.WindowManager_._LayoutParams import WindowManagerLayoutParams
from android.view.MotionEvent import MotionEvent
from android.opengl.GLSurfaceView import GLSurfaceView
from android.opengl.GLES20 import GLES20
from android.opengl.Matrix import Matrix
from java.nio.Buffer import NIOBuffer
from java.nio.ByteBuffer import jByteBuffer
from java.nio.ByteOrder import ByteOrder
from java.lang.Math import Math
from android.graphics.BitmapFactory import BitmapFactory
from android.graphics.BitmapFactory_._Options import BitmapFactoryOptions

INTarr = ()._a_int # INT.new_array(0)
FLOATarr = ()._a_float

#print(INT.new_array(10)[:])
#print(INT.new_array(10, 12)[:])
#exit()



ACTIVITY_SERVICE = Context._f_ACTIVITY_SERVICE
FEATURE_NO_TITLE = Window._f_FEATURE_NO_TITLE
FLAG_FULLSCREEN = WindowManagerLayoutParams._f_FLAG_FULLSCREEN
ACTION_DOWN = MotionEvent._f_ACTION_DOWN
ACTION_MOVE = MotionEvent._f_ACTION_MOVE
ACTION_UP = MotionEvent._f_ACTION_UP

#for f in GLES20.fields(): print(f)
#GL_QUAD_STRIP = GL10._f_GL_QUAD_STRIP
GL_TRIANGLES = GLES20._f_GL_TRIANGLES
GL_TRIANGLE_STRIP = GLES20._f_GL_TRIANGLE_STRIP
GL_TRIANGLE_FAN = GLES20._f_GL_TRIANGLE_FAN

GL_COLOR_BUFFER_BIT = GLES20._f_GL_COLOR_BUFFER_BIT
GL_DEPTH_BUFFER_BIT = GLES20._f_GL_DEPTH_BUFFER_BIT

GL_VERTEX_SHADER = GLES20._f_GL_VERTEX_SHADER
GL_FRAGMENT_SHADER = GLES20._f_GL_FRAGMENT_SHADER

GL_COMPILE_STATUS = GLES20._f_GL_COMPILE_STATUS
GL_LINK_STATUS = GLES20._f_GL_LINK_STATUS

GL_FALSE = GLES20._f_GL_FALSE
GL_TRUE = GLES20._f_GL_TRUE
GL_NO_ERROR = GLES20._f_GL_NO_ERROR
GL_FLOAT = GLES20._f_GL_FLOAT
GL_UNSIGNED_BYTE = GLES20._f_GL_UNSIGNED_BYTE
GL_UNSIGNED_INT = GLES20._f_GL_UNSIGNED_INT
GL_RGBA = GLES20._f_GL_RGBA

GL_ARRAY_BUFFER = GLES20._f_GL_ARRAY_BUFFER
GL_ELEMENT_ARRAY_BUFFER = GLES20._f_GL_ELEMENT_ARRAY_BUFFER
GL_STATIC_DRAW = GLES20._f_GL_STATIC_DRAW



sin = Math._mw_sin(DOUBLE)
cos = Math._mw_cos(DOUBLE)
PI = Math._f_PI
PI180 = PI / 180

glClearColor = GLES20._mw_glClearColor(FLOAT, FLOAT, FLOAT, FLOAT)
glViewport = GLES20._mw_glViewport(INT, INT, INT, INT)
glClear = GLES20._mw_glClear(INT)

glCreateShader = GLES20._mw_glCreateShader(INT)
glShaderSource = GLES20._mw_glShaderSource(INT, str)
glCompileShader = GLES20._mw_glCompileShader(INT)
glGetShaderiv = GLES20._mw_glGetShaderiv(INT, INT, INTarr, INT)
glGetShaderInfoLog = GLES20._mw_glGetShaderInfoLog(INT)
glDeleteShader = GLES20._mw_glDeleteShader(INT)

glCreateProgram = GLES20._mw_glCreateProgram()
glAttachShader = GLES20._mw_glAttachShader(INT, INT)
glLinkProgram = GLES20._mw_glLinkProgram(INT)
glGetProgramiv = GLES20._mw_glGetProgramiv(INT, INT, INTarr, INT)
glGetProgramInfoLog = GLES20._mw_glGetProgramInfoLog(INT)
glDeleteProgram = GLES20._mw_glDeleteProgram(INT)

glGetAttribLocation = GLES20._mw_glGetAttribLocation(int, str) # program, name
glGetUniformLocation = GLES20._mw_glGetUniformLocation(int, str) # program, name
glGetError = GLES20._mw_glGetError()
glUniform1i = GLES20._mw_glUniform1i(int, int) # location, x
glUniform4f = GLES20._mw_glUniform4f(int, float, float, float, float) # location, x, y, z, w
glUniformMatrix4fv = GLES20._mw_glUniformMatrix4fv(int, int, bool, FLOATarr, int) # location, count, transpose, value, offset

glGenBuffers = GLES20._mw_glGenBuffers(INT, INTarr, INT) # n, buffers, offset
glGenTextures = GLES20._mw_glGenTextures(INT, INTarr, INT) # n, textures, offset

glBindBuffer = GLES20._mw_glBindBuffer(INT, INT) # target, buffer
glBufferData = GLES20._mw_glBufferData(INT, INT, NIOBuffer, INT) # target, size, data, usage

glUseProgram = GLES20._mw_glUseProgram(INT) # program
glEnableVertexAttribArray = GLES20._mw_glEnableVertexAttribArray(int) # location
glDisableVertexAttribArray = GLES20._mw_glEnableVertexAttribArray(int) # location
glVertexAttribPointer = GLES20._mw_glVertexAttribPointer(int, int, int, bool, int, int) # location, size, type, normalized, stride, offset
glDrawElements = GLES20._mw_glDrawElements(int, int, int, int) # mode, count, type, offset

glEnable = GLES20._mw_glEnable(int) # cap
glDisable = GLES20._mw_glDisable(int) # cap
GL_BLEND = GLES20._f_GL_BLEND
GL_DEPTH_TEST = GLES20._f_GL_DEPTH_TEST

glBlendFunc = GLES20._mw_glBlendFunc(int, int) # src factor, dst factor
GL_SRC_ALPHA = GLES20._f_GL_SRC_ALPHA
GL_ONE_MINUS_SRC_ALPHA = GLES20._f_GL_ONE_MINUS_SRC_ALPHA

perspectiveM = Matrix._mw_perspectiveM(FLOATarr, int, float, float, float, float) # m, offset, fovy, aspect, zNear, zFar
setLookAtM = Matrix._mw_setLookAtM(FLOATarr, int, float, float, float, float, float, float, float, float, float) # rm, rmOffset, eyeX, eyeY, eyeZ, centerX, centerY, centerZ, upX, upY, upZ
setIdentityM = Matrix._mw_setIdentityM(FLOATarr, int) # sm, smOffset
multiplyMM = Matrix._mw_multiplyMM(FLOATarr, int, FLOATarr, int, FLOATarr, int) # result, resultOffset, lhs, lhsOffset, rhs, rhsOffset



class MyBuffer:
  allocate = jByteBuffer._mw_allocate(int)
  allocateDirect = jByteBuffer._mw_allocateDirect(int)
  nativeOrder = ByteOrder._m_nativeOrder()
  def __init__(self, isFloat, data = (), isArr = False):
    bb = MyBuffer.allocateDirect(len(data) * 4)
    bb._m_order(MyBuffer.nativeOrder)
    fb = bb._m_asFloatBuffer() if isFloat else bb._m_asIntBuffer()

    self.put = put = fb._mw_put(FLOATarr if isFloat else INTarr)
    self.getPos = fb._mw_position()
    self.setPos = pos = fb._mw_position(INT)
    self.capacity = fb._mw_capacity()
    self.fb = fb # float buffer (либо int buffer)

    if isArr: put(data)
    else: put(data._a_float if isFloat else data._a_int)
    #print("pos:", self.getPos()) и есть len(data)
    pos(0)

def FloatBuffer(data = (), isArr = False): return MyBuffer(True, data, isArr)
def IntBuffer(data = (), isArr = False): return MyBuffer(False, data, isArr)

#print(FloatBuffer().capacity()) # -> 0
#print(FloatBuffer((0, .5, 0)).capacity()) # -> 3
#print(IntBuffer().capacity()) # -> 0
#print(IntBuffer((0, 0, 0)).capacity()) # -> 3
#exit()



def newShader(type, code):
  shader = glCreateShader(type)
  glShaderSource(shader, code)
  glCompileShader(shader)
  arr = INT.new_array(1)
  glGetShaderiv(shader, GL_COMPILE_STATUS, arr, 0)
  if arr[0] == GL_FALSE:
    err = glGetShaderInfoLog(shader)
    glDeleteShader(shader)
    shader = err
  return shader

def newProgram(vCode, fCode, attribs, uniforms):
  vShader = newShader(GL_VERTEX_SHADER, vCode)
  if type(vShader) is str: return "Ошибка компиляции V-шейдера: " + vShader

  fShader = newShader(GL_FRAGMENT_SHADER, fCode)
  if type(fShader) is str: return "Ошибка компиляции F-шейдера: " + fShader

  program = glCreateProgram()
  glAttachShader(program, vShader)
  glAttachShader(program, fShader)
  glLinkProgram(program)
  arr = INT.new_array(1)
  glGetProgramiv(program, GL_LINK_STATUS, arr, 0)
  if arr[0] == GL_FALSE:
    err = glGetProgramInfoLog(program)
    glDeleteProgram(program)
    return err

  glDeleteShader(vShader)
  glDeleteShader(fShader)

  attribLocs = {}
  for name in attribs:
    loc = glGetAttribLocation(program, name)
    error = glGetError()
    if error != GL_NO_ERROR:
      return "get attribute %r error: %s" % (name, error)
    if loc < 0:
      return "attribute %r not found: %s" % (name, loc)
    attribLocs[name] = loc

  uniformLocs = {}
  for name in uniforms:
    loc = glGetUniformLocation(program, name)
    error = glGetError()
    if error != GL_NO_ERROR:
      return "get uniform %r error: %s" % (name, error)
    if loc < 0:
      return "uniform %r not found: %s" % (name, loc)
    uniformLocs[name] = loc

  return program, attribLocs, uniformLocs

bitmapFactoryOptions = BitmapFactoryOptions()
bitmapFactoryOptions._f_inScaled = False # чтобы не раздувало
bitmapFactoryOptions._f_inDensity = 0 # чтобы не сглаживало (все 3 Density)
bitmapFactoryOptions._f_inScreenDensity = 0
bitmapFactoryOptions._f_inTargetDensity = 0

glBindTexture = GLES20._mw_glBindTexture(int, int)
glTexParameteri = GLES20._mw_glTexParameteri(int, int, int)
glTexImage2D = GLES20._mw_glTexImage2D(int, int, int, int, int, int, int, int, NIOBuffer) # target, level, internalformat, width, height, border, format, type, pixels
GL_TEXTURE_2D = GLES20._f_GL_TEXTURE_2D
GL_TEXTURE_MIN_FILTER = GLES20._f_GL_TEXTURE_MIN_FILTER
GL_TEXTURE_MAG_FILTER = GLES20._f_GL_TEXTURE_MAG_FILTER
GL_LINEAR = GLES20._f_GL_LINEAR

glActiveTexture = GLES20._mw_glActiveTexture(20) # texture
GL_TEXTURE0 = GLES20._f_GL_TEXTURE0

def newTexture(ctxResources, resId):
  bitmap = BitmapFactory._m_decodeResource(ctxResources, resId, bitmapFactoryOptions)
  W, H = bitmap._m_getWidth(), bitmap._m_getHeight()
  pixels = INT.new_array(W * H)
  bitmap._m_getPixels(pixels, 0, W, 0, 0, W, H) # pixels, offset, stride, x, y, width, height
  byteCount = bitmap._m_getByteCount()
  bitmap._m_recycle()
  buffer = IntBuffer(pixels, True)

  ids = INT.new_array(1)
  glGenTextures(1, ids, 0)
  textureId = ids[0]

  glBindTexture(GL_TEXTURE_2D, textureId)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
  glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, W, H, 0, GL_RGBA, GL_UNSIGNED_BYTE, buffer.fb)

  return textureId

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
  else gl_FragColor = texture2D(uTexture, vaUV);
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
  glVertex3f = gl._mw_glVertex3f(FLOAT, FLOAT, FLOAT)
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

def Activity():
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



  class handler:
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

  H = handler()
  ress.activity("layout/main", H)



Activity()