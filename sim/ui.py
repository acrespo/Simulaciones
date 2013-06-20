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
        wx.Frame.__init__(self, None, -1, 'Funciones Objetivo')
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

        legend_sizer = wx.BoxSizer(wx.VERTICAL)
        legend_sizer.Add(wx.StaticText(self, label = 'Leyenda'))
        legend_sizer.Add(wx.StaticText(self, label = '\t 1 - Precio (0 Devs)'))
        legend_sizer.Add(wx.StaticText(self, label = '\t 2 - Precio (2 Devs)'))
        legend_sizer.Add(wx.StaticText(self, label = '\t 3 - Precio (4 Devs)'))
        legend_sizer.Add(wx.StaticText(self, label = '\t 4 - Precio (6 Devs)'))
        legend_sizer.Add(wx.StaticText(self, label = '\t 5 - Facturacion (0 Devs)'))
        legend_sizer.Add(wx.StaticText(self, label = '\t 6 - Facturacion (2 Devs)'))
        legend_sizer.Add(wx.StaticText(self, label = '\t 7 - Facturacion (4 Devs)'))
        legend_sizer.Add(wx.StaticText(self, label = '\t 8 - Facturacion (6 Devs)'))
        sizer.Add(legend_sizer, 1, wx.EXPAND)

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

        self.cost_plot.boxplot(self.aggregator.cost, sym = '')
        self.cost_plot.set_ylabel('$')

        self.profit_plot.boxplot(self.aggregator.profit, sym = '')
        self.profit_plot.set_ylabel('$')

        self.resource_usage_plot.boxplot(self.aggregator.resource_usage, sym = '')
        self.resource_usage_plot.set_ylabel('Devs')

        for p in self.plots:
            p.canvas.draw()

        self.SetSize(self.Size)


class Buttons(wx.Frame):
    def __init__(self, parent, aggregator, id = -1, **kwargs):
        wx.Frame.__init__(self, parent, title = 'Control', id = id, **kwargs)

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
        wx.Frame.__init__(self, None, -1, 'Simulacion')

        stats.set_observer(self)
        self.sizer = wx.GridSizer(4, 2)
        self.plots = []

        self.active_workforce_axes = self.add_plot(stats, "Devs").figure.gca()

        self.sales_plot = self.add_plot(stats, "HH")

        self.sales_money_plot = self.add_plot(stats, "$")

        self.workload_plot = self.add_plot(stats, "HH")

        self.SetSizer(self.sizer)
        self.sizer.Fit(self)

        bind_event(self, update_plot_event, self.update_plot)

    def get_axes(self, plot, stats, ylabel):

        plot.figure.clear()
        axes = plot.figure.gca(
                xlim = (stats.warm_up / 3, stats.runs / 3),
                adjustable = 'box',
                xlabel = "Trimester",
                ylabel = ylabel)
        axes.set_autoscalex_on(False)

        return axes

    def add_plot(self, stats, ylabel):
        plot = Plot(self)
        self.get_axes(plot, stats, ylabel)

        self.sizer.Add(plot)
        self.plots.append(plot)
        return plot

    def end_month(self, stats):
        fire_event(self, update_plot_event, stats)

    def legend(self, axes, lines):
        axes.legend(lines, [l.get_label() for l in lines])

    def update_plot(self, ev):
        stats = ev.data
        if stats.current_step <= stats.warm_up or stats.current_step % 3:
            return None

        x = (stats.current_step / 3) + 1
        x_r = range(stats.warm_up / 3, stats.current_step / 3)

        p1,  = self.active_workforce_axes.step(x, sum(stats.active_workforce[-3:]) / 3.0, 'g*', label = "Devs Activos")
        self.legend(self.active_workforce_axes, [p1])

        trimesterify = lambda d: [sum(d[r:r+3]) for r in range(0, stats.current_step - stats.warm_up, 3)]

        axes = self.get_axes(self.sales_plot, stats, 'HH')
        hours_sold = trimesterify(stats.hours_sold)

        p1 = axes.bar(x_r, hours_sold, color = 'g', label = "Horas vendidas")
        p2 = axes.bar(x_r, trimesterify(stats.hours_declined), color = 'r', bottom = hours_sold, label = "Horas rechazadas")
        self.legend(axes, [p1, p2])

        axes = self.get_axes(self.sales_money_plot, stats, '$')
        profit = trimesterify(stats.profit)

        p1 = axes.bar(x_r, profit, color = 'g', label = "Ganancia")
        p2 = axes.bar(x_r, trimesterify(stats.opportunity_cost),  bottom = profit, color = 'r', label = "Costo de oportunidad")
        self.legend(axes, [p1, p2])

        axes = self.get_axes(self.workload_plot, stats, 'HH')
        p1 = axes.bar(x_r, trimesterify(stats.average_workload), label = "Trabajo Comprometido Promedio")
        self.legend(axes, [p1])

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


