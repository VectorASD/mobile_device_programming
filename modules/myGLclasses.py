import myGL



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

    print2("✅ OK buffers:", VBO, IBO)
    self.data = VBO, IBO, IBOdata.capacity()

  def draw(self, func = None):
    VBO, IBO, indexes = self.data

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, IBO)

    if func is None:
      glVertexAttribPointer(Model.vPosition, 3, GL_FLOAT, False, 9 * 4, 0)
      glVertexAttribPointer(Model.vColor,    4, GL_FLOAT, False, 9 * 4, 3 * 4)
      glVertexAttribPointer(Model.vUV,       2, GL_FLOAT, False, 9 * 4, 7 * 4)
    else: func()

    glDrawElements(GL_TRIANGLES, indexes, GL_UNSIGNED_INT, 0)
    #glBindBuffer(GL_ARRAY_BUFFER, 0)
    #glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)





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
