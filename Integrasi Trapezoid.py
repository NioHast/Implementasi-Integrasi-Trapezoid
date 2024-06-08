import timeit
import numpy as np
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

class PiApproximation:
    def __init__(self):
        self.pi_reference = 3.14159265358979323846
        self.N_values = np.array([10, 100, 1000, 10000])
        self.pi_approximations = []
        self.execution_times = []
        self.rms_errors = []

    def f(self, x):
        return 4 / (1 + x**2)

    def trapezoid_integration(self, a, b, N):
        delta_x = (b - a) / N
        x = np.linspace(a, b, N+1)
        y = self.f(x)
        integral = (delta_x / 2) * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])
        return integral

    def calculate_rms_error(self, pi_approx):
        return np.sqrt(mean_squared_error([self.pi_reference] * len(pi_approx), pi_approx))

    def run(self):
        num_repeats = 1000
        for N in self.N_values:
            timer = timeit.Timer(lambda: self.trapezoid_integration(0, 1, N))
            execution_times = timer.repeat(repeat=num_repeats, number=1)
            avg_execution_time = np.mean(execution_times)
            pi_approx = self.trapezoid_integration(0, 1, N)
            
            self.pi_approximations.append(pi_approx)
            self.execution_times.append(avg_execution_time)

            rms_error = self.calculate_rms_error([pi_approx])
            self.rms_errors.append(rms_error)

            print(f"Jumlah Sub-Interval (N) = {N}:")
            print(f"Hasil Integrasi = {pi_approx}")
            print(f"Rata-Rata waktu Eksekusi = {avg_execution_time:.8f} detik")
            print(f"Galat RMS = {rms_error}")
            rms_error_percent = (abs(self.pi_reference - pi_approx) / self.pi_reference) * 100
            print(f"Presentase Galat RMS = {rms_error_percent:.10f}%\n")

        print(f"Nilai referensi pi = {self.pi_reference}")

class Plotting:
    def __init__(self, pi_app):
        self.pi_app = pi_app
        self.fig, self.axs = plt.subplots(figsize=(13, 6))
        self.plot_index = 0
        self.plot_types = ['RMS Error', 'Execution Time']
        self.update_plot()

        plt.subplots_adjust(bottom=0.2)

        axprev = plt.axes([0.4, 0.05, 0.1, 0.075])
        axnext = plt.axes([0.5, 0.05, 0.1, 0.075])
        self.prev_button = Button(axprev, 'Previous')
        self.next_button = Button(axnext, 'Next')

        self.prev_button.on_clicked(self.show_previous_plot)
        self.next_button.on_clicked(self.show_next_plot)

        plt.show()

    def update_plot(self):
        self.axs.clear()

        if self.plot_types[self.plot_index] == 'RMS Error':
            self.axs.plot(self.pi_app.N_values, self.pi_app.rms_errors, marker='o', color='green', label='RMS Error')
            self.axs.set_xscale('log')
            self.axs.set_xlabel('Jumlah Sub-Interval (N)')
            self.axs.set_ylabel('Galat RMS')
            self.axs.set_title('Galat RMS vs Jumlah Sub-Interval')
            self.axs.legend()
            self.axs.grid(True)
        elif self.plot_types[self.plot_index] == 'Execution Time':
            self.axs.plot(self.pi_app.N_values, self.pi_app.execution_times, marker='o', color='purple', label='Execution Time')
            self.axs.set_xscale('log')
            self.axs.set_yscale('log')
            self.axs.set_xlabel('Jumlah Sub-Interval (N)')
            self.axs.set_ylabel('Waktu Eksekusi (Detik)')
            self.axs.set_title('Waktu Eksekusi vs Jumlah Sub-Interval')
            self.axs.legend()
            self.axs.grid(True)

        self.fig.canvas.draw_idle()

    def show_previous_plot(self, event):
        self.plot_index = (self.plot_index - 1) % len(self.plot_types)
        self.update_plot()

    def show_next_plot(self, event):
        self.plot_index = (self.plot_index + 1) % len(self.plot_types)
        self.update_plot()

pi_app = PiApproximation()
pi_app.run()
plotting = Plotting(pi_app)