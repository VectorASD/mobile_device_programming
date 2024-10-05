if True: # __name__ == "__main__":
  from executor import main, load_codes # пока нереализован доступный всем способ компиляции БЕЗ доступа к компилятору (облачные технологии)
  load_codes("PMY.py")
  main("pmy")
  exit()

###~~~### pmy

from android.content.Context import Context
from android.view.View import View
from android.opengl.GLSurfaceView import GLSurfaceView
from android.view.Window import Window
from android.view.WindowManager_._LayoutParams import WindowManagerLayoutParams
from android.opengl.GLES20 import GLES20

ACTIVITY_SERVICE = Context._f_ACTIVITY_SERVICE
FEATURE_NO_TITLE = Window._f_FEATURE_NO_TITLE.int
FLAG_FULLSCREEN = WindowManagerLayoutParams._f_FLAG_FULLSCREEN.int

GL_COLOR_BUFFER_BIT = GLES20._f_GL_COLOR_BUFFER_BIT.int



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
    def onSurfaceCreated(self, gl, config):
      print("📽️ onSurfaceCreated", gl, config)
      gl._m_glClearColor((1).float, (0).float, (0).float, (0).float)
    def onSurfaceChanged(self, gl, width, height):
      print("📽️ onSurfaceChanged", gl, width, height)
      gl._m_glViewport((0).int, (0).int, width.int, height.int)
    def onDrawFrame(self, gl):
      self.frames += 1
      #print("📽️ onDraw", gl)
      print(self.fps())
      gl._m_glClear(GL_COLOR_BUFFER_BIT)
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
