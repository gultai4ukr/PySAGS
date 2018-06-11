import tkinter as tk

from base import SystolicArray
from configs.example_1 import ARRAY_SIZE, NODES_BY_CLASS, INPUT_STREAMS, CONNECTIONS


class Application(tk.Frame):

    def __init__(self, systolic_array, master=None, *args, **kwargs):
        self.systolic_array = systolic_array
        super().__init__(master, *args, **kwargs)
        self.place(x=0, y=0)
        self.visible_nodes = []
        self.create_widgets()

    def create_widgets(self):
        self.label_select_node = tk.Label(self, text="Select node")
        self.label_select_node.place(x=20, y=20)

        self.label_x = tk.Label(self, text="X=")
        self.label_x.place(x=20, y=40)
        self.entry_x = tk.Entry(self, width=6)
        self.entry_x.place(x=40, y=40)

        self.label_y = tk.Label(self, text="Y=")
        self.label_y.place(x=20, y=60)
        self.entry_y = tk.Entry(self, width=6)
        self.entry_y.place(x=40, y=60)

        self.label_steps = tk.Label(self, text="Select step")
        self.label_steps.place(x=20, y=80)

        self.button_step_backward = tk.Button(self, text="-1", command=self.step_backward)
        self.button_step_backward.place(x=20, y=100, width=25, height=20)

        self.step = tk.IntVar()
        self.entry_step = tk.Entry(self, width=4, textvariable=self.step)
        self.entry_step.place(x=46, y=100)

        self.button_step_forward = tk.Button(self, text="+1", command=self.step_forward)
        self.button_step_forward.place(x=85, y=100, width=25, height=20)

        self.button_simulate = tk.Button(self, text="Simulate", command=self.simulate)
        self.button_simulate.place(x=20, y=120, width=90)

    def simulate(self):
        if self.step.get() < self.systolic_array.current_step:
            self.systolic_array.reset()
        self.systolic_array.iterate(self.step.get() - self.systolic_array.current_step)

        r = int(self.entry_y.get())
        c = int(self.entry_x.get())
        for node in self.visible_nodes:
            node.destroy()
        self.visible_nodes = []
        show_indexes = [
            (r-1, c-1), (r-1, c), (r-1, c+1),
            (r, c-1), (r, c), (r, c+1),
            (r+1, c-1), (r+1, c), (r+1, c+1),
        ]
        r0 = max(0, r-1)
        c0 = max(0, c-1)
        for r, c in show_indexes:
            if r < 0 or r >= self.systolic_array.n or c < 0 or c >= self.systolic_array.m:
                continue
            sz = 160
            frame = tk.Frame(
                self, width=sz, height=sz,
                highlightbackground='black',
                highlightthickness=1
            )
            gap = 40
            start = (250 + (sz + gap) * (c - c0), 30 + (sz + gap) * (r - r0))
            end = tuple(c + sz for c in start)
            frame.place(x=start[0], y=start[1], width=sz, height=sz)
            self.visible_nodes.append(frame)
            for i, (k, v) in enumerate(self.systolic_array.array[r][c].data.items()):
                label = tk.Label(frame, text="{}={}".format(k, v))
                label.pack()  # place(x=0, y=i*20)
            # todo: add arrows on connections

    def step_forward(self):
        self.step.set(self.step.get() + 1)
        self.simulate()

    def step_backward(self):
        self.step.set(max(0, self.step.get() - 1))
        self.simulate()


if __name__ == '__main__':
    root = tk.Tk()
    SCREEN_SIZE = {
        'width': root.winfo_screenwidth(),
        'height': root.winfo_screenheight()
    }
    root.geometry("{width}x{height}".format(**SCREEN_SIZE))
    app = Application(
        SystolicArray(ARRAY_SIZE, NODES_BY_CLASS, INPUT_STREAMS, CONNECTIONS),
        master=root, **SCREEN_SIZE
    )
    app.mainloop()
