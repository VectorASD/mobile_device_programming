from net.jpountz.lz4.LZ4Factory import LZ4Factory
from java.net.URL import URL
#from java.io.InputStreamReader import InputStreamReader
import rbxmMeshReader
import rbxmLoader

LZ4factory = LZ4Factory._m_fastestJavaInstance()
LZ4decompressor = LZ4factory._m_fastDecompressor()
LZ4decompress = LZ4decompressor._mw_decompress(BYTEarr, int, BYTEarr, int, int) # src, srcOff, dest, destOff, destLen



def NetworkRequests(url, contentType):
  conn = URL(url)._m_openConnection()
  conn._m_setRequestMethod("GET")
  conn._m_setRequestProperty("Content-Type", contentType)
  conn._m_setConnectTimeout(5000)
  conn._m_setReadTimeout(5000)
  conn._m_setInstanceFollowRedirects(False)
  status = conn._m_getResponseCode()
  # print(conn)
  # print(conn._m_getContentType())

  chunkL = 1024
  chunk = BYTE.new_array(chunkL)
  chunkB = bytes(chunk)
  IS = conn._m_getInputStream()
  reader = IS._mw_read(BYTEarr, int, int) # cbuf, off, len
  response = []
  while True:
    L = reader(chunk, 0, chunkL)
    if L <= 0: break
    response.append(chunkB[:L])
  response = b"".join(response)

  return status, response



class Storager:
  def __init__(self):
    path = "/sdcard/my_cache.asd"
    self.base = base = STORAGE("storager_cache")
    if not base:
      try:
        with open(path, "rb") as file:
          while True:
            b = file.read(1)
            if not b: break
            file.seek(-1, 1)
            name, cdn, data = (file.read(BytesIO(file.read(4)).unpack("<I")[0]) for i in range(3))
            base[name.decode("utf-8")] = cdn, data
      except OSError: pass
    self.file = open(path, "a")

  def writeStr(self, str):
    str = str if type(str) is bytes else str.encode("utf-8")
    b = BytesIO() # TODO
    b.pack("<I", len(str))
    writer = self.file.write
    writer(b.getvalue())
    writer(str)

  def put(self, name, cdn, data):
    try:
      self.base[name]
      return
    except KeyError: pass
    self.writeStr(name)
    self.writeStr(cdn)
    self.writeStr(data)
    self.file.flush()
    self.base[name] = cdn, data

  def get(self, name):
    try: return self.base[name]
    except KeyError: return None

storager = Storager()



def cdnLoader(asset):
  if type(asset) is not int:
    if not asset: return

    pos = len(asset) - 1
    while pos > 0 and asset[pos] in "0123456789": pos -= 1
    if asset[pos] not in "0123456789": pos += 1
    ID = asset[pos:]
    if not ID: return
  else: ID = asset

  assetURL = "https://assetdelivery.roblox.com/v1/assetId/%s" % ID
  print(assetURL)

  memory = storager.get(assetURL)
  if memory is not None:
    # print("CACHE!")
    cdn, content = memory
    return content

  # print("NETWORK!")
  status, response = NetworkRequests(assetURL, "application/json")
  print("status:", status)
  if status not in range(200, 300): exit("Status error: %s\n%s" % (status, response))
  obj = json.load(response)
  print(obj)

  status, content = NetworkRequests(obj["location"], "binary/octet-stream")
  print("status:", status)
  if status not in range(200, 300): exit("Status error: %s\n%s" % (status, response))

  storager.put(assetURL, response, content)
  return content

# cdnLoader(6023979233)
# cdnLoader(6246085453)
# exit()



# структура rbxm (Roblox Binary Model Format): https://dom.rojo.space/binary.html#byte-interleaving
# чей-то уже существующий python-вариант парсера rbxm: https://github.com/tapple/pyrxbm/blob/main/pyrxbm/binary.py
# основа LZ4-декомпрессора: https://github.com/python-lz4/python-lz4/blob/master/lz4libs/lz4.c#L1937
# процесс обращения с robloxAssetDelivery (взял только ссылку rbxassetidReadURL): https://github.com/Anaminus/rbxmk/blob/imperative/library/rbxassetid.go
# структура сеток (Roblox Mesh Format): https://devforum.roblox.com/t/roblox-mesh-format/326114
# структура CSGPHS (встречается в Shared String): https://devforum.roblox.com/t/some-info-on-sharedstrings-for-custom-collision-data-meshparts-unions-etc/294588

# пример цепочки ссылок:
#     rbxassetid://17481576983
#     https://assetdelivery.roblox.com/v1/assetId/17481576983
#     https://c7.rbxcdn.com/c9cf425d469ebf995547557fdb3d8f07
# уже ранее известно, что семёрка после 'c' - номер CDN-сервера, что просто модуль 8 суммы ascii/unicode-кодов hex-символов хеша





def String(content): # 0x01
  L = content.unpack("<I")[0]
  str = content.read(L)
  if len(str) < L: exit("Неудачная попытка считывания строки длины %s: %r" % (L, str))
  return str if any(i < 32 for i in str) else str.decode("utf-8")

def Bool(content, count): # 0x02
  arr = content.read(count)
  for byte in arr:
    if byte not in range(2): exit("Недопустимое Bool-значение: %s" % byte)
  return map(bool, arr)

def Int32(content, count): # 0x03
  data = b"".join(map(bytes, zip(content.read(count), content.read(count), content.read(count), content.read(count))))
  referents = tuple((x >> 1) ^ -(x & 1) for x in BytesIO(data).unpack(">%sI" % count)) # TODO
  return referents

def Float(bytes):
  # Standard	seeeeeee emmmmmmm mmmmmmmm mmmmmmmm
  # Roblox	eeeeeeee mmmmmmmm mmmmmmmm mmmmmmms
  #exp, b, c, d = content.read(4)
  #mant, sign = b << 15 | c << 7 | d >> 1, d & 1
  #data = sign << 31 | exp << 23 | mant
  #print(data.to_bytes(4, "big").hex())
  #return unpack(">f", data.to_bytes(4, "big"))[0]
  x = int.from_bytes(bytes, "big") #, signed = False) # signed и так по умолчанию = False... просто пометил
  res = BytesIO(((x & 1) << 31 | x >> 1).to_bytes(4, "big")).unpack(">f")[0] # TODO
  return res
#print(Float(bytes.fromhex("7c400001"))) # -0.15625 ok!
#exit()
def Float32(content, count): # 0x04
  return (Float(bytes(i)) for i in zip(content.read(count), content.read(count), content.read(count), content.read(count)))

def Float64(content, count): # 0x05
  return content.unpack("<%sd" % count)

def UDim(content, count): # 0x06
  scale = Float32(content, count)
  offset = Int32(content, count)
  return zip(scale, offset)

def UDim2(content, count): # 0x07
  scale = Float32(content, count)
  scale2 = Float32(content, count)
  offset = Int32(content, count)
  offset2 = Int32(content, count)
  return zip(zip(scale, offset), zip(scale2, offset2))

def Color3(content, count): # 0x0c
  R = Float32(content, count)
  G = Float32(content, count)
  B = Float32(content, count)
  return zip(R, G, B)

def Vector2(content, count): # 0x0d
  X = Float32(content, count)
  Y = Float32(content, count)
  return zip(X, Y)

def Vector3(content, count): # 0x0e
  X = Float32(content, count)
  Y = Float32(content, count)
  Z = Float32(content, count)
  return zip(X, Y, Z)

def getRotators():
  def rotX(s, c): return 1, 0, 0, 0, c, -s, 0, s, c
  def rotY(s, c): return c, 0, s, 0, 1, 0, -s, 0, c
  def rotZ(s, c): return c, -s, 0, s, c, 0, 0, 0, 1
  def mul(a, b):
    a00, a01, a02, a10, a11, a12, a20, a21, a22 = a
    b00, b01, b02, b10, b11, b12, b20, b21, b22 = b
    return (
      a00 * b00 + a01 * b10 + a02 * b20, a00 * b01 + a01 * b11 + a02 * b21, a00 * b02 + a01 * b12 + a02 * b22,
      a10 * b00 + a11 * b10 + a12 * b20, a10 * b01 + a11 * b11 + a12 * b21, a10 * b02 + a11 * b12 + a12 * b22,
      a20 * b00 + a21 * b10 + a22 * b20, a20 * b01 + a21 * b11 + a22 * b21, a20 * b02 + a21 * b12 + a22 * b22)
  pi180 = 0.017453292519943295
  def fromEulerAngles(x, y, z): # проверено в Roblox Studio на print(CFrame.fromEulerAngles(math.rad(10), math.rad(20), math.rad(30)))
    x, y, z = x * pi180, y * pi180, z * pi180
    sx, cx, sy, cy, sz, cz = sin(x), cos(x), sin(y), cos(y), sin(z), cos(z)
    return mul(mul(rotX(sx, cx), rotY(sy, cy)), rotZ(sz, cz))
  def fromEulerAnglesYXZ(x, y, z): # проверено в Roblox Studio на print(CFrame.fromEulerAnglesYXZ(math.rad(10), math.rad(20), math.rad(30)))
    x, y, z = x * pi180, y * pi180, z * pi180
    sx, cx, sy, cy, sz, cz = sin(x), cos(x), sin(y), cos(y), sin(z), cos(z)
    return mul(mul(rotY(sy, cy), rotX(sx, cx)), rotZ(sz, cz))
  rotators = (
    None, None, (0, 0, 0), (90, 0, 0), None, (0, 180, 180), (-90, 0, 0), (0, 180, 90), None, (0, 90, 90),
    (0, 0, 90), None, (0, -90, 90), (-90, -90, 0), (0, -90, 0), None, (90, -90, 0), (0, 90, 180),
    None, None, (0, 180, 0), (-90, -180, 0), None, (0, 0, 180), (90, 180, 0), (0, 0, -90), None, (0, -90, -90),
    (0, -180, -90), None, (0, 90, -90), (90, 90, 0), (0, 90, 0), None, (-90, 90, 0), (0, -90, 180))
  #for i, j in enumerate(rotators):
  #  if j: print(hex(i), j) всё сошлось
  return tuple((fromEulerAnglesYXZ(rotator[0], rotator[1], rotator[2]) if rotator else None) for rotator in rotators)
  # также, properties explorer в Roblox Studio преобразует поворот именно по fromEulerAnglesYXZ, а не fromEulerAngles!
CFrameRotators = getRotators()
# print(CFrameRotators)

def CFrame(content, count): # 0x10
  rotators = []
  for i in range(count):
    ID = content.read(1)[0]
    if ID:
      try: rotator = CFrameRotators[ID]
      except KeyError: rotator = None
      if rotator is None: exit("Недопустимое значение вращателя CFrame: %s" % ID)
      rotators.append(rotator)
    else: rotators.append(content.unpack("<9f"))
  return (vec + rot for rot, vec in zip(rotators, Vector3(content, count)))

def Enum(content, count): # 0x12
  data = b"".join(map(bytes, zip(content.read(count), content.read(count), content.read(count), content.read(count))))
  return BytesIO(data).unpack(">%sI" % count) # TODO

def Referent(content, count): # 0x13
  data = b"".join(map(bytes, zip(content.read(count), content.read(count), content.read(count), content.read(count))))
  referents = [(x >> 1) ^ -(x & 1) for x in BytesIO(data).unpack(">%sI" % count)]
  for i in range(1, count): referents[i] += referents[i - 1]
  return referents

def Rect(content, count): # 0x18 не до конца протестировано
  MinX = Float32(content, count)
  MinY = Float32(content, count)
  MaxX = Float32(content, count)
  MaxY = Float32(content, count)
  return zip(zip(MinX, MaxX), zip(MinY, MaxY))

def PhysicalProperties(content, count): # 0x19
  #content = BytesIO(bytes.fromhex("00 01 33 33 33 3f 9a 99 99 3e 00 00 00 3f 00 00 80 3f 00 00 80 3f".replace(" ", "")) + b"\0" * (count - 2))
  return tuple(content.unpack("<5f") if content.read(1)[0] else None for i in range(count))

def Color3uint8(content, count): # 0x1a
  R = content.read(count)
  G = content.read(count)
  B = content.read(count)
  return zip(R, G, B)

def Int64(content, count): # 0x1b
  data = b"".join(map(bytes, zip(content.read(count), content.read(count), content.read(count), content.read(count), content.read(count), content.read(count), content.read(count), content.read(count))))
  return ((x >> 1) ^ -(x & 1) for x in BytesIO(data).unpack(">%sQ" % count)) # TODO

def SharedString(content, count, SStrings): # 0x1c
  data = b"".join(map(bytes, zip(content.read(count), content.read(count), content.read(count), content.read(count))))
  return (SStrings[i] for i in BytesIO(data).unpack(">%sI" % count)) # TODO

def OptionalCoordinateFrame(content, count): # 0x1e
  # content = BytesIO(bytes.fromhex("10 0a 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 7f 00 00 00 00 00 00 00 02 01 00".replace(" ", "")))
  # count = 2
  if content.read(1)[0] != 0x10: exit("Ожидался CFrame внутри OptionalCoordinateFrame")
  cframes = CFrame(content, count)
  if content.read(1)[0] != 0x02: exit("Ожидался Bool внутри OptionalCoordinateFrame")
  have_a_value = Bool(content, count)
  return zip(have_a_value, cframes)

def Font(content, count): # 0x20
  fonts = []
  for i in range(count):
    family = String(content)
    weight, style = content.unpack("<HB")
    cachedFaceId = String(content)
    fonts.append((family, weight, style, cachedFaceId))
  return fonts

def Capabilities(content, count): # 0x21
  content.read()
  return "?" * count

dbgPrint = False
dbgType = None

PROP_types = {
  # 0x00: не существует
  0x01: lambda content, count: (String(content) for i in range(count)),
  0x02: Bool,
  0x03: Int32,
  0x04: Float32,
  0x05: Float64,
  0x06: UDim,
  0x07: UDim2,
  # 0x08: Ray,
  # 0x09: Faces,
  # 0x0a: Axes,
  # 0x0b: BrickColor,
  0x0c: Color3,
  0x0d: Vector2,
  0x0e: Vector3,
  # 0x0f: не существует
  0x10: CFrame,
  # 0x11: не существует
  0x12: Enum,
  0x13: Referent,
  # 0x14: Vector3int16
  # 0x15: NumberSequence
  # 0x16: ColorSequence,
  # 0x17: NumberRange,
  0x18: Rect,
  0x19: PhysicalProperties,
  0x1a: Color3uint8,
  0x1b: Int64,
  0x1c: SharedString,
  # 0x1d: Bytecode,
  0x1e: OptionalCoordinateFrame,
  # 0x1f: UniqueId,
  0x20: Font,
  0x21: Capabilities, # неизвестное содержание. Везде нулевые байты :/
  # всё, что после 0x21: не существует
}

def CFrame2mat(CFrame):
  if CFrame is None: return (1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)._a_float
  x, y, z, r00, r01, r02, r10, r11, r12, r20, r21, r22 = CFrame
  return (r00, r10, r20, 0, r01, r11, r21, 0, r02, r12, r22, 0, x, y, z, 1)._a_float





def META(content):
  entries = content.unpack("<I")[0]
  meta = {}
  for i in range(entries):
    key, value = String(content), String(content)
    try:
      conflict = meta[key]
      exit("Конфликтный ключ %r: %r <-> %r" % (key, conflict, value))
    except KeyError: meta[key] = value
  what = content.read()
  if what: exit("Не до конца считанный META-чанк: %s" % what)
  return meta

def SSTR(content, SStrings): # Shared STRings
  version, count = content.unpack("<II")
  if version != 0: exit("Странная версия SSTR-чанка: %s" % version)
  for i in range(count):
    hash, str = content.read(16), String(content)
    if dbgPrint: print("%s %r" % (hash.hex(), str))
    SStrings.append(str)
  what = content.read()
  if what: exit("Не до конца считанный SSTR-чанк: %s" % what)

def INST(content):
  classID = content.unpack("<I")[0]
  className = String(content)
  objectFormat, count = content.unpack("<BI")
  if objectFormat not in range(2): exit("Неизвестный формат INST-чанка: %s" % objectFormat)
  referents = Referent(content, count)
  markers = content.unpack("<%sB" % count) if objectFormat else None
  what = content.read()
  if what: exit("Не до конца считанный INST-чанк: %s" % what)
  return classID, className, objectFormat, referents, markers

typesAll = set()
def PROP(content, CTX):
  SStrings, classes, root, instances = CTX

  classID = content.unpack("<I")[0]
  propertyName = String(content)
  typeID = content.read(1)[0]
  typesAll.add(typeID)

  try: inst = classes[classID]
  except KeyError: exit("Несуществующий classID в PROP-чанке: %s" % classID)
  className, objectFormat, referents, markers = inst
  count = len(referents)

  try:
    Type = PROP_types[typeID]
    #if dbgType is None or typeID == dbgType:
      # print()
      # print(propertyName, hex(typeID), "| class:", classID, className, count, referents, "---> ", end = "")
  except KeyError: Type = None

  if Type is None:
    print("Неизвестный typeID: %s" % typeID)
    values = ()
  else: values = Type(content, count, SStrings) if typeID == 0x1c else Type(content, count)

  # values2 = [] # только для печати
  for id, value in zip(referents, values):
    # values2.append(value)
    try: node = instances[id]
    except KeyError: exit("Нет экземпляра с таким id: %s" % id)
    try:
      conflict = node["_props"][propertyName]
      exit("Повторяющийся параметр %r: %r <-> %r" % (propertyName, conflict, value))
    except KeyError:
      #if dbgType is None or typeID == dbgType or propertyName == "Name":
      if propertyName == "Name": node["_name"] = checkString((typeID, value))
      else: node["_props"][propertyName] = typeID, value

  if dbgType is None:
    if Type is not None:
      what = content.read()
      if what: exit("Не до конца считанный PROP-чанк: %s" % what)
      # print(tuple(values2))
      # print()
  elif typeID == dbgType:
    what = content.read()
    #print(count, len(what), what.hex(), tuple(values2))
    print()

def PRNT(content, instances): # parents
  version, count = content.unpack("<BI")
  if version != 0: exit("Странная версия PRNT-чанка: %s" % version)
  childs = Referent(content, count)
  parents = Referent(content, count)
  for child, parent in zip(childs, parents):
    try: L = instances[child]
    except KeyError: exit("Нет потомка с таким id: %s" % child)
    try: R = instances[parent]
    except KeyError: exit("Нет родителя с таким id: %s" % parent)
    if L["_parent"] is not None: exit("Повторное присвоение родителя: %s %s %s %s" % (child, parent, L, R))
    L["_parent"] = R
    R["_childs"].append(L)
    # print(child, parent, L, R)
  for node in instances.values():
    if node["_parent"] is None: exit("Существует узел без родителя: %s" % node)
  what = content.read()
  if what: exit("Не до конца считанный PRNT-чанк: %s" % what)
  return childs, parents





def printTree(node, lvl = "", check = False):
  id, parent, childs, className, name = node["_id"], node["_parent"], node["_childs"], node["_class"], node["_name"]
  data = node["_props"]
  data = {k: v for k, (t, v) in data.items() if dbgType is None or t == dbgType}

  checked = dbgType is None or any(printTree(child, "", True) for child in childs)
  if check: return bool(data) or checked

  if data or checked: print("%s%s %s (%s) %s" % (lvl, id, name, className, data))
  lvl += "| "
  for child in childs: printTree(child, lvl)

def printTree2(node, lvl = ""):
  id, childs, className, name = node["_id"], node["_childs"], node["_class"], node["_name"]
  data = "" # node["_props"]
  print("%s%s %s (%s) %s" % (lvl, id, name, className, data))
  lvl += "| "
  for child in childs: printTree2(child, lvl)

def Chunk(file, CTX):
  SStrings, classes, root, instances = CTX

  name, compressL, uncompressL, reserved = file.unpack("<4sII4s")
  while name[-1] == 0: name = name[:-1]
  if dbgPrint: print("Чанк %r длины %s -> %s" % (name, compressL, uncompressL))
  if reserved != b"\0" * 4: exit("Странный reserved чанка: %s" % reserved.hex())

  compressed = compressL > 0
  dataL = compressL if compressed else uncompressL
  chunk = file.read(dataL)
  if compressed:
    src = chunk._a_byte
    dest = BYTE.new_array(uncompressL)
    LZ4decompress(src, 0, dest, 0, uncompressL)
    data = bytes(dest)
  else: data = chunk
  # check = lz4.block.compress(data, store_size=False)
  content = BytesIO(data)
  if name == b"META":
    meta = META(content)
    if dbgPrint: print(meta)
  elif name == b"SSTR":
    SSTR(content, SStrings)
    if dbgPrint: print(SStrings)
  elif name == b"INST":
    classID, className, objectFormat, referents, markers = INST(content)
    if dbgPrint: print(classID, className, "service" if objectFormat else "regular", referents, markers)
    inst = className, objectFormat, referents, markers
    try:
      conflict = classes[classID]
      exit("Конфликтный classID %r: %r <-> %r" % (classID, conflict, inst))
    except KeyError: classes[classID] = inst

    for referent in referents:
      data = {"_id": referent, "_parent": None, "_childs": [], "_class": className, "_name": "🤔", "_props": {}}
      try:
        conflict = instances[referent]
        exit("Конфликтный referent %r: %r <-> %r" % (referent, conflict, data))
      except: instances[referent] = data
  elif name == b"PROP":
    PROP(content, CTX)
  elif name == b"PRNT":
    PRNT(content, instances)
  elif name == b"END":
    if data != b'</roblox>': print("Странное окончание: %r" % data)
    return True
  else: exit("UNKNOWN CHUNK (%r): %r" % (name, data))

def rbxmReader(resource):
  SStrings = []
  classes = {}
  root = {"_id": -1, "_parent": "x", "_childs": [], "_class": "root", "_name": "root", "_props": {}}
  instances = {-1: root}
  CTX = (SStrings, classes, root, instances)

  file = BytesIO(resource)
  if file.read(8) != b'<roblox!': exit("Это не rbxm!")
  sign = file.read(6).hex()
  if sign != "89ff0d0a1a0a": exit("Неверная подпись: %s" % sign)
  version, classes, instances, reserved = file.unpack("<Hii8s")
  print("Класов:", classes)
  print("Экземпляров:", instances)
  if version != 0: exit("Странная версия заголовка: %s" % version)
  if reserved != b"\0" * 8: exit("Странный reserved заголовка: %s" % reserved.hex())
  while True:
    end = Chunk(file, CTX)
    if end: break
  return root

def loadRBXM(resource, name, textureChain):
  cache = STORAGE("rbxm_cache")
  T = time()
  print("🐾🐾🐾")
  try: root = cache[name]
  except KeyError: root = None
  if root is None:
    root = rbxmReader(resource)
    cache[name] = root
  # printTree(root)
  models = modelLoader(root, name, textureChain)
  print("models:", len(models))
  print("🐾🐾🐾", time() - T)
  return models

"""
Проверка самодельного BytesIO и pack/unpack функций внутри.
Всё уже было, только unpack не было - пришлось к этому rbxmReader докодивать (по случаю нужды) :/

bb = BytesIO(b"\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\1\0\0\0\0\0\0\0\x7f\0\0\0\0\0\0\0\x80\0\0\0\0\0\0\0\x81\0\0\0\xff\xff\xff\xff\xff")
print(bb.unpack("<6q"))
bb.seek(0)
print(bb.unpack("<6Q"))
bb.seek(0)
print(bb.unpack(">6q"))
bb.seek(0)
print(bb.unpack(">6Q"))
"""
