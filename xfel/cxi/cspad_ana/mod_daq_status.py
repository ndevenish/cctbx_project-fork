from __future__ import absolute_import, division, print_function
# -*- Mode: Python; c-basic-offset: 2; indent-tabs-mode: nil; tab-width: 8 -*-
#
# XXX Could include injector positions.  What about laser intensities
# as read out from the diodes?
#
# $Id$

import logging
import threading
import wx

from xfel.cxi.gfx import status_plot
from xfel.cxi.cspad_ana import cspad_tbx
from xfel.cxi.cspad_ana import skip_event_flag

class StatusFrame_thread(threading.Thread):
  """The XrayFrame_thread class allows Run MainLoop() to be run as a
  thread, which is necessary because all calls to wxPython must be
  made from the same thread that originally imported wxPython.

  This is all based on "Running MainLoop in a separate thread",
  http://wiki.wxpython.org/MainLoopAsThread.
  """
  def __init__(self):
    threading.Thread.__init__(self) # XXX super()?
    self.setDaemon(1)
    self.start_orig = self.start
    self.start      = self.start_local
    self.frame      = None
    self.lock       = threading.Lock()
    self.lock.acquire()
    self.start()

  def run(self):
    import wx
    app   = wx.App(0)
    frame = status_plot.StatusFrame(None, -1, "CXI experiment status")
    frame.Show()
    self.frame = frame
    self.lock.release()
    app.MainLoop()

  def start_local(self):
    """The start_local() function calls the run() function through
    self.start_orig, and exists only after self.lock has been
    released.  This eliminates a race condition which could cause
    updates to be sent to non-existent frame."""
    self.start_orig()
    self.lock.acquire()

class mod_daq_status (object) :
  # XXX Could inherit from mod_event?
  def __init__ (self) :
    self.initialize()
    self.logger = logging.getLogger(__name__)
    self.logger.setLevel(logging.INFO)
    self.display_thread = StatusFrame_thread()
    self.window = self.display_thread.frame
    self.run_id = None

  def __del__ (self):
    logging.shutdown()

  def initialize (self) :
    self.nfail = 0
    self.nshots = 0
    self._t = []
    self._wavelength = []
    self._det_z = []
    self._laser01 = []
    self._laser04 = []
    self._laser04_power = []
    self._si_foil = []

  def beginjob(self, evt, env):
    env.update(evt)
    self.initialize()
    self.run_id = evt.run()
    event = status_plot.RunNumberEvent(self.run_id)
    wx.PostEvent(self.window, event)

  def event (self, evt, env) :
    if (evt.get("skip_event")) :
      return
    self.nshots += 1

    s = None
    t = evt.getTime()
    if (t is not None):
      s = t.seconds() + (t.nanoseconds() / 1000000000)
    else :
      self.nfail += 1
      self.logger.warning("event(): no timestamp, shot skipped")
      evt.put(skip_event_flag(), "skip_event")
      return
    if (not isinstance(s, float)) :
      raise RuntimeError("Wrong type for 's': %s" % type(s).__name__)

    # XXX This hardcodes the address for the front detector!
    det_z = cspad_tbx.env_detz('CxiDs1-0|Cspad-0', env)
    if (det_z is None):
      self.nfail += 1
      self.logger.warning("event(): no distance, shot skipped")
      evt.put(skip_event_flag(), "skip_event")
      return

    laser01 = cspad_tbx.env_laser_status(env, 1)
    if laser01 is None:
      self.nfail += 1
      self.logger.warning("event(): no status for laser 1, shot skipped")
      evt.put(skip_event_flag(), 'skip_event')
      return

    laser04 = cspad_tbx.env_laser_status(env, 4)
    if laser04 is None:
      self.nfail += 1
      self.logger.warning("event(): no status for laser 4, shot skipped")
      evt.put(skip_event_flag(), 'skip_event')
      return

    # Laser power for fourth laser.  The control name was provided by
    # Jan Kern.  XXX Move to its own function in cspad_tbx?
    laser04_power = None
    if env is not None:
      pv = env.epicsStore().value('CXI:LAS:MMN:02:ROT.RBV')
      if pv is not None and len(pv.values) == 1:
        laser04_power = pv.values[0]
    if laser04_power is None:
      self.nfail += 1
      self.logger.warning("event(): no power for laser 4, shot skipped")
      evt.put(skip_event_flag(), 'skip_event')
      return

    si_foil = cspad_tbx.env_sifoil(env)
    if (si_foil is None):
      self.nfail += 1
      self.logger.warning("event(): no Si-foil thickness, shot skipped")
      evt.put(skip_event_flag(), "skip_event")
      return
    if (not (isinstance(si_foil, float) or isinstance(si_foil, int))) :
      raise RuntimeError("Wrong type for 'si_foil': %s"% type(si_foil).__name__)

    wavelength = cspad_tbx.evt_wavelength(evt)
    if (wavelength is None):
      self.nfail += 1
      self.logger.warning("event(): no wavelength, shot skipped")
      evt.put(skip_event_flag(), "skip_event")
      return

    # In order to keep all arrays the same length, only append once
    # all values have been successfully obtained.  XXX Still bugs: see
    # June run 119.
    self._t.append(s)
    self._si_foil.append(si_foil)
    self._wavelength.append(wavelength)
    self._det_z.append(det_z)
    self._laser01.append(laser01)
    self._laser04.append(laser04)
    self._laser04_power.append(laser04_power)
    if (self.nshots % 120 == 0) :
      self.update_plot()

  def update_plot (self) :
    """
    Post an update event with current plot values to redraw the window.
    """
    event = status_plot.UpdateEvent(
      self._t, self._det_z, self._laser01, self._laser04, self._laser04_power,
      self._si_foil, self._wavelength)
    wx.PostEvent(self.window, event)

  #signature for pyana:
  #def endjob(self, env):

  #signature for psana:
  #def endjob(self, evt, env):

  def endjob(self, obj1, obj2=None):
    """
    @param evt Event object (psana only)
    @param env Environment object
    """

    if obj2 is None:
      env = obj1
    else:
      evt = obj1
      env = obj2

    # Make sure any remaining shots are taken into account.  XXX
    # Hardcoded update frequency.
    if (self.nshots % 120 != 0) :
      self.update_plot()
    print("END OF RUN")
    wx.PostEvent(self.window, status_plot.SaveImageEvent())

    # Uncomment to close the frame immediately.  Otherwise, wouldn't
    # it be nice if the window's title bar indicated that the run has
    # ended, so that one wouldn't have to watch the controlling
    # terminal?  XXX It may be safer to post an event than to call
    # Close() directly.
#    self.window.Close()

    self.display_thread.join()
