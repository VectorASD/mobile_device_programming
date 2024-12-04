from byte import BYTE
from int import INT
from float import FLOAT 
from double import DOUBLE

BYTEarr = ()._a_byte
INTarr = ()._a_int # INT.new_array(0)
FLOATarr = ()._a_float

#print(INT.new_array(10)[:])
#print(INT.new_array(10, 12)[:])
#exit()



from java.security.MessageDigest import MessageDigest

MessageDigest_getInstance = MessageDigest._mw_getInstance(str)
class sha256:
  def __init__(self, md = None):
    if md is None: md = MessageDigest_getInstance("sha256")
    self.update = md._mw_update([]._a_byte)
    self.digest = md._mw_digest()
    clone = md._mw_clone()
    self.clone = lambda: sha256(clone())
class sha1:
  def __init__(self, data = None, md = None):
    if md is None: md = MessageDigest_getInstance("sha1")
    self.update = update = md._mw_update([]._a_byte)
    if data is not None: update(data)
    self.digest = md._mw_digest()
    clone = md._mw_clone()
    self.clone = lambda: sha1(None, clone())



from java.lang.Math import Math
from java.util.concurrent.locks.ReentrantLock import ReentrantLock

class MyLock:
  def __init__(self):
    self.obj = obj = ReentrantLock()
    self.lock = obj._mw_lock()
    self.unlock = obj._mw_unlock()
  def __enter__(self): self.lock()
  def __exit__(self, exc, val, trace): self.unlock()



sin = Math._mw_sin(DOUBLE)
cos = Math._mw_cos(DOUBLE)
asin = Math._mw_asin(DOUBLE)
acos = Math._mw_acos(DOUBLE)
atan2 = Math._mw_atan2(DOUBLE, DOUBLE)
floor = Math._mw_floor(DOUBLE)
pi = Math._f_PI
pi2 = pi / 2
pi180 = pi / 180
log = Math._mw_log(DOUBLE)
LOG_2 = log(2)
log2 = lambda n: log(n) / LOG_2
