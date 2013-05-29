import wx
import wx.aui
import matplotlib as mpl

from copy import deepcopy
from threading import Thread
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as Canvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as Toolbar

from stats import Stats

new_run_event = wx.NewId()
def bind_event(window, id, cb):
    window.Connect(-1, -1, id, cb)

def start_callback(stats, cb):

    def f():
        cb(stats)

    return f

def fire_event(to, type, data):
    ev = wx.PyEvent()
    ev.SetEventType(type)
    ev.data = data

    wx.PostEvent(to, ev)

class Window(object):

    def __init__(self, cb):
        self.app = wx.PySimpleApp()

        self.cb = cb
        self.frame = wx.Frame(None, -1, 'Sim')
        sizer = wx.BoxSizer(wx.VERTICAL)

        start_id = wx.NewId()
        sizer.Add(wx.Button(self.frame, start_id, 'Start'))
        self.frame.SetSizer(sizer)
        sizer.Fit(self.frame)
        self.frame.Show()

        self.frame.Bind(wx.EVT_BUTTON, self.run_event, id = start_id)

        self.app.MainLoop()

    def run_event(self, ev):

        stats = Stats(12, 24)

        frame = RunFrame(stats)
        frame.Show()

        self.thread = Thread(target = start_callback(stats, self.cb))
        self.thread.start()

update_plot_event = wx.NewId()

class RunFrame(wx.Frame):

    def __init__(self, stats):
        wx.Frame.__init__(self, None, -1, 'Run')

        stats.set_observer(self)
        self.sizer = wx.GridSizer(4, 2)
        self.plots = []

        self.active_workforce_axes = self.add_plot(stats, "Devs")

        self.sales_axes = self.add_plot(stats, "HH")
        self.declined_axes = self.add_subplot(self.sales_axes)

        self.sales_money_axes = self.add_plot(stats, "$")
        self.declined_money_axes = self.add_subplot(self.sales_money_axes)

        self.workload_axes = self.add_plot(stats, "HH")

        self.SetSizer(self.sizer)
        self.sizer.Fit(self)

        bind_event(self, update_plot_event, self.update_plot)

    def add_plot(self, stats, ylabel):
        plot = Plot(self)
        axes = plot.figure.gca(
                xlim = (stats.warm_up, stats.runs),
                adjustable = 'box',
                xlabel = "Months",
                ylabel = ylabel)
        axes.set_autoscalex_on(False)

        self.sizer.Add(plot)
        self.plots.append(plot)
        return plot.figure.gca()

    def add_subplot(self, axes):
        new_axes = axes.twinx()
        new_axes.set_autoscalex_on(False)
        return new_axes

    def end_month(self, stats):
        fire_event(self, update_plot_event, stats)

    def legend(self, axes, lines):
        axes.legend(lines, [l.get_label() for l in lines])


    def update_plot(self, ev):
        stats = ev.data
        x = stats.current_step + 1

        p1, = self.active_workforce_axes.step(x, stats.active_workforce[-1], 'g*', label = "Active Workforce")
        self.legend(self.active_workforce_axes, [p1])

        p1, = self.sales_axes.step(x, stats.hours_sold[-1], 'r.', label = "Sold Hours")
        p2, = self.declined_axes.step(x, stats.hours_declined[-1], 'b*', label = "Declined Hours")

        self.legend(self.sales_axes, [p1, p2])

        p1, = self.sales_money_axes.step(x, stats.profit[-1], 'r.', label = "Profit")
        p2, = self.declined_money_axes.step(x, stats.opportunity_cost[-1], 'b*', label = "Opportunity cost")

        self.legend(self.sales_money_axes, [p1, p2])

        p1, = self.workload_axes.step(x, stats.average_workload[-1], 'b*', label = "Fixed Average Workload")

        self.legend(self.workload_axes, [p1])

        for p in self.plots:
            p.canvas.draw()

class Plot(wx.Panel):
    def __init__(self, parent, id = -1, dpi = None, **kwargs):
        wx.Panel.__init__(self, parent, id=id, **kwargs)

        self.figure = mpl.figure.Figure(dpi=dpi, figsize=(9, 5))
        self.canvas = Canvas(self, -1, self.figure)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND)

        self.SetSizer(sizer)

