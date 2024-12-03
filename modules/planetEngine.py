import common # floor, sin, cos, atan2
# print(pi)
# pi = 3.141592653589793
# pi180 = pi / 180
# сходятся числа pi

def time_to_d(year, month, day, hour, minute, UT=0, dst=0): 
  pr = 1/24 if dst else 0
  JDN = (367 * year - floor(7 * (year + floor((month + 9) / 12)) / 4)) + floor(275 * month / 9) + (day + 1721013.5 - UT / 24)
  JD = JDN + hour/24 + minute/1440 - pr
  j2000 = 2451543.5
  d = JD - j2000
  return d

def Planet_Sun(N, i, w, a, e, M):
  """
  N (Ω) - долгота восходящего узла. Это угол между направлением на точку весеннего равноденствия и направлением на восходящий узел орбиты планеты. Восходящий узел — это точка, где орбита планеты пересекает плоскость эклиптики (плоскость земной орбиты) двигаясь "вверх". Определяет ориентацию плоскости орбиты в пространстве.
  i - наклонение орбиты. Это угол между плоскостью орбиты планеты и плоскостью эклиптики.
  w (ω) - аргумент перицентра. Это угол между направлением на восходящий узел и направлением на перицентр (точка орбиты, ближайшая к Солнцу). Определяет ориентацию эллипса на орбитальной плоскости.
  a - большая полуось. Это половина длины самой длинной оси эллиптической орбиты планеты. Она определяет среднее расстояние планеты от Солнца.
  e - эксцентриситет. Это мера того, насколько вытянута орбита планеты. e = 0 соответствует круговой орбите, а e → 1 — сильно вытянутой эллиптической орбите.
  M - средняя аномалия. Это угол, который планета "прошла бы" за определенное время, если бы двигалась по круговой орбите с постоянной угловой скоростью. Он выражается в градусах и зависит от времени.
  """
  M %= 360
  M2 = M * pi180
  E0 = M + (180 / pi) * e * sin(M2) * (1 + e * cos(M2))
  E0 %= 360
  E02 = E0 * pi180
  E1 = E0 - (E0 - (180 / pi) * e * sin(E02) - M) / (1 - e * cos(E02))
  E1 %= 360
  E = E1 * pi180
  x = a * (cos(E) - e)
  y = a * ((1 - e*e) ** 0.5) * sin(E)

  r = (x*x + y*y) ** 0.5
  v = atan2(y, x)
  v = v / pi180 % 360

  vw = (v + w) * pi180
  xeclip = r * (cos(N * pi180) * cos(vw) - sin(N * pi180) * sin(vw) * cos(i * pi180))
  yeclip = r * (sin(N * pi180) * cos(vw) + cos(N * pi180) * sin(vw) * cos(i * pi180))
  zeclip = r * sin(vw) * sin(i * pi180) 
  long2 = atan2(yeclip, xeclip)
  long2 = long2 / pi180 % 360
  lat2 = atan2(zeclip, (xeclip*xeclip + yeclip*yeclip) ** 0.5)
  lat2 /= pi180
  return xeclip, yeclip, zeclip, long2, lat2, r

def spherical2rectangular(RA, Decl, r):
  # RA - лонгнитуда (long)
  # Decl - лантитуда (lat)
  RA *= pi180
  Decl *= pi180
  x = r * cos(RA) * cos(Decl)
  y = r * sin(RA) * cos(Decl)
  z = r * sin(Decl)
  return x, y, z

def rectangular2spherical(x, y, z):
  r    = (x*x + y*y + z*z) ** 0.5
  RA   = atan2(y, x)
  Decl = atan2(z, (x*x + y*y) ** 0.5)
    
  RA = RA / pi180 % 360
  Decl = Decl / pi180
  return RA, Decl, r

def Earth(w, a, e, M):
  # L = (w+M) % 360
  E = M + (180 / pi) * e * sin(M * pi180) * (1 + e * cos(M * pi180))
  E = E * pi180
  x = cos(E) - e
  y = sin(E) * (1 - e*e) ** 0.5

  r = (x*x + y*y) ** 0.5
  v = atan2(y, x) / pi180
  lon = (v+w) % 360 * pi180
  x2 = -r * cos(lon)
  y2 = -r * sin(lon)
  z2 = 0
  long, lat, dist = rectangular2spherical(x2, y2, z2)
  # dist == r
  return x2, y2, z2, long, lat, dist

def Ploutonas(d):
  S = ( 50.03 + 0.033459652 * d) * pi180
  P = (238.95 + 0.003968789 * d) * pi180

  long = (238.9508 + 0.00400703 * d
    -19.799 * sin(    P) +19.848 * cos(    P)
    + 0.897 * sin(2 * P) - 4.956 * cos(2 * P)
    + 0.610 * sin(3 * P) + 1.211 * cos(3 * P)
    - 0.341 * sin(4 * P) - 0.190 * cos(4 * P)
    + 0.128 * sin(5 * P) - 0.034 * cos(5 * P)
    - 0.038 * sin(6 * P) + 0.031 * cos(6 * P)
    + 0.020 * sin(S - P) - 0.010 * cos(S - P))
  lat = (-3.9082
    - 5.453 * sin(    P) -14.975 * cos(    P)
    + 3.527 * sin(2 * P) + 1.673 * cos(2 * P)
    - 1.051 * sin(3 * P) + 0.328 * cos(3 * P)
    + 0.179 * sin(4 * P) - 0.292 * cos(4 * P)
    + 0.019 * sin(5 * P) + 0.100 * cos(5 * P)
    - 0.031 * sin(6 * P) - 0.026 * cos(6 * P)
                         + 0.011 * cos(S - P))
  r = (40.72
    + 6.68 * sin(    P) + 6.90 * cos(P)
    - 1.18 * sin(2 * P) - 0.03 * cos(2 * P)
    + 0.15 * sin(3 * P) - 0.14 * cos(3 * P))

  x, y, z = spherical2rectangular(long, lat, r)
  return x, y, z, long, lat, r

def planetPositions(d):
  # print(time_to_d(2000, 1, 1, 0, 0)) # 1.0
  # d = time_to_d(2020, 1, 1, 12, 0)

  # Ermis (Меркурий)
  N = 48.3313 + 3.24587E-5 * d
  i = 7.0047 + 5.00E-8 * d
  w = 29.1241 + 1.01444E-5 * d
  a = 0.387098
  e = 0.205635 + 5.59E-10 * d
  M = 168.6562 + 4.0923344368 * d
  ermis = Planet_Sun(N, i, w, a, e, M)

  # xereclip,yereclip,zereclip, long2_er, lat2_er, r_er = Planet_Sun(
  #   M_er, e_er, a_er, N_er, w_er, i_er)
  # print("Mercury (horizontal):", long2_er, lat2_er, r_er)
  # print("Mercury (rectangular):", xereclip, yereclip, zereclip) # xzy в компьютерной системе координат

  # Afroditi (Венера)
  N = 76.6799 + 2.46590E-5 * d
  i = 3.3946 + 2.75E-8 * d
  w = 54.8910 + 1.38374E-5 * d
  a = 0.723330
  e = 0.006773 - 1.30E-9 * d
  M = 48.0052 + 1.6021302244 * d
  afroditi = Planet_Sun(N, i, w, a, e, M)

  # Earth (зЮмля)
  w = 282.9404 + 4.70935E-5 * d      
  a = 1 # расстояние от Солнца до Земли как раз и задаёт 1 а.е.
  e = 0.016709 - 1.151E-9 * d
  M = 356.047 + 0.9856002585 * d
  earth = Earth(w, a, e, M)

  # Aris (Марс)
  N = 49.5574 + 2.11081E-5 * d
  i = 1.8497 - 1.78E-8 * d
  w = 286.5016 + 2.92961E-5 * d
  a = 1.523688
  e = 0.093405 + 2.51E-9 * d
  M = 18.6021 + 0.5240207766 * d
  aris = Planet_Sun(N, i, w, a, e, M)

  # Dias (Юпитер)
  N = 100.4542 + 2.76854E-5 * d
  i = 1.3030 - 1.557E-7 * d
  w = 273.8777 + 1.6450E-5 * d
  a = 5.20256
  e = 0.048498 + 4.469E-9 * d
  M = 19.8950 + 0.0830853001 * d
  dias = Planet_Sun(N, i, w, a, e, M)
  M_di = M % 360

  # Kronos (Сатурн)
  N = 113.6634 + 2.38980E-5 * d
  i = 2.4886 - 1.081E-7 * d
  w = 339.3939 + 2.97661E-5 * d
  a = 9.55475
  e = 0.055546 - 9.499E-9 * d
  M = 316.9670 + 0.0334442282 * d
  kronos = Planet_Sun(N, i, w, a, e, M)
  M_kr = M % 360

  # Ouranos (Уран)
  N = 74.0005 + 1.3978E-5 * d
  i = 0.7733 + 1.9E-8 * d
  w = 96.6612 + 3.0565E-5 * d
  a = 19.18171 - 1.55E-8 * d
  e = 0.047318 + 7.45E-9 * d
  M = 142.5905 + 0.011725806 * d
  ouranus = Planet_Sun(N, i, w, a, e, M)
  M_ou = M % 360

  # Взаимодействие Юпитера, Сатурна и Урана между собой

  diat1 = -0.332 * sin((2 * M_di - 5 * M_kr - 67.6) * pi180)
  diat2 = -0.056 * sin((2 * M_di - 2 * M_kr + 21  ) * pi180)
  diat3 =  0.042 * sin((3 * M_di - 5 * M_kr + 21  ) * pi180)
  diat4 = -0.036 * sin((    M_di - 2 * M_kr       ) * pi180)
  diat5 =  0.022 * cos((    M_di -     M_kr       ) * pi180)
  diat6 =  0.023 * sin((2 * M_di - 3 * M_kr + 52  ) * pi180)
  diat7 = -0.016 * sin((    M_di - 5 * M_kr - 69  ) * pi180)
  diataraxes_long_di = diat1 + diat2 + diat3 + diat4 + diat5 + diat6 + diat7

  diat1 =  0.812 * sin((2 * M_di - 5 * M_kr - 67.6) * pi180)
  diat2 = -0.229 * cos((2 * M_di - 4 * M_kr -  2  ) * pi180)
  diat3 =  0.119 * sin((    M_di - 2 * M_kr -  3  ) * pi180)
  diat4 =  0.046 * sin((2 * M_di - 6 * M_kr - 69  ) * pi180)
  diat5 =  0.014 * sin((    M_di - 3 * M_kr + 32  ) * pi180)
  diataraxes_long_kr = diat1 + diat2 + diat3 + diat4 + diat5
  diat6 = -0.02  * cos((2 * M_di - 4 * M_kr -  2  ) * pi180)
  diat7 =  0.018 * sin((2 * M_di - 6 * M_kr - 49  ) * pi180)
  diataraxes_lat_kr = diat6 + diat7

  diat1 =  0.04  * sin((M_kr - 2 * M_ou +  6) * pi180)
  diat2 =  0.035 * sin((M_kr - 3 * M_ou + 33) * pi180)
  diat3 = -0.015 * sin((M_di -     M_ou + 20) * pi180)
  diataraxes_long_ou = diat1 + diat2 + diat3

  long, lat, r = dias[3:]
  x, y, z = spherical2rectangular(long + diataraxes_long_di, lat, r)
  dias = x, y, z, long, lat, r

  long, lat, r = kronos[3:]
  x, y, z = spherical2rectangular(long + diataraxes_long_kr, lat + diataraxes_lat_kr, r)
  kronos = x, y, z, long, lat, r

  long, lat, r = ouranus[3:]
  x, y, z = spherical2rectangular(long + diataraxes_long_ou, lat, r)
  ouranus = x, y, z, long, lat, r

  # Poseidonas (Нептун)
  N = 131.7806 + 3.0173E-5 * d
  i = 1.7700 - 2.55E-7 * d
  w = 272.8461 - 6.027E-6 * d
  a = 30.05826 + 3.313E-8 * d
  e = 0.008606 + 2.15E-9 * d
  M = 260.2471 + 0.005995147 * d
  poseidonas = Planet_Sun(N, i, w, a, e, M)

  # Ploutonas (Плутон)
  ploutonas = Ploutonas(d)

  # D CERES epoch 2455400.5 2010-jul-23.0   j2000= 2451543.5
  ddd = d + 2451543.5 - 2455400.5
  N = 80.39319901972638 + 1.1593E-5 * ddd
  i = 10.58682160714853 - 2.2048E-6 * ddd
  w = 72.58981198193074 + 1.84E-5 * ddd
  a = 2.765348506018043
  e = 0.07913825487621974 + 1.8987E-8 * ddd
  M = 113.4104433863731 + 0.21408169952325 * ddd
  ceres = Planet_Sun(N, i, w, a, e, M)

  # A CHIRON epoch  2456400.5 2013-apr-18.0   j2000= 2451543.5
  dddd = d + 2451543.5 - 2456400.5
  N = 209.3557401732507
  i = 6.929449422368333
  w = 339.3298742575888
  a = 13.6532230321495
  e = 0.3803659797957286
  M = 122.8444574834622 + 0.01953670401251872 * dddd
  chiron = Planet_Sun(N, i, w, a, e, M)

  # A ERIS epoch  2456400.5 2013-apr-18.0   j2000= 2451543.5
  ddddd = d + 2451543.5 - 2456400.5
  N = 36.0308972598494
  i = 43.88534676566927
  w = 150.8002573158863
  a = 67.95784302407351
  e = 0.4370835020505101
  M = 203.2157808586589 + 0.001759319413340421 * ddddd
  eris = Planet_Sun(N, i, w, a, e, M)

  return {
    'Mercury': ermis,
    'Venus'  : afroditi,
    'Earth'  : earth,
    'Mars'   : aris,
    'Jupiter': dias,
    'Saturn' : kronos,
    'Uranus' : ouranus,
    'Neptune': poseidonas,
    'Pluto'  : ploutonas,
    'Ceres'  : ceres,
    'Chiron' : chiron,
    'Eris'   : eris,
  }



AUm = 149597870700
# Астрономическая единица (AU) равна 149 597 870 700 метрам
# Расстояние от Солнца до Земли = 1 AU
# Летом 0.9832898912 AU
# Зимой 1.0167103335 AU

sunRadius = 695700000 # метров
sunRadius /= AUm
# print(sunRadius) # в AU = 0.004650467260962157

"""
GT       = {
     'Mercury': (263.83033031837124, -4.057599521202387, 0.4659797616165433),
     'Venus': (5.228267566604346, -3.2222136733454763, 0.7262291936644325),
     'Earth': (100.52892458583565, 0.0, 0.9833180862528659),
     'Mars': (214.38221616457562, 0.4891253753974966, 1.5891803735433014),
   # 'Jupiter': (276.10498313633025, 0.10374961050190847, 5.228112674603031),
     'Jupiter': (276.0863342124177,  0.10374961050190847, 5.228112674603031),
   # 'Saturn': (292.512767008796,   0.05134540100060894,  10.05212207219113),
     'Saturn': (292.60686589472857, 0.053486386724257005, 10.05212207219113),
   # 'Uranus': (35.35030250536327,    359.5159538071305, 19.809355998647174),
     'Uranus': (35.36072346107011, -0.48404619286953715, 19.80935599864717),
     'Neptune': (348.0172656026235, -1.039905299592724, 29.914939199387618),
     'Pluto': (292.7499413549187, -0.6709774750727665, 33.87680754878506),
     'Ceres': (290.86531789432115, -5.404211011344594, 2.9204640444111933),
     'Chiron': (4.327136751763591, 2.943432379699923, 18.810534112295773),
     'Eris': (23.548094614031402, -11.744274334977886, 95.99830322945104)
     }

GT2       = {
 'Mercury': (-0.04995474668786382, -0.46211955436524343, -0.03297239743832171),
 'Venus': (0.7220644052172724, 0.06607221451735312, -0.04082032480874338),
 'Earth': (-0.1796835606652678, 0.9667617476807042, 0),
 'Mars': (-1.3114849994179518, -0.8973947336694352, 0.013566426916695826),
 'Jupiter': (0.5560117501416899, -5.198453948006299, 0.009466916443751654),
 'Saturn': (3.8488483131935203, -9.286088717491223, 0.009008170828773239),
 'Uranus': (16.156527438922524, 11.460767849633232, -0.1673514066131819),
 'Neptune': (29.25827921158193, -6.209824739715596, -0.5429194988087228),
 'Pluto': (13.09960254295737, -31.239096028464672, -0.3967143031550649),
 'Ceres': (1.0355652247801526, -2.716810703397821, -0.2750536344563635),
 'Chiron': (18.732169225956646, 1.4174013926682936, 0.9659207897275007),
 'Eris': (86.16175536857236, 37.550227779065736, -19.539870226800424)
 }

for k, v in planetPositions().items():
  verdict  = "✅" if v[:3] == GT2[k] else "🔥"
  verdict2 = "✅" if v[3:] == GT [k] else "🔥"
  print(k, verdict, verdict2, " ")
  print([abs(v[i] - GT2[k][i]) for i in range(3)])
  # print([abs(v[i+3] - GT[k][i]) for i in range(3)])
print("•", -120 % 360, -120 % 360.0, divmod(-120, 360), divmod(-120, 360.0))
print("•", -120.5 % 360, -120.5 % 360.0, divmod(-120.5, 360), divmod(-120.5, 360.0))
"""
