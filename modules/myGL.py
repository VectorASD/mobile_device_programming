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

glClearColor = GLES20._mw_glClearColor(float, float, float, float)
glViewport = GLES20._mw_glViewport(int, int, int, int)
glClear = GLES20._mw_glClear(int)

glCreateShader = GLES20._mw_glCreateShader(int)
glShaderSource = GLES20._mw_glShaderSource(int, str)
glCompileShader = GLES20._mw_glCompileShader(int)
glGetShaderiv = GLES20._mw_glGetShaderiv(int, int, INTarr, INT)
glGetShaderInfoLog = GLES20._mw_glGetShaderInfoLog(int)
glDeleteShader = GLES20._mw_glDeleteShader(int)

glCreateProgram = GLES20._mw_glCreateProgram()
glAttachShader = GLES20._mw_glAttachShader(int, int)
glLinkProgram = GLES20._mw_glLinkProgram(int)
glGetProgramiv = GLES20._mw_glGetProgramiv(int, int, INTarr, int)
glGetProgramInfoLog = GLES20._mw_glGetProgramInfoLog(int)
glDeleteProgram = GLES20._mw_glDeleteProgram(int)

glGetAttribLocation = GLES20._mw_glGetAttribLocation(int, str) # program, name
glGetUniformLocation = GLES20._mw_glGetUniformLocation(int, str) # program, name
glGetError = GLES20._mw_glGetError()
glUniform1i = GLES20._mw_glUniform1i(int, int) # location, x
glUniform4f = GLES20._mw_glUniform4f(int, float, float, float, float) # location, x, y, z, w
glUniformMatrix4fv = GLES20._mw_glUniformMatrix4fv(int, int, bool, FLOATarr, int) # location, count, transpose, value, offset

glGenBuffers = GLES20._mw_glGenBuffers(int, INTarr, int) # n, buffers, offset
glGenTextures = GLES20._mw_glGenTextures(int, INTarr, int) # n, textures, offset

glBindBuffer = GLES20._mw_glBindBuffer(int, int) # target, buffer
glBufferData = GLES20._mw_glBufferData(int, int, NIOBuffer, int) # target, size, data, usage

glUseProgram = GLES20._mw_glUseProgram(int) # program
glEnableVertexAttribArray = GLES20._mw_glEnableVertexAttribArray(int) # location
glDisableVertexAttribArray = GLES20._mw_glEnableVertexAttribArray(int) # location
glVertexAttribPointer = GLES20._mw_glVertexAttribPointer(int, int, int, bool, int, int) # location, size, type, normalized, stride, offset
glDrawElements = GLES20._mw_glDrawElements(int, int, int, int) # mode, count, type, offset

glEnable = GLES20._mw_glEnable(int) # cap
glDisable = GLES20._mw_glDisable(int) # cap
GL_BLEND = GLES20._f_GL_BLEND
GL_DEPTH_TEST = GLES20._f_GL_DEPTH_TEST
GL_CULL_FACE = GLES20._f_GL_CULL_FACE

glBlendFunc = GLES20._mw_glBlendFunc(int, int) # src factor, dst factor
GL_SRC_ALPHA = GLES20._f_GL_SRC_ALPHA
GL_ONE_MINUS_SRC_ALPHA = GLES20._f_GL_ONE_MINUS_SRC_ALPHA

perspectiveM = Matrix._mw_perspectiveM(FLOATarr, int, float, float, float, float) # m, offset, fovy, aspect, zNear, zFar
setLookAtM = Matrix._mw_setLookAtM(FLOATarr, int, float, float, float, float, float, float, float, float, float) # rm, rmOffset, eyeX, eyeY, eyeZ, centerX, centerY, centerZ, upX, upY, upZ
setIdentityM = Matrix._mw_setIdentityM(FLOATarr, int) # sm, smOffset
multiplyMM = Matrix._mw_multiplyMM(FLOATarr, int, FLOATarr, int, FLOATarr, int) # result, resultOffset, lhs, lhsOffset, rhs, rhsOffset

glBindTexture = GLES20._mw_glBindTexture(int, int)
glTexParameteri = GLES20._mw_glTexParameteri(int, int, int)
glTexImage2D = GLES20._mw_glTexImage2D(int, int, int, int, int, int, int, int, NIOBuffer) # target, level, internalformat, width, height, border, format, type, pixels
GL_TEXTURE_2D = GLES20._f_GL_TEXTURE_2D
GL_TEXTURE_MIN_FILTER = GLES20._f_GL_TEXTURE_MIN_FILTER
GL_TEXTURE_MAG_FILTER = GLES20._f_GL_TEXTURE_MAG_FILTER
GL_LINEAR = GLES20._f_GL_LINEAR

glActiveTexture = GLES20._mw_glActiveTexture(20) # texture
GL_TEXTURE0 = GLES20._f_GL_TEXTURE0



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
  glUseProgram(program)

  attribLocs = {}
  for name in attribs:
    loc = glGetAttribLocation(program, name)
    error = glGetError()
    if error != GL_NO_ERROR:
      return "get attribute %r error: %s" % (name, error)
    if loc < 0:
      return "attribute %r not found: %s" % (name, loc)
    attribLocs[name] = loc
    glEnableVertexAttribArray(loc)

  uniformLocs = {}
  for name in uniforms:
    loc = glGetUniformLocation(program, name)
    error = glGetError()
    if error != GL_NO_ERROR:
      return "get uniform %r error: %s" % (name, error)
    if loc < 0:
      return "uniform %r not found: %s" % (name, loc)
    uniformLocs[name] = loc

  # утерян смысл в следующих строках:
  #glEnableVertexAttribArray(vPosition)
  #glEnableVertexAttribArray(vColor)
  #glEnableVertexAttribArray(vUV)
  #...
  #glDisableVertexAttribArray(vPosition)
  #glDisableVertexAttribArray(vColor)
  #glDisableVertexAttribArray(vUV)

  return program, attribLocs, uniformLocs



bitmapFactoryOptions = BitmapFactoryOptions()
bitmapFactoryOptions._f_inScaled = False # чтобы не раздувало
bitmapFactoryOptions._f_inDensity = 0 # чтобы не сглаживало (все 3 Density)
bitmapFactoryOptions._f_inScreenDensity = 0
bitmapFactoryOptions._f_inTargetDensity = 0

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



class Model:
  vPosition = vColor = vUV = None
  def calcAttribs(attribs):
    Model.vPosition = attribs["vPosition"]
    Model.vColor    = attribs["vColor"]
    Model.vUV       = attribs["vUV"]

  def __init__(self, VBOdata, IBOdata):
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

    print("✅ OK buffers:", VBO, IBO)
    self.data = VBO, IBO, IBOdata.capacity()

  def draw(self):
    VBO, IBO, indexes = self.data

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, IBO)

    glVertexAttribPointer(Model.vPosition, 3, GL_FLOAT, False, 9 * 4, 0)
    glVertexAttribPointer(Model.vColor,    4, GL_FLOAT, False, 9 * 4, 3 * 4)
    glVertexAttribPointer(Model.vUV,       2, GL_FLOAT, False, 9 * 4, 7 * 4)

    glDrawElements(GL_TRIANGLES, indexes, GL_UNSIGNED_INT, 0)
    #glBindBuffer(GL_ARRAY_BUFFER, 0)
    #glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
