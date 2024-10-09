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
ACTION_DOWN = MotionEvent._f_ACTION_DOWN, MotionEvent._f_ACTION_POINTER_DOWN
ACTION_MOVE = MotionEvent._f_ACTION_MOVE
ACTION_UP = MotionEvent._f_ACTION_UP, MotionEvent._f_ACTION_POINTER_UP
ACTION_CANCEL = MotionEvent._f_ACTION_CANCEL

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
GL_RGB = GLES20._f_GL_RGB
GL_RGBA = GLES20._f_GL_RGBA
# GL_DEPTH24_STENCIL8 = GLES20._f_GL_DEPTH24_STENCIL8 опять бортанули в этой OpenGL ES... зато появились следующие две строчки
GL_DEPTH_COMPONENT16 = GLES20._f_GL_DEPTH_COMPONENT16
GL_STENCIL_INDEX8 = GLES20._f_GL_STENCIL_INDEX8

GL_ARRAY_BUFFER = GLES20._f_GL_ARRAY_BUFFER
GL_ELEMENT_ARRAY_BUFFER = GLES20._f_GL_ELEMENT_ARRAY_BUFFER
GL_FRAMEBUFFER = GLES20._f_GL_FRAMEBUFFER
GL_RENDERBUFFER = GLES20._f_GL_RENDERBUFFER
GL_STATIC_DRAW = GLES20._f_GL_STATIC_DRAW



sin = Math._mw_sin(DOUBLE)
cos = Math._mw_cos(DOUBLE)
PI = Math._f_PI
PI180 = PI / 180

glClearColor = GLES20._mw_glClearColor(float, float, float, float)
glClear = GLES20._mw_glClear(int)
glViewport = GLES20._mw_glViewport(int, int, int, int)
glGetIntegerv = GLES20._mw_glGetIntegerv(int, INTarr, int) # pname, params, offset
GL_VIEWPORT = GLES20._f_GL_VIEWPORT

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
glUniform1f = GLES20._mw_glUniform1f(int, float) # location, x
glUniform2f = GLES20._mw_glUniform2f(int, float, float) # location, x, y
glUniform3f = GLES20._mw_glUniform3f(int, float, float, float) # location, x, y, z
glUniform4f = GLES20._mw_glUniform4f(int, float, float, float, float) # location, x, y, z, w
glUniformMatrix4fv = GLES20._mw_glUniformMatrix4fv(int, int, bool, FLOATarr, int) # location, count, transpose, value, offset

glBufferData = GLES20._mw_glBufferData(int, int, NIOBuffer, int) # target, size, data, usage

glGenBuffers = GLES20._mw_glGenBuffers(int, INTarr, int) # n, buffers, offset
glGenTextures = GLES20._mw_glGenTextures(int, INTarr, int) # n, textures, offset
glGenFramebuffers = GLES20._mw_glGenFramebuffers(int, INTarr, int) # n, framebuffers, offset
glGenRenderbuffers = GLES20._mw_glGenRenderbuffers(int, INTarr, int) # n, renderbuffers, offset

glBindBuffer = GLES20._mw_glBindBuffer(int, int) # target, buffer
glBindTexture = GLES20._mw_glBindTexture(int, int) # target, texture
glBindFramebuffer = GLES20._mw_glBindFramebuffer(int, int) # target, framebuffer
glBindRenderbuffer = GLES20._mw_glBindRenderbuffer(int, int) # target, framebuffer

glDeleteBuffers = GLES20._mw_glDeleteBuffers(int, INTarr, int) # n, buffers, offset
glDeleteTextures = GLES20._mw_glDeleteTextures(int, INTarr, int) # n, textures, offset
glDeleteFramebuffers = GLES20._mw_glDeleteFramebuffers(int, INTarr, int) # n, framebuffers, offset
glDeleteRenderbuffers = GLES20._mw_glDeleteRenderbuffers(int, INTarr, int) # n, renderbuffers, offset

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
multiplyMV = Matrix._mw_multiplyMV(FLOATarr, int, FLOATarr, int, FLOATarr, int) # resultVec, resultVecOffset, lhsMat, lhsMatOffset, rhsVec, rhsVecOffset
transposeM = Matrix._mw_transposeM(FLOATarr, int, FLOATarr, int) # mTrans, mTransOffset, m, mOffset
translateM = Matrix._mw_translateM(FLOATarr, int, float, float, float) # m, mOffset, x, y, z
translateM2 = Matrix._mw_translateM(FLOATarr, int, FLOATarr, int, float, float, float) # tm, tmOffset, m, mOffset, x, y, z

glTexImage2D = GLES20._mw_glTexImage2D(int, int, int, int, int, int, int, int, NIOBuffer) # target, level, internalformat, width, height, border, format, type, pixels
glReadPixels = GLES20._mw_glReadPixels(int, int, int, int, int, int, NIOBuffer) # x, y, width, height, format, type, pixels
glTexParameterf = GLES20._mw_glTexParameterf(int, int, float) # target, pname, param
glTexParameterfv = GLES20._mw_glTexParameterfv(int, int, FLOATarr, int) # target, pname, params, offset
glTexParameteri = GLES20._mw_glTexParameteri(int, int, int)
glTexParameteriv = GLES20._mw_glTexParameteriv(int, int, INTarr, int) # target, pname, params, offset
GL_TEXTURE_2D = GLES20._f_GL_TEXTURE_2D
GL_TEXTURE_CUBE_MAP = GLES20._f_GL_TEXTURE_CUBE_MAP
GL_TEXTURE_CUBE_MAP_TARGETS = GLES20._f_GL_TEXTURE_CUBE_MAP_POSITIVE_X, GLES20._f_GL_TEXTURE_CUBE_MAP_NEGATIVE_X, GLES20._f_GL_TEXTURE_CUBE_MAP_POSITIVE_Y, GLES20._f_GL_TEXTURE_CUBE_MAP_NEGATIVE_Y, GLES20._f_GL_TEXTURE_CUBE_MAP_POSITIVE_Z, GLES20._f_GL_TEXTURE_CUBE_MAP_NEGATIVE_Z
GL_TEXTURE_MIN_FILTER = GLES20._f_GL_TEXTURE_MIN_FILTER
GL_TEXTURE_MAG_FILTER = GLES20._f_GL_TEXTURE_MAG_FILTER
GL_TEXTURE_WRAP_S = GLES20._f_GL_TEXTURE_WRAP_S
GL_TEXTURE_WRAP_T = GLES20._f_GL_TEXTURE_WRAP_T
# GL_TEXTURE_WRAP_R = GLES20._f_GL_TEXTURE_WRAP_R опять OpenGL ES...
GL_NEAREST = GLES20._f_GL_NEAREST # фильтр ближайшено соседа, как в майнкрафте, как нам и надо ;"-}
GL_LINEAR = GLES20._f_GL_LINEAR # линейная фильтрация (мыло)
GL_NEAREST_MIPMAP_NEAREST = GLES20._f_GL_NEAREST_MIPMAP_NEAREST
GL_LINEAR_MIPMAP_NEAREST = GLES20._f_GL_LINEAR_MIPMAP_NEAREST
GL_NEAREST_MIPMAP_LINEAR = GLES20._f_GL_NEAREST_MIPMAP_LINEAR
GL_REPEAT = GLES20._f_GL_REPEAT
GL_MIRRORED_REPEAT = GLES20._f_GL_MIRRORED_REPEAT
GL_CLAMP_TO_EDGE = GLES20._f_GL_CLAMP_TO_EDGE
# GL_CLAMP_TO_BORDER = GLES20._f_GL_CLAMP_TO_BORDER опять OpenGL ES...
# GL_TEXTURE_BORDER_COLOR = GLES20._f_GL_TEXTURE_BORDER_COLOR без опции из предыдущей строки эта опция теряет смысл существования, потому её и нет в OpenGL ES

glActiveTexture = GLES20._mw_glActiveTexture(20) # texture
GL_TEXTURE0 = GLES20._f_GL_TEXTURE0

glFramebufferTexture2D = GLES20._mw_glFramebufferTexture2D(int, int, int, int, int) # target, attachment, textarget, texture, level
glFramebufferRenderbuffer = GLES20._mw_glFramebufferRenderbuffer(int, int, int, int) # target, attachment, renderbuffertarget, renderbuffer
glCheckFramebufferStatus = GLES20._mw_glCheckFramebufferStatus(int) # target
glRenderbufferStorage = GLES20._mw_glRenderbufferStorage(int, int, int, int) # target, internalformat, width, height
GL_FRAMEBUFFER_COMPLETE = GLES20._f_GL_FRAMEBUFFER_COMPLETE
GL_COLOR_ATTACHMENT0 = GLES20._f_GL_COLOR_ATTACHMENT0
# GL_DEPTH_STENCIL_ATTACHMENT = GLES20._f_GL_DEPTH_STENCIL_ATTACHMENT
GL_DEPTH_ATTACHMENT = GLES20._f_GL_DEPTH_ATTACHMENT
GL_STENCIL_ATTACHMENT = GLES20._f_GL_STENCIL_ATTACHMENT



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
    self.clear = fb._mw_clear()

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

  print2("✅ OK shaders:", vShader, fShader)

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

def checkProgram(program):
  if type(program) is str:
    print2("💥 shader program error:")
    print(program)
  print2("✅ OK shader program:", program)
  return program

prevLocs = None
def enableProgram(program):
  global prevLocs
  program, attribs, uniforms = program
  locs = tuple(attribs.values())
  if prevLocs is not None:
    for loc in prevLocs: glDisableVertexAttribArray(loc)
  glUseProgram(program)
  for loc in locs: glEnableVertexAttribArray(loc)
  prevLocs = locs

  # утерян смысл в следующих строках:
  #glEnableVertexAttribArray(vPosition)
  #glEnableVertexAttribArray(vColor)
  #glEnableVertexAttribArray(vUV)
  #...
  #glDisableVertexAttribArray(vPosition)
  #glDisableVertexAttribArray(vColor)
  #glDisableVertexAttribArray(vUV)



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
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
  glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, W, H, 0, GL_RGBA, GL_UNSIGNED_BYTE, buffer.fb)
  buffer.clear()
  glBindTexture(GL_TEXTURE_2D, 0)

  print2("✅ OK texture:", textureId)
  return textureId



GLES20_fields = GLES20.fields()
GL_errors = {}
for k, v in GLES20_fields.items():
  try: GL_errors[v] += "|" + k
  except KeyError: GL_errors[v] = k
# GL_errors[0] = "ZERO_ERROR"

def checkGLError():
  err = glGetError()
  if err != GL_NO_ERROR: print2("🔥 glError:", err, "(%s)" % GL_errors[err])
  else: print2("gl ok")

def checkFrameBuffer():
  status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
  if status != GL_FRAMEBUFFER_COMPLETE:
    print2("💥 FBO error:", status, "(%s)" % GL_errors[status])
  else: print2("✅ FBO ok")

def newFrameBuffer(width, height, depthTest = True):
  arr = INT.new_array(3)
  glGenFramebuffers(1, arr, 0)
  glGenTextures(1, arr, 1)
  if depthTest: glGenRenderbuffers(1, arr, 2)
  # glGenRenderbuffers(1, arr, 3)
  fbo, textureId, rbo = arr

  glBindFramebuffer(GL_FRAMEBUFFER, fbo)

  glBindTexture(GL_TEXTURE_2D, textureId)
  glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
  glBindTexture(GL_TEXTURE_2D, 0)

  if depthTest:
    glBindRenderbuffer(GL_RENDERBUFFER, rbo)
    glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT16, width, height)

  # glBindRenderbuffer(GL_RENDERBUFFER, rbo2)
  # glRenderbufferStorage(GL_RENDERBUFFER, GL_STENCIL_INDEX8, width, height)
  # glBindRenderbuffer(GL_RENDERBUFFER, 0)

  # checkFrameBuffer() нет аттачментов
  glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, textureId, 0)
  # checkFrameBuffer() ok
  if depthTest: glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, rbo)
  # checkFrameBuffer() ok
  # трафарет (при том не нужный мне 🗿) отваливается с ошибкой GL_FRAMEBUFFER_UNSUPPORTED
  #glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_STENCIL_ATTACHMENT, GL_RENDERBUFFER, rbo2)
  checkFrameBuffer()
 
  print2("🥳 FBO:", fbo, textureId, rbo if depthTest else "x")

  glBindFramebuffer(GL_FRAMEBUFFER, 0)
  return arr

def deleteFrameBuffer(arr):
  fbo, textureId, rbo = arr
  depthTest = rbo > 0
  glDeleteFramebuffers(1, arr, 0)
  glDeleteTextures(1, arr, 1)
  if depthTest: glDeleteRenderbuffers(1, arr, 2)
  print2("♻️ FBO:", fbo, textureId, rbo if depthTest else "x")
