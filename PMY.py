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
import planetEngine



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
  for n in range(0, len(VBOdata), 5):
    x, y, z, U, V = VBOdata[n : n + 5]
    L = (x * x + y * y + z * z) ** 0.5
    # r, g, b = (sin(n * 3) + 2) / 3, (sin(n * 4) + 2) / 3, (sin(n * 5) + 2) / 3
    # L = 1 / L * 0.5 + L * 0.5
    L = 1 / L
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
    cX, cY, cZ = renderer.camera
    fwX, fwY, fwZ = renderer.forward
    nonlocal haloDraws
    halos2 = sorted(halos, key = lambda halo: dist(halo._pos.translate), reverse = True)
    haloDraws = [halo.draw for halo in halos2]
  def drawer():
    for draw in planetDraws: draw()
    glDepthMask(False)
    for draw in haloDraws: draw()
    glDepthMask(True)
  def recalcPlanetPositions():
    nonlocal day, prevTargetPos
    SunX, SunY, SunZ = sunPosition
    positions = planetPositions(day)
    for name in planetNames:
      pos = positions[name]
      x, z, y = pos[:3]
      PlanetX = SunX + x * step
      PlanetY = SunY + y * step
      PlanetZ = SunZ + z * step
      radius, model = planets[name]
      radius /= dist_div
      model.update2((PlanetX, PlanetY, PlanetZ))
      for moonName in moonNames.get(name, ()):
        x, z, y = positions[moonName][:3]
        MoonX = PlanetX + x * radius
        MoonY = PlanetY + y * radius
        MoonZ = PlanetZ + z * radius
        planets[moonName][1].update2((MoonX, MoonY, MoonZ))
    day += renderer.td

    radius, model = planets[target]
    x, y, z = model.translate
    if prevTargetPos is None:
      fx, fy, fz = renderer.forward
      r = radius * 2.5
      renderer.setCamPos(x - fx * r, y - fy * r, z - fz * r)
    elif type(prevTargetPos) is not int:
      px, py, pz = prevTargetPos
      dx, dy, dz = x - px, y - py, z - pz
      if dx or dy or dz:
        renderer.moveCam(dx, dy, dz)
    prevTargetPos = x, y, z

    # step = (sunS / sunRadius) / max(1, 10 - day / 2)

  def changeTarget(inc):
    nonlocal target, targetN, prevTargetPos
    if type(inc) is str:
      try: targetN = targetNames.index(inc)
      except ValueError: return
      target = inc
      radius, model = planets[target]
      prevTargetPos = model.translate
    else:
      targetN = (targetN + (1 if inc else -1)) % len(targetNames)
      target = targetNames[targetN]
      prevTargetPos = None
    renderer.setTargetText(target)
  def findNearestPlanet():
    def dist(pos):
      x, y, z = pos
      return (x - cX) ** 2 + (y - cY) ** 2 + (z - cZ) ** 2
    if type(prevTargetPos) is not tuple:
      return
    cX, cY, cZ = renderer.camera
    mi = 1e400
    result = None
    for name in targetNames:
      radius, model = planets[name]
      D = dist(model.translate) ** 0.5 - radius
      if D < mi:
        mi = D
        result = D, name, radius, model
    return result

  # Индекс неиспользованных в двигателе планет (от большей к меньшей):
  # Название модели в реестре SolarSystem.rbxm - описание

  # Ganymede - спутник Юпитера
  # Titan - спутник Сатурна
  # Callisto - спутник Юпитера
  # Io - спутник Юпитера
#✅ Moon (Luna) - ну понятно
  # Europa - спутник Юпитера
  # Triton - спутник Нептуна
  # Haumea — карликовая планета Солнечной системы, классифицирующаяся как плутоид, транснептуновый объект (ТНО)
  # Titania - спутник Урана
  # Rhea - спутник Сатурна
  # Oberon - спутник Урана
  # Iapetus - спутник Сатурна
  # Makemake - карликовая планета Солнечной системы, относится к транснептуновым объектам (ТНО), плутоидам. Является крупнейшим из известных классических объектов пояса Койпера
  # 2007 OR₁₀ - одна из крупнейших карликовых планет Солнечной системы
  # Charon - спутник Плутона
  # Umbriel - спутник Урана
  # Ariel - спутник Урана
  # Dione - спутник Сатурна
  # Quaoar - транснептуновый объект, один из крупнейших объектов в поясе Койпера, часто классифицируется как карликовая планета
  # Tethys - (Те́фия) спутник Сатурна
  # Sedna - транснептуновый объект. Была открыта 14 ноября 2003 года американскими наблюдателями Брауном, Трухильо и Рабиновицем
  # Orcus - Орк (90482 Orcus) — крупный транснептуновый объект из пояса Койпера, вероятно, являющийся карликовой планетой
  # Salacia - Салация (120347 Salacia по каталогу Центра малых планет) — транснептуновый объект, расположенный в поясе Койпера. Классифицируется и как кьюбивано (MPC), и как отделённый объект (DES). Он был обнаружен 22 сентября 2004 года группой учёных из Паломарской обсерватории. Обладает одним из самых низких значений альбедо среди крупных ТНО. Майкл Браун считает его кандидатом на статус карликовой планеты
  # 2002 MS4 - крупный транснептуновый объект в поясе Койпера. Он был открыт 18 июня 2002 года американскими астрономами Чедвиком Трухильо и Майклом Брауном
  # Varda - Варда (174567) — транснептуновый объект, кандидат в карликовые планеты. Открыт 21 июня 2003 года Джеффри Ларсеном по проекту Spacewatch
  # Ixion - Иксион (28978) — объект пояса Койпера. Является одним из крупнейших плутино (то есть транснептуновым объектом, орбита которого сходна с орбитой Плутона)
  # Dysnomia - спутник карликовой планеты (136199) Эрида, первоначально названный S/2005 (2003 UB313)
  # 2014 UZ₂₂₄ — крупный транснептуновый объект в поясе Койпера, кандидат в карликовые планеты. Открыт группой астрономов в рамках проекта Pan-STARRS 19 августа 2014 года посредством камеры DECam телескопа имени Виктора Бланко в обсерватории Серро-Тололо в Чили
  # Varuna - (20000) Ва́руна — транснептуновый объект, один из крупнейших кьюбивано (классических объектов пояса Койпера), отделённый объект
  # Vesta - Веста (официальное название — 4 Веста; англ. 4 Vesta) — астероид, движущийся вблизи внутренней границы Главного пояса астероидов. Входит в семейство Весты (вестоиды)
  # Pallas - Паллада (Pallas) — крупнейший астероид Главного пояса астероидов. Открыт 28 марта 1802 года Генрихом Вильгельмом Ольберсом и назван в честь древнегреческой богини Афины Паллады
  # Enceladus - спутник Сатурна
  # Chaos - Хаос (19521) — крупный транснептуновый объект в поясе Койпера. Был открыт в 1998 году в рамках проекта «Глубокий обзор эклиптики», в обсерватории Китт Пик на 4-метровом телескопе
  # Miranda - спутник Урана
  # Vanth - единственный известный спутник транснептунового объекта (90482) Орк. Его обнаружили Майкл Браун и Т. А. Суер, изучая изображения, полученные при помощи космического телескопа «Хаббл» 13 ноября 2005 года
  # Hygiea - карликовая планета в Солнечной системе, четвёртое по величине небесное тело в главном поясе астероидов между Марсом и Юпитером
  # Proteus - спутник Нептуна
  # Huya - Huya (38628) — крупный транснептуновый объект, относящийся к группе плутино и являющийся кандидатом в карликовые планеты. Он обращается в резонансе 2:3 с Нептуном
  # Mimas - спутник Сатурна
  # Ilmarë — спутник транснептунового объекта (кьюбивано) (174567) Варда. Был открыт 26 апреля 2009 года командой астрономов под руководством Кита С. Нолла на изображениях, поступающих с космического телескопа «Хаббл»
  # Nereid - (Нереида) спутник Нептуна
  # Actaea - Актея (120347 Salacia I Actaea) — спутник транснептунового объекта (120347) Салация. Был открыт 21 июля 2006 года на снимках телескопа «Хаббл». 13 18 февраля 2011 года спутнику присвоено название Актея — по имени морской нимфы
  # Chariklo - 10199 Харикло — один из крупнейших кентавров, самый большой астероид между Главным поясом и поясом Койпера. Харикло была открыта 15 февраля 1997 года Джеймсом Скотти в рамках проекта Spacewatch. Названа в честь Харикло — жены кентавра Хирона
  # Hi'iaka - крупный внешний спутник карликовой планеты Хаумеа. 13 Он был обнаружен 26 января 2005 года
  # Hyperion - восьмой спутник Сатурна
  # S/2012 (38628) 1 - маленький нерегулярный спутник, который вращается вокруг транснептунового объекта и кандидата в карликовые планеты 38628 Хуя. Он был открыт 6 мая 2012 года командой под руководством Кита Нолла
  # Larissa - Ларисса — внутренний спутник планеты Нептун. Также обозначается как Нептун VII. Ларисса была открыта Гарольдом Рейтсемой, Уильямом Хаббардом, Ларри Лебофски, Дэвидом Толеном 24 мая 1981 года благодаря случайному наблюдению с Земли покрытия этим спутником звезды. Повторно открыта в 1989 году при прохождении аппарата «Вояджер-2» возле Нептуна. Собственное название было дано 16 сентября 1991 года
  # MK2 - это единственный спутник карликовой планеты Makemake
  # Namaka - Намака — меньший внутренний спутник транснептуновой карликовой планеты Хаумеа. Он был открыт 30 июня 2005 года и назван в честь Намаки, богини моря в гавайской мифологии и одной из дочерей Хаумеа
  # Weywot - естественный спутник транснептуновой карликовой планеты Кваоар. Был открыт Майклом Брауном и Терри-Энн Суер с помощью снимков, сделанных космическим телескопом «Хаббл» 14 февраля 2006 года
  # Hale-Bopp - это комета. Она была открыта 23 июля 1995 года американскими астрономами Аланом Хейлом и Томасом Боппом
  # Phobos - спутник Марса
  # Deimos - спутник Марса
  # Halley's comet - Комета Галлея (официальное название 1P/Halley) — яркая короткопериодическая комета, возвращающаяся к Солнцу каждые 75–76 лет. Названа в честь английского астронома Эдмунда Галлея. С кометой связаны метеорные потоки эта-Аквариды и Ориониды

  def clickHandler(models, data):
    renderer.setClickHandler(models, lambda: clickByPlanet(data))
  def clickByPlanet(data):
    name, radius, translated = data
    if name != target:
      changeTarget(name)
      return
    print("planet!", data)
    if name in selectedPlanets: selectedPlanets.remove(name)
    else: selectedPlanets.add(name)
    for name in selectedPlanets:
      radius, model = planets[name]
      x, y, z = model.translate
      pos = (x, y, z, 1)._a_float
      pos2d = FLOAT.new_array(4)
      multiplyMV(pos2d, 0, renderer.MVPmatrix, 0, pos, 0)
      x, y, z, w = pos2d
      x /= w
      y /= w
      z /= w
      print("👣", name, x, y, z)
  def SunDraw(origDraw):
    def draw():
      glUniform1i(uLightSource, 1)
      origDraw()
      glUniform1i(uLightSource, 0)
    uLightSource = renderer.noPBR.uLightSource
    return draw

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
  planets = {}
  planetDraws = []
  halos = []
  haloDraws = []
  result = []
  X = 0
  planetNames = {"Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "Ceres", "Eris"}
  moonNames = {"Earth": ("Moon (Luna)",)}
  targetNames = ("Sun", "Mercury", "Venus", "Earth", "Moon (Luna)", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "Ceres", "Eris")
  targetNameSet = set(targetNames) # только для print

  for node in order:
    group = groups[node]
    name = node["_name"]
    print("🐾🐾🐕", len(group), name, ("🔥", "✅")[name in targetNameSet])

    radius = group[-1].info["size"][0] # с учётом пояса и только X
    if name not in planetNames:
      if X: X += radius
      pos = (X, -10, 0)
      X += radius
    else: pos = (0, 0, 0)

    union = UnionModel(group)

    n = len(group) - 1
    while "decal" in group[n].info: n -= 1
    radius = sum(group[n].info["size"]) / 3 # без учёта пояса и со всеми осями

    translated = TranslateModel(union, pos)
    result.append(translated)
    planets[name] = radius, translated

    for model in group:
      if "decal" in model.info:
        halos.append(model)
        model._pos = translated
      else:
        draw = model.draw
        if name == "Sun": draw = SunDraw(draw)
        planetDraws.append(draw)

    clickHandler(group[:n+1], (name, radius, translated))

  sunS = planets["Sun"][0]
  step = sunS / sunRadius
  print("step:", step) # Условных единиц длины на одну AU
  dist_div = 10
  step /= dist_div # Т.к. их СЛИШКОМ много
  sunPosition = planets["Sun"][1].translate
  renderer.lightPos = sunPosition
  day = 0  

  target = "???"
  targetN = -1
  changeTarget(1)
  prevTargetPos = 0
  selectedPlanets = set()

  renderer.camMoveEvent = haloSort
  renderer.recalcPlanetPositions = recalcPlanetPositions
  renderer.changeTarget = changeTarget
  renderer.findNearestPlanet = findNearestPlanet

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
    self.camera = 0, 0, -3.5
    self.eventN = 0
    self.time, self.td = time(), 0
    self.moveTd = 0
    self.moveTd2 = 0

    self.W = self.H = self.WH_ratio = -1
    self.FBO = None
    self.ready = False
    self.ready2 = False

    self.colorDimension = False
    self.clickHandlerQueue = []
    self.lightPos = 0, 3, 0

    self.camMoveEvent = lambda: None
    self.recalcPlanetPositions = lambda: None
    self.changeTarget = lambda inc: None
    self.findNearestPlanet = lambda: None
    self.lastNearestPlanet = "Sun"

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
      self.glyphs.setText(self.fpsText, "fps: %s" % S, self.W / 16)
    return self.fpsS

  def setTargetText(self, target):
    runOnGLThread(self.view, lambda:
      self.glyphs.setText(self.targetText, target, self.W / 12))

  def onSurfaceCreated(self, gl10, config):
    self.ready = self.ready2 = False
    print("📽️ onSurfaceCreated", gl10, config)
    self.time, self.td = time(), 0
    self.clickHandlerQueue.clear()

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

    textures = __resource("textures.png")
    skybox_labeled = __resource("skybox_labeled.png")
    skybox_space = __resource("skybox_space.webp")
    self.mainTexture = mainTextures = newTexture2(textures)
    skyboxLabeled = newTexture2(skybox_labeled)
    skyboxSpace   = newTexture2(skybox_space)

    # все шейдерные программы в одном месте

    self.program = firstProgram = mainProgram(self)
    self.gridProgram = gridProgram = d2textureProgram(mainTextures, (8, 64), self)
    self.skyboxes = (
      skyBoxLoader(gridProgram, (4, 50, 384, 65, 78, 401)),
      skyBoxLoader(d2textureProgram(skyboxLabeled, (1, 6), self), (0, 1, 2, 3, 4, 5)),
      skyBoxLoader(d2textureProgram(skyboxSpace, (4, 3), self), (6, 4, 3, 11, 7, 5), True),
      None,
      None,
    )
    self.textureChain = TextureChain(self)
    self.pbr = PBR(self)
    self.noPBR = NoPBR(self)
    self.glyphs = glyphs = glyphTextureGenerator(self)
    glyphs.printer = False
    self.colorama = Colorama(self)

    # настройка шейдерных программ

    gridProgram.setUp(0.25)
    gridProgram.add(160, 0.25, 5.5,  8, 1)
    gridProgram.add(142, 0.25, 6.75, 8, 2)
    gridProgram.add(45,  6.75, 6.75, 8, 3)
    gridProgram.setDirection(1)
    gridProgram.add(70,  2.25, 0.25, 10, 4)
    gridProgram.add(70,  8.75, 0.25, 10, 5)

    self.skyboxN       = 2
    self.currentSkybox = self.skyboxes[self.skyboxN]

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

    self.model_cache = {}
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
    self.SolarSystem.recalc(pbr_mat)
    self.ready = True

  def onSurfaceChanged(self, gl10, width, height):
    if not self.ready: return

    print("📽️ onSurfaceChanged", gl10, width, height)
    if width == self.W and height == self.H: return

    glViewport(0, 0, width, height)
    self.W, self.H, self.WH_ratio = width, height, width / height

    perspectiveM(self.projectionM, 0, 90, self.WH_ratio, 0.01, 1000000)
    self.calcMVPmatrix()

    if self.FBO is not None: deleteFrameBuffer(self.FBO)
    self.FBO = newFrameBuffer(width, height)

    # настройка glyphs

    glyphs = self.glyphs
    glyphs.setDirection(1)
    glyphs.setHeight(self.W / 16)
    glyphs.setColor(0xadddff)
    self.fpsText = glyphs.add(0, 0, 1, "fps: ?")
    glyphs.setHeight(self.W / 8)
    glyphs.setColor(0x0000ad)
    glyphs.add(2.375, -0.25, 10, "<-")
    glyphs.add(8.875, -0.25, 10, "->")
    glyphs.setColor(0xadffdd)
    glyphs.setHeight(self.W / 12)
    self.targetText = glyphs.add(3.375, 0.25, 10, "loading...")

    self.ready2 = True

  def calcMVPmatrix(self):
    MVPmatrix = self.MVPmatrix
    multiplyMM(MVPmatrix, 0, self.projectionM, 0, self.viewM, 0)
    # print("MVP:", self.MVPmatrix[:])
    multiplyMM(self.VPmatrix,  0, self.projectionM, 0, self.viewNotTranslatedM, 0)
    self.updMVP = False

    for model in self.models: model.recalc(MVPmatrix)
    self.rbxModel.recalc(MVPmatrix)
    if self.character: self.character.recalc(MVPmatrix)

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
      if event == 2: td = -td
      x, y, z = self.forward

      dist = self.findNearestPlanet()
      if dist is None:
        self.moveTd += td
        if self.moveTd >= 1:
          self.moveTd2 = min(self.moveTd2 + td, 5)
        td *= 3 ** self.moveTd2
      else:
        D, name, radius, model = dist
        # print(D, name, radius)
        if D > 10: td *= max(1, min(1.5 ** log2(D - 10), 3 ** 5))
        if name != self.lastNearestPlanet:
          self.lastNearestPlanet = name
          self.changeTarget(name)

      td *= 10
      self.moveCam(x * td, y * td, z * td)
    else:
      self.moveTd = 0
      self.moveTd2 = max(0, self.moveTd2 - td)

  def drawColorDimension(self):
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    self.colorama.draw(self.SolarSystem)
  def readPixel(self, x, y):
    buffer = MyBuffer.allocateDirect(4)
    buffer._m_order(MyBuffer.nativeOrder)
    glReadPixels(round(x), round(y), 1, 1, GL_RGBA, GL_UNSIGNED_BYTE, buffer)
    arr = BYTE.new_array(buffer._m_remaining())
    buffer._m_get(arr)
    return bytes(arr)

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

    self.noPBR.draw(self.SolarSystem)
    # self.pbr.draw(self.SolarSystem)

    self.gridProgram.draw(self.WH_ratio, self.eventN)
    self.glyphs.draw(self.WH_ratio)

  def onDrawFrame(self, gl10):
    if not self.ready2: return

    self.frames += 1
    T = time()
    self.td = T - self.time
    self.time = T
    #print("📽️ onDraw", gl)

    self.fps()
    self.eventHandler()
    self.recalcPlanetPositions()

    try: character = self.character.model
    except AttributeError: character = None
    if character is not None:
      yaw, pitch, roll = character.YPR
      yaw = (yaw + 15 * self.td) % 360
      character.setRotation(yaw, pitch, roll)

    if self.updMVP: self.calcMVPmatrix()

    glBindFramebuffer(GL_FRAMEBUFFER, self.FBO[0])
    queue = self.clickHandlerQueue
    if queue:
      self.drawColorDimension()
      for x, y in queue:
        rgba = self.readPixel(x, self.H - y)
        cb = self.colorama.to_n(rgba)
        if cb is not None: cb()
      self.clickHandlerQueue.clear()
    if self.skyboxN == 4:
      self.drawColorDimension()
    else: self.drawScene()
    glBindFramebuffer(GL_FRAMEBUFFER, 0)

    self.textureChain.postprocessing()
    #print("🫢", glGetError())

  def move(self, dx, dy):
    if not self.ready2: return
    self.yaw -= dx * 0.5
    self.pitch = max(-90, min(self.pitch - dy * 0.5, 90))
    self.calcViewMatrix()

  def setCamPos(self, x, y, z):
    self.camX = x
    self.camY = y
    self.camZ = z
    self.camera = x, y, z
    self.calcViewMatrix()
  def moveCam(self, dx, dy, dz):
    self.camX += dx
    self.camY += dy
    self.camZ += dz
    self.camera = self.camX, self.camY, self.camZ
    self.calcViewMatrix()

  def event(self, up, down, misc):
    self.eventN = up | down << 1 | misc << 2

  def getTByPosition(self, x, y):
    if not self.ready2: return -1
    return self.gridProgram.checkPosition(x / self.W, y / self.H)

  def click(self, x, y, click_td):
    if not self.ready2: return
    if click_td > 0.5: return
    t = self.getTByPosition(x, y)
    if t == -1:
      self.clickHandlerQueue.append((x, y))
    elif t == 3:
      self.skyboxN = N = (self.skyboxN + 1) % len(self.skyboxes)
      self.currentSkybox = self.skyboxes[N]
    elif t in (4, 5): self.changeTarget(t == 5)
    # print("🐾 click:", x, y, t)

  def setClickHandler(self, models, cb):
    color = self.colorama.next(cb)
    for model in models:
      model.setColor(color)

  def restart(self):
    print2("~" * 53)
    self.ready = self.ready2 = False
    self.W = self.H = self.WH_ratio = -1
    self.FBO = None
    SkyBox.restart()
    self.findNearestPlanet = lambda: None

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
    global HALT
    def halt(message):
      try:
        activity._m_finish()
        renderer.ready = renderer.ready2 = False
      except: pass
      exit(message)
    HALT = halt

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
HALT = exit
# ctxResources пока не используется
def Activity():
  global rm, ctxResources
  rm = ResourceManager()
  rm.xml("main", "main.xml", main_xml)
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
