if True: # __name__ == "__main__":
  from executor import main, load_codes # пока нереализован доступный всем способ компиляции БЕЗ доступа к компилятору (облачные технологии)
  load_codes("PMY.py")
  main("pmy")
  exit()

###~~~### pmy

from int import INT
from float import FLOAT 

from android.content.Context import Context
from android.view.View import View
from android.opengl.GLSurfaceView import GLSurfaceView
from android.view.Window import Window
from android.view.WindowManager_._LayoutParams import WindowManagerLayoutParams
from javax.microedition.khronos.opengles.GL10 import GL10
from android.opengl.GLES20 import GLES20
from java.nio.Buffer import NIOBuffer
from java.nio.ByteBuffer import jByteBuffer
from java.nio.ByteOrder import ByteOrder

INTarr = ()._a_int # INT.new_array(0)
FLOATarr = ()._a_float

#print(INT.new_array(10)[:])
#print(INT.new_array(10, 12)[:])
#exit()



ACTIVITY_SERVICE = Context._f_ACTIVITY_SERVICE
FEATURE_NO_TITLE = Window._f_FEATURE_NO_TITLE
FLAG_FULLSCREEN = WindowManagerLayoutParams._f_FLAG_FULLSCREEN

#for f in GLES20.fields(): print(f)
#GL_QUAD_STRIP = GL10._f_GL_QUAD_STRIP
GL_TRIANGLES = GLES20._f_GL_TRIANGLES
GL_TRIANGLE_STRIP = GLES20._f_GL_TRIANGLE_STRIP
GL_TRIANGLE_FAN = GLES20._f_GL_TRIANGLE_FAN

GL_COLOR_BUFFER_BIT = GLES20._f_GL_COLOR_BUFFER_BIT

GL_VERTEX_SHADER = GLES20._f_GL_VERTEX_SHADER
GL_FRAGMENT_SHADER = GLES20._f_GL_FRAGMENT_SHADER

GL_COMPILE_STATUS = GLES20._f_GL_COMPILE_STATUS
GL_LINK_STATUS = GLES20._f_GL_LINK_STATUS

GL_FALSE = GLES20._f_GL_FALSE
GL_TRUE = GLES20._f_GL_TRUE
GL_NO_ERROR = GLES20._f_GL_NO_ERROR
GL_FLOAT = GLES20._f_GL_FLOAT
GL_UNSIGNED_INT = GLES20._f_GL_UNSIGNED_INT

GL_ARRAY_BUFFER = GLES20._f_GL_ARRAY_BUFFER
GL_ELEMENT_ARRAY_BUFFER = GLES20._f_GL_ELEMENT_ARRAY_BUFFER
GL_STATIC_DRAW = GLES20._f_GL_STATIC_DRAW



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
glUniform4f = GLES20._mw_glUniform4f(int, float, float, float, float) # location, x, y, z, w

glGenBuffers = GLES20._mw_glGenBuffers(INT, INTarr, INT) # n, buffers, offset
glGenTextures = GLES20._mw_glGenTextures(INT, INTarr, INT) # n, textures, offset

glBindBuffer = GLES20._mw_glBindBuffer(INT, INT) # target, buffer
glBufferData = GLES20._mw_glBufferData(INT, INT, NIOBuffer, INT) # target, size, data, usage

glUseProgram = GLES20._mw_glUseProgram(INT) # program
glEnableVertexAttribArray = GLES20._mw_glEnableVertexAttribArray(int) # location
glDisableVertexAttribArray = GLES20._mw_glEnableVertexAttribArray(int) # location
glVertexAttribPointer = GLES20._mw_glVertexAttribPointer(int, int, int, bool, int, int) # location, size, type, normalized, stride, offset
glDrawElements = GLES20._mw_glDrawElements(int, int, int, int) # mode, count, type, offset



class MyBuffer:
  allocateDirect = jByteBuffer._mw_allocateDirect(INT)
  nativeOrder = ByteOrder._m_nativeOrder()
  def __init__(self, isFloat, data = ()):
    bb = MyBuffer.allocateDirect(len(data) * 4)
    bb._m_order(MyBuffer.nativeOrder)
    fb = bb._m_asFloatBuffer() if isFloat else bb._m_asIntBuffer()

    self.put = put = fb._mw_put(FLOATarr if isFloat else INTarr)
    self.getPos = fb._mw_position()
    self.setPos = pos = fb._mw_position(INT)
    self.capacity = fb._mw_capacity()
    self.fb = fb # float buffer (либо int buffer)

    put(data._a_float if isFloat else data._a_int)
    #print("pos:", self.getPos()) и есть len(data)
    pos(0)

def FloatBuffer(data = ()): return MyBuffer(True, data)
def IntBuffer(data = ()): return MyBuffer(False, data)

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

def mainProgram():
  program = newProgram("""
attribute vec4 vPosition;
void main() {
  gl_Position = vPosition;
}
""", """
precision mediump float;
uniform vec4 vColor;
void main() {
  gl_FragColor = vColor;
}
""", ('vPosition',), ('vColor',))
  if type(program) is str:
    print("shader program error:")
    print(program)
    exit()
  print("OK shader program:", program)
  return program

def triangle(ratio):
  buffers = INT.new_array(2)
  glGenBuffers(2, buffers, 0)
  VBO, IBO = buffers

  ratio *= (1 - 0.5 ** 2) ** 0.5
  ratio2 = ratio * 0.6

  VBOdata = FloatBuffer((
      0,  ratio, 0,
     -1, -ratio, 0,
      1, -ratio, 0,
    0.8,  ratio, 0,
    0.6, ratio2, 0,
      1, ratio2, 0,
    0.6,  ratio, 0,
  )) # в будущем это будут 3d-координаты, 3d-нормали и 2d-UV вершин
  IBOdata = IntBuffer((0, 1, 2, 5, 4, 3, 0, 4, 6)) # в будущем это будут сами полигоны = сетка

  glBindBuffer(GL_ARRAY_BUFFER, VBO)
  glBufferData(GL_ARRAY_BUFFER, VBOdata.capacity() * 4, VBOdata.fb, GL_STATIC_DRAW)
  glBindBuffer(GL_ARRAY_BUFFER, 0)

  glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, IBO)
  glBufferData(GL_ELEMENT_ARRAY_BUFFER, IBOdata.capacity() * 4, IBOdata.fb, GL_STATIC_DRAW)
  glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

  print("OK buffers:", VBO, IBO)
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
      self.frame_arr = None

    def fps(self):
      T = time()
      arr = self.frame_arr
      if T >= self.last_time:
        self.last_time = T + 0.1
        fd = self.frames - self.last_frames
        self.last_frames = self.frames
        self.frame_pos = pos = (self.frame_pos + 1) % 10
        if arr is None: self.frame_arr = arr = [fd] * 10
        else: arr[pos] = fd
      if arr is None: return "?"
      S = 0
      for i in arr: S += i
      return S

    def onSurfaceCreated(self, gl10, config):
      print("📽️ onSurfaceCreated", gl10, config)
      glClearColor(0.9, 0.95, 1, 0)
      self.program = program, attribs, uniforms = mainProgram()
      vColor = uniforms["vColor"]
      glUseProgram(program)
      glUniform4f(vColor, 0, 0, 1, 1)

    def onSurfaceChanged(self, gl10, width, height):
      print("📽️ onSurfaceChanged", gl10, width, height)
      glViewport(0, 0, width, height)
      self.W, self.H, self.WH_ratio = width, height, width / height
      self.buffers = triangle(self.WH_ratio)

    def onDrawFrame(self, gl10):
      self.frames += 1
      #print("📽️ onDraw", gl)
      glClear(GL_COLOR_BUFFER_BIT)

      program, attribs, uniforms = self.program
      vPosition = attribs["vPosition"]
      VBO, IBO, indexes = self.buffers

      glEnableVertexAttribArray(vPosition)
      glBindBuffer(GL_ARRAY_BUFFER, VBO)
      glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, IBO)

      glVertexAttribPointer(vPosition, 3, GL_FLOAT, False, 0, 0)
      glDrawElements(GL_TRIANGLES, indexes, GL_UNSIGNED_INT, 0)
      print(self.fps())

      glBindBuffer(GL_ARRAY_BUFFER, 0)
      glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
      glDisableVertexAttribArray(vPosition)

      

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
      renderer = rm.renderer(myRenderer())
      print("V:", view)
      print("R:", renderer)
      view._m_setEGLContextClientVersion(2)
      view._m_setRenderer(renderer)
      activity._mw_setContentView(View)(view)

      self.viewResume = view._mw_onResume()
      self.viewPause = view._mw_onPause()

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
      print("onTouchEvent", e)
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
  #print("•", rm)
  ress = rm.release()
  ctx = ress.ctx
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
