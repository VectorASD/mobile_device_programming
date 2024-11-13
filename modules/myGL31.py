from java.lang.String import STRING

import myGL

from android.opengl.GLES30 import GLES30
from android.opengl.GLES31 import GLES31 # до API 21 (Android 5.0 (LOLLIPOP)) не будет работать
#from android.opengl.GLES32 import GLES32 # до API 24 (Android 7.0 (N)) не будет работать
# всё обошлось без GLES32 ;"-}}}

STRarr = STRING.new_array(0)



GL_COMPUTE_SHADER = GLES31._f_GL_COMPUTE_SHADER # нет в GLES30

GL_MAX_COMPUTE_WORK_GROUP_COUNT = GLES31._f_GL_MAX_COMPUTE_WORK_GROUP_COUNT
GL_MAX_COMPUTE_WORK_GROUP_INVOCATIONS = GLES31._f_GL_MAX_COMPUTE_WORK_GROUP_INVOCATIONS
GL_MAX_COMPUTE_WORK_GROUP_SIZE = GLES31._f_GL_MAX_COMPUTE_WORK_GROUP_SIZE
GL_MAX_SHADER_STORAGE_BLOCK_SIZE = GLES31._f_GL_MAX_SHADER_STORAGE_BLOCK_SIZE

GL_MAP_READ_BIT = GLES30._f_GL_MAP_READ_BIT

GL_SHADER_STORAGE_BARRIER_BIT = GLES31._f_GL_SHADER_STORAGE_BARRIER_BIT
GL_SHADER_STORAGE_BUFFER = GLES31._f_GL_SHADER_STORAGE_BUFFER

#GL_STREAM_COPY = GLES30._f_GL_STREAM_COPY
GL_DYNAMIC_READ = GLES30._f_GL_DYNAMIC_READ
GL_READ_ONLY = GLES31._f_GL_READ_ONLY
#GL_WRITE_ONLY = GLES31._f_GL_WRITE_ONLY


glDispatchCompute = GLES31._mw_glDispatchCompute(int, int, int) # num_groups_x, num_groups_y, num_groups_z
glMemoryBarrier = GLES31._mw_glMemoryBarrier(int)

glMapBufferRange = GLES30._mw_glMapBufferRange(int, int, int, int) # target, offset, length, access
glUnmapBuffer = GLES30._mw_glUnmapBuffer(int) # target

glBindBufferBase = GLES30._mw_glBindBufferBase(int, int, int) # target, index, buffer

glGetIntegeri_v = GLES30._mw_glGetIntegeri_v(int, int, INTarr, int) # target, index, data, offset



def newProgram31(cCode):
  cShader = newShader(GL_COMPUTE_SHADER, cCode)
  if type(cShader) is str: return "Ошибка компиляции C-шейдера: " + cShader

  print2("✅ OK shaders:", cShader)

  program = glCreateProgram()
  glAttachShader(program, cShader)
  glLinkProgram(program)
  arr = INT.new_array(1)
  glGetProgramiv(program, GL_LINK_STATUS, arr, 0)
  if arr[0] == GL_FALSE:
    err = glGetProgramInfoLog(program)
    glDeleteProgram(program)
    return err

  glDeleteShader(cShader)
  return (program,) # всё для checkProgram



def newSSBOs(size, size2):
  ids = INT.new_array(2)
  glGenBuffers(2, ids, 0)
  dataBuffer, outputBuffer = ids

  glBindBuffer(GL_SHADER_STORAGE_BUFFER, dataBuffer)
  glBufferData(GL_SHADER_STORAGE_BUFFER, size, None, GL_STATIC_DRAW)
  checkGLError()
  glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 0, dataBuffer)

  glBindBuffer(GL_SHADER_STORAGE_BUFFER, outputBuffer)
  glBufferData(GL_SHADER_STORAGE_BUFFER, size2, None, GL_STATIC_DRAW) # GL_DYNAMIC_READ
  checkGLError()
  glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 1, outputBuffer)

  glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)

  print2("✅ OK shader-storage-buffers:", dataBuffer, outputBuffer)
  return ids



def readIntOutput(buffer):
  buffer._m_order(MyBuffer.nativeOrder)
  buffer = buffer._m_asIntBuffer()
  arr = INT.new_array(buffer._m_remaining())
  buffer._m_get(arr)
  buffer._m_clear()
  return arr

def readByteOutput(buffer):
  arr = BYTE.new_array(buffer._m_remaining())
  buffer._m_get(arr)
  buffer._m_clear()
  return arr



def gpu_code_generator(ab, groups, checks):
  letters = groups * 5
  eax = len(ab)
  repeat_limit = letters // eax + 1

  while checks and checks[-1] == "*": checks = checks[:-1]
  if not checks: return """
void main() {
  uint index = gl_GlobalInvocationID.x + gl_WorkGroupSize.x * gl_NumWorkGroups.x * gl_GlobalInvocationID.y;
  if (index >= 86400000u) return;
  atomicOr(output_data.elements[index >> 5], 1u << (index & 31u));
}"""[1:]
  ab = {letter: i for i, letter in enumerate(ab)}
  print(ab)

  def checker(code, i):
    try: letter = checks[i]
    except IndexError: return None
    if letter == "*": return code.replace("caT", '')
    letter = ab[letter]
    return code.replace("caT", "\n  if (%s != %ru) return;" % (
      "LR"[i & 1],
      letter
    ))
  def parts():
    arr = []
    for i in range(1, inter):
      item = checker(body % (L1, L2)[i & 1], i)
      if item is None: return arr
      arr.append(item)
    for i in range(inter, letters):
      item = checker(body2 % (L3, L4)[i & 1], i)
      if item is None: return arr
      arr.append(item)
    return arr

  body = """
  s = s * 0x08088405u + 1u;
  %%s = uint(float(s) * %s. / 4294967296.);
  r[%%s]++;
  while (%%s == %%s) {
    s = s * 0x08088405u + 1u;
    %%s = uint(float(s) * %s. / 4294967296.);
  }caT
"""[1:] % (eax, eax)
  L1 = ("L", "L", "R", "L", "L")
  L2 = ("R", "R", "L", "R", "R")

  body2 = """
  while (true) {
    s = s * 0x08088405u + 1u;
    %%s = uint(float(s) * %s. / 4294967296.);
    if (r[%%s] < %s) break;
  }
  r[%%s]++;
  while (%%s == %%s) {
    s = s * 0x08088405u + 1u;
    %%s = uint(float(s) * %s. / 4294967296.);
  }caT
"""[1:] % (eax, repeat_limit, eax)
  L3 = ("L", "L", "L", "R", "L", "L")
  L4 = ("R", "R", "R", "L", "R", "R")

  inter = min(eax * 2, letters)
  return checker("""
void main() {
  uint index = gl_GlobalInvocationID.x + gl_WorkGroupSize.x * gl_NumWorkGroups.x * gl_GlobalInvocationID.y;
  if (index >= 86400000u) return;

  int r[] = int[](%s);

  uint s = index * 0x08088405u + 1u;
  uint L = uint(float(s) * %s. / 4294967296.), R;
  r[L] = 1;caT

%s
  atomicOr(output_data.elements[index >> 5], 1u << (index & 31u));
}
""", 0) % (
  ", ".join(["0"] * eax),
  eax,
  "\n".join(parts())
)



def shift(L, R):
  return (L + (1 << R - 1) - 1) >> R

class gpuRenderer:
  glVersion = 3

  def __init__(self, activity, view):
    self.activity  = activity
    self.view      = view
    self.seeds = 86400000 # 24 * 60 * 60 * 1000 = 0x5265c00
    # self.width, self.height = 0x1080, 0x5000
    # self.seeds = self.width * self.height # 0x5280000
    self.used = False

  def onSurfaceCreated(self, gl10, config):
    print("📽️ onSurfaceCreated", gl10, config)
    glClearColor(0.9, 0.95, 1, 0)

    # self.seeds в битах!
    # self.seeds >> 3 в байтах!
    ssbo_items = shift(self.seeds, 5)
    ssbo_size = ssbo_items << 2
    ssbo2_items = shift(ssbo_items, 8)
    ssbo2_size = ssbo2_items << 2
    print("ssbo_size:", ssbo_size)
    print("ssbo_items:", ssbo_items)
    print("ssbo2_size:", ssbo2_size)
    print("ssbo2_items:", ssbo2_items)

    self.cleaner = checkProgram(newProgram31("""#version 310 es
layout (local_size_x = 16, local_size_y = 16, local_size_z = 1) in;
layout(std430) buffer;
layout(binding = 0) writeonly buffer Output {
  uint elements[];
} output_data;
void main() {
  uint seed = gl_GlobalInvocationID.x + gl_WorkGroupSize.x * gl_NumWorkGroups.x * gl_GlobalInvocationID.y;
  if (seed < %su) output_data.elements[seed] = 0u;
}""" % ssbo_items))
    self.cleaner2 = checkProgram(newProgram31("""#version 310 es
layout (local_size_x = 16, local_size_y = 16, local_size_z = 1) in;
layout(std430) buffer;
layout(binding = 1) writeonly buffer Output {
  uint elements[];
} output_data;
void main() {
  uint seed = gl_GlobalInvocationID.x + gl_WorkGroupSize.x * gl_NumWorkGroups.x * gl_GlobalInvocationID.y;
  if (seed < %su) output_data.elements[seed] = 0u;
}""" % ssbo2_items))

    code = gpu_code_generator("1234567890", 15, "*7*30" +"*"*20 + "*183*" +"*"*20 + "15***")
    #code = gpu_code_generator("1234567890", 5, "*7*3")
    #code = gpu_code_generator("1234567890", 5, "**********")
    print(code)
    self.shader = checkProgram(newProgram31("""#version 310 es

layout (local_size_x = 16, local_size_y = 16, local_size_z = 1) in;
layout(std430) buffer;

layout(binding = 0) buffer Output {
  uint elements[];
} output_data;
/*layout(binding = 1) readonly buffer Input0 {
  uint elements[];
} input_data0;*/

%s
void mainNone() {
  uint seed = gl_GlobalInvocationID.x + gl_WorkGroupSize.x * gl_NumWorkGroups.x * gl_GlobalInvocationID.y;
  uint index = seed >> 5;

  // input_data0.elements[seed] * input_data0.elements[seed];
  if (seed == 0x5280000u-18u) return;

  atomicOr(output_data.elements[index], 1u << (seed & 31u));
}""" % code))

    self.counter = checkProgram(newProgram31("""#version 310 es

layout (local_size_x = 16, local_size_y = 16, local_size_z = 1) in;
layout(std430) buffer;

layout(binding = 0) readonly buffer Input0 {
  uint elements[];
} input_data0;
layout(binding = 1) buffer Output {
  uint elements[];
} output_data;

void main() {
  uint item = gl_GlobalInvocationID.x + gl_WorkGroupSize.x * gl_NumWorkGroups.x * gl_GlobalInvocationID.y;
  if (item >= %su) return;
  uint index = item >> 8;
  atomicAdd(output_data.elements[index], uint(bitCount(input_data0.elements[item])));
}""" % ssbo_items))
    self.outputBuffer = newSSBOs(ssbo_size, ssbo2_size)

    arr = (0, 0, 0, 0, 0, 0, 0, 0)._a_int
    for i in range(3): glGetIntegeri_v(GL_MAX_COMPUTE_WORK_GROUP_COUNT, i, arr, i)
    glGetIntegerv(GL_MAX_COMPUTE_WORK_GROUP_INVOCATIONS, arr, 3)
    for i in range(3): glGetIntegeri_v(GL_MAX_COMPUTE_WORK_GROUP_SIZE, i, arr, i + 4)
    glGetIntegerv(GL_MAX_SHADER_STORAGE_BLOCK_SIZE, arr, 7)
    print("🌴 Limits:", arr[:])
    self.limits = arr[:]

    print("default:", readByteOutput(self.readBuffer(0, ssbo_size - 0x100, 0x100))[:])
    T = time()
    self.calculate(self.cleaner, ssbo_items)
    self.calculate(self.cleaner2, ssbo2_items)
    td = time() - T
    print("Time:", td)
    print("default:", readByteOutput(self.readBuffer(0, ssbo_size - 0x100, 0x100))[:])

    T = time()
    self.calculate(self.shader, self.seeds)
    td = time() - T
    print("Time:", td)

    arr = readIntOutput(self.readBuffer(0, 0, ssbo_size))
    print(arr[:64])

    for n in range(4): # len(arr)):
      item = arr[n]
      if item:
        for bit in range(32):
          #print(n << 5 | bit, item, item >> bit, item >> bit & 1, "✅" if item >> bit & 1 else "🐓")
          if item >> bit & 1: print("✅", n << 5 | bit)

    T = time()
    self.calculate(self.counter, ssbo_items)
    td = time() - T
    print("Time:", td)

    arr2 = readIntOutput(self.readBuffer(1, 0, ssbo2_size))
    print("Всего найдено радиограмм:", sum(arr2))
    offset = 0
    for count in arr2:
      if count:
        for n in range(offset, offset + 256):
          item = arr[n]
          if item:
            for bit in range(32):
              #print(n << 5 | bit, item, item >> bit, item >> bit & 1, "✅" if item >> bit & 1 else "🐓")
              if item >> bit & 1: print("✅", n << 5 | bit)
      offset += 256
    # self.Print(0, (self.seeds >> 3) - 256, 256)
    #arr = readIntOutput(self.readBuffer(0, 0, 0x100 * 4))
    #print("👍", ((arr[i] >> 16, arr[i] & 0xffff) for i in range(256)))

  def onSurfaceChanged(self, gl10, width, height):
    print("📽️ onSurfaceChanged", gl10, width, height)
    glViewport(0, 0, width, height)

  def readBuffer(self, n, offset, size):
    print2("readBuffer")
    glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.outputBuffer[n])
    checkGLError()
    buffer = glMapBufferRange(GL_SHADER_STORAGE_BUFFER, offset, size, GL_MAP_READ_BIT)
    checkGLError()
    glUnmapBuffer(GL_SHADER_STORAGE_BUFFER)
    checkGLError()
    glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)
    return buffer

  def calculateOld(self, shader, width, height):
    glUseProgram(shader)
    glDispatchCompute(width >> 4, height >> 4, 1)
    glMemoryBarrier(GL_SHADER_STORAGE_BARRIER_BIT)
    print("CALCULATED!")

  def calculate(self, shader, items):
    width = (round(items ** 0.5) + 15) // 16 * 16
    height = ((items + width - 1) // width + 15) // 16 * 16
    print(hex(width), hex(height), "|", items, "->", width * height)
    glUseProgram(shader)
    glDispatchCompute(width >> 4, height >> 4, 1)
    glMemoryBarrier(GL_SHADER_STORAGE_BARRIER_BIT)
    print("CALCULATED!")

  def Print(self, n, offset, size):
    # buffer = self.readBuffer(n, offset * 4, size * 4)
    # print("👍", readIntOutput(buffer)[:])
    buffer = self.readBuffer(n, offset, size)
    if buffer is None:
      print2("SSBO reader error!")
      return
    arr = readByteOutput(buffer)
    print("👍", (arr[i] & 255 for i in range(size)))

  def onDrawFrame(self, gl10):
    glClear(GL_COLOR_BUFFER_BIT)

  def move(self, dx, dy): pass
  def event(self, up, down, misc): pass
  def getTByPosition(self, x, y, up): return 0
  def click(self, x, y, click_td): pass
  def restart(self): pass

  reverse = {
    "cr": onSurfaceCreated,
    "ch": onSurfaceChanged,
    "df": onDrawFrame,
  }
