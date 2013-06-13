import wx
import wx.aui
import matplotlib as mpl
import strategies

from threading import Thread
from time import time

mpl.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as Canvas

from sim import Simulation, ResultAggregator, batch_run

new_run_event = wx.NewId()
update_aggregate_event = wx.NewId()
update_plot_event = wx.NewId()

def bind_event(window, id, cb):
    window.Connect(-1, -1, id, cb)

def fire_event(to, type, data):
    ev = wx.PyEvent()
    ev.SetEventType(type)
    ev.data = data

    wx.PostEvent(to, ev)

class Window(object):

    def __init__(self):
        self.app = wx.PySimpleApp()
        self.frame = MainFrame()
        self.app.MainLoop()


class MainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Sim')
        bind_event(self, update_aggregate_event, self.update_aggregate)

        self.last_render = time()
        self.aggregator = ResultAggregator()
        self.aggregator.set_observer(self)

        sizer = wx.GridSizer(2, 2)
        self.sizer = sizer;
        self.plots = []

        buttons = Buttons(self, self.aggregator)
        buttons.Show()

        self.cost_plot = self.add_plot('$', 'Costo de Oportunidad')
        self.profit_plot = self.add_plot('$', 'Ganancia')
        self.resource_usage_plot = self.add_plot('Devs', '# devs activos')

        sizer.Fit(self)
        self.SetSizer(sizer)

        self.Show()

    def add_plot(self, ylabel, title):
        plot = Plot(self)
        axes = plot.figure.gca(
                xlim = (0, 7),
                adjustable = 'box',
                ylabel = ylabel)
        axes.set_autoscalex_on(False)
        axes.hold(False)

        plot.figure.suptitle(title)

        self.sizer.Add(plot, 0, wx.ALIGN_CENTER)
        self.plots.append(plot)
        return plot.figure.gca()

    def update(self, aggregate):
        now = time()
        if now - self.last_render < 1:
            return

        fire_event(self, update_aggregate_event, None)
        self.last_render = now

    def batch_done(self, aggregate):
        fire_event(self, update_aggregate_event, None)

    def update_aggregate(self, ev):

        for p in self.plots:
            p.figure.gca().cla()

        self.cost_plot.boxplot(self.aggregator.cost)
        self.cost_plot.set_ylabel('$')

        self.profit_plot.boxplot(self.aggregator.profit)
        self.profit_plot.set_ylabel('$')

        self.resource_usage_plot.boxplot(self.aggregator.resource_usage)
        self.resource_usage_plot.set_ylabel('Devs')

        for p in self.plots:
            p.canvas.draw()

        self.SetSize(self.Size)


class Buttons(wx.Frame):
    def __init__(self, parent, aggregator, id = -1, **kwargs):
        wx.Frame.__init__(self, parent, id = id, **kwargs)

        self.aggregator = aggregator
        sizer = wx.BoxSizer(wx.VERTICAL)

        batch_id = wx.NewId()
        sizer.Add(wx.Button(self, batch_id, 'Batch'), 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.Bind(wx.EVT_BUTTON, self.batch_event, id = batch_id)

        self.sizer = wx.GridSizer(3, 2)

        self.add_button('Precio - 0 devs', self.price_0)
        self.add_button('Facturacion - 0 devs', self.cost_0)

        self.add_button('Precio - 2 devs', self.price_2)
        self.add_button('Facturacion - 2 devs', self.cost_2)

        self.add_button('Precio - 4 devs', self.price_4)
        self.add_button('Facturacion - 4 devs', self.cost_4)

        self.add_button('Precio - 6 devs', self.price_6)
        self.add_button('Facturacion - 6 devs', self.cost_6)

        sizer.Add(self.sizer, 0, wx.ALIGN_CENTER_HORIZONTAL)

        save_id = wx.NewId()
        sizer.Add(wx.Button(self, save_id, 'Save output to file'), 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.Bind(wx.EVT_BUTTON, self.save_event, id = save_id)

        self.SetSizer(sizer)
        sizer.Layout()

    def save_event(self, ev):
        self.aggregator.save('out-' + str(int(time())))

    def add_button(self, text, cb):
        id = wx.NewId()
        self.sizer.Add(wx.Button(self, id, text), 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.Bind(wx.EVT_BUTTON, cb, id = id)

    def price_0(self, ev):
        self.run_event(strategies.price_hours, 0)

    def price_2(self, ev):
        self.run_event(strategies.price_hours, 2)

    def price_4(self, ev):
        self.run_event(strategies.price_hours, 4)

    def price_6(self, ev):
        self.run_event(strategies.price_hours, 6)

    def cost_0(self, ev):
        self.run_event(strategies.cost_price, 0)

    def cost_2(self, ev):
        self.run_event(strategies.cost_price, 2)

    def cost_4(self, ev):
        self.run_event(strategies.cost_price, 4)

    def cost_6(self, ev):
        self.run_event(strategies.cost_price, 6)

    def batch_event(self, ev):
        Thread(target = lambda: batch_run(self.aggregator)).start()

    def run_event(self, strategy, reserved):
        sim = Simulation(self.aggregator, strategy, reserved, 0.2)

        frame = RunFrame(sim.stats)
        frame.Show()

        Thread(target = sim.run).start()

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


