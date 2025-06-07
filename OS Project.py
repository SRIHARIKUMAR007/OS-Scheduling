import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class DiskSchedulingAlgorithms:
    """Core algorithms for disk scheduling"""
    
    @staticmethod
    def fcfs(requests, initial_head=0):
        """First Come First Serve"""
        sequence = [initial_head]
        total_seek_time = 0
        current_head = initial_head
        
        for request in requests:
            seek_time = abs(request - current_head)
            total_seek_time += seek_time
            current_head = request
            sequence.append(current_head)
        
        return sequence, total_seek_time
    
    @staticmethod
    def sstf(requests, initial_head=0):
        """Shortest Seek Time First"""
        sequence = [initial_head]
        total_seek_time = 0
        current_head = initial_head
        remaining_requests = requests.copy()
        
        while remaining_requests:
            # Find closest request
            closest_request = min(remaining_requests, 
                                key=lambda x: abs(x - current_head))
            
            seek_time = abs(closest_request - current_head)
            total_seek_time += seek_time
            current_head = closest_request
            sequence.append(current_head)
            remaining_requests.remove(closest_request)
        
        return sequence, total_seek_time
    
    @staticmethod
    def scan(requests, initial_head=0, disk_size=200, direction="right"):
        """SCAN (Elevator) Algorithm"""
        sequence = [initial_head]
        total_seek_time = 0
        current_head = initial_head
        
        # Separate requests based on direction
        left_requests = sorted([r for r in requests if r < current_head], reverse=True)
        right_requests = sorted([r for r in requests if r >= current_head])
        
        if direction == "right":
            # Service right requests first
            for request in right_requests:
                seek_time = abs(request - current_head)
                total_seek_time += seek_time
                current_head = request
                sequence.append(current_head)
            
            # Move to end if there were right requests
            if right_requests and left_requests:
                seek_time = abs(disk_size - 1 - current_head)
                total_seek_time += seek_time
                current_head = disk_size - 1
                sequence.append(current_head)
            
            # Service left requests
            for request in left_requests:
                seek_time = abs(request - current_head)
                total_seek_time += seek_time
                current_head = request
                sequence.append(current_head)
        
        else:  # direction == "left"
            # Service left requests first
            for request in left_requests:
                seek_time = abs(request - current_head)
                total_seek_time += seek_time
                current_head = request
                sequence.append(current_head)
            
            # Move to beginning if there were left requests
            if left_requests and right_requests:
                seek_time = abs(0 - current_head)
                total_seek_time += seek_time
                current_head = 0
                sequence.append(current_head)
            
            # Service right requests
            for request in right_requests:
                seek_time = abs(request - current_head)
                total_seek_time += seek_time
                current_head = request
                sequence.append(current_head)
        
        return sequence, total_seek_time
    
    @staticmethod
    def c_scan(requests, initial_head=0, disk_size=200):
        """Circular SCAN Algorithm"""
        sequence = [initial_head]
        total_seek_time = 0
        current_head = initial_head
        
        # Separate requests
        left_requests = sorted([r for r in requests if r < current_head])
        right_requests = sorted([r for r in requests if r >= current_head])
        
        # Service right requests first
        for request in right_requests:
            seek_time = abs(request - current_head)
            total_seek_time += seek_time
            current_head = request
            sequence.append(current_head)
        
        # Move to end, then to beginning
        if right_requests and left_requests:
            # Go to end
            seek_time = abs(disk_size - 1 - current_head)
            total_seek_time += seek_time
            current_head = disk_size - 1
            sequence.append(current_head)
            
            # Jump to beginning
            seek_time = abs(0 - (disk_size - 1))
            total_seek_time += seek_time
            current_head = 0
            sequence.append(current_head)
        
        # Service left requests
        for request in left_requests:
            seek_time = abs(request - current_head)
            total_seek_time += seek_time
            current_head = request
            sequence.append(current_head)
        
        return sequence, total_seek_time


class DiskSchedulingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Disk Scheduling Simulator")
        self.root.geometry("900x700")
        
        # Variables
        self.algorithms = DiskSchedulingAlgorithms()
        self.results = {}
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Input Parameters", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Algorithm selection
        ttk.Label(input_frame, text="Algorithm:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.algorithm_var = tk.StringVar(value="SSTF")
        self.algorithm_combo = ttk.Combobox(input_frame, textvariable=self.algorithm_var,
                                          values=["FCFS", "SSTF", "SCAN", "C-SCAN"])
        self.algorithm_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        
        # Initial head position
        ttk.Label(input_frame, text="Initial Head Position:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.head_var = tk.StringVar(value="53")
        ttk.Entry(input_frame, textvariable=self.head_var, width=10).grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Disk size
        ttk.Label(input_frame, text="Disk Size:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.disk_size_var = tk.StringVar(value="200")
        ttk.Entry(input_frame, textvariable=self.disk_size_var, width=10).grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Direction for SCAN
        ttk.Label(input_frame, text="SCAN Direction:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.direction_var = tk.StringVar(value="right")
        direction_combo = ttk.Combobox(input_frame, textvariable=self.direction_var,
                                     values=["left", "right"], width=10)
        direction_combo.grid(row=3, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Requests input
        ttk.Label(input_frame, text="Disk Requests:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.requests_var = tk.StringVar(value="98,183,37,122,14,124,65,67")
        requests_entry = ttk.Entry(input_frame, textvariable=self.requests_var, width=40)
        requests_entry.grid(row=4, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=2)
        
        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="Simulate", command=self.simulate).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Compare All", command=self.compare_algorithms).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_results).pack(side=tk.LEFT, padx=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Text widget for results
        self.results_text = tk.Text(results_frame, height=8, width=50)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Plot frame
        plot_frame = ttk.LabelFrame(main_frame, text="Visualization", padding="10")
        plot_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Matplotlib figure
        self.figure, self.ax = plt.subplots(figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.figure, master=plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
    def get_inputs(self):
        """Get and validate inputs"""
        try:
            initial_head = int(self.head_var.get())
            disk_size = int(self.disk_size_var.get())
            requests_str = self.requests_var.get().strip()
            requests = [int(x.strip()) for x in requests_str.split(',') if x.strip()]
            algorithm = self.algorithm_var.get()
            direction = self.direction_var.get()
            
            # Validate inputs
            if not requests:
                raise ValueError("No requests provided")
            
            if any(r < 0 or r >= disk_size for r in requests):
                raise ValueError(f"All requests must be between 0 and {disk_size-1}")
            
            if initial_head < 0 or initial_head >= disk_size:
                raise ValueError(f"Initial head position must be between 0 and {disk_size-1}")
            
            return initial_head, disk_size, requests, algorithm, direction
        
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return None
    
    def simulate(self):
        """Simulate selected algorithm"""
        inputs = self.get_inputs()
        if not inputs:
            return
        
        initial_head, disk_size, requests, algorithm, direction = inputs
        
        # Execute algorithm
        if algorithm == "FCFS":
            sequence, seek_time = self.algorithms.fcfs(requests, initial_head)
        elif algorithm == "SSTF":
            sequence, seek_time = self.algorithms.sstf(requests, initial_head)
        elif algorithm == "SCAN":
            sequence, seek_time = self.algorithms.scan(requests, initial_head, disk_size, direction)
        elif algorithm == "C-SCAN":
            sequence, seek_time = self.algorithms.c_scan(requests, initial_head, disk_size)
        
        # Store results
        self.results[algorithm] = {
            'sequence': sequence,
            'seek_time': seek_time,
            'avg_seek_time': seek_time / len(requests)
        }
        
        # Display results
        self.display_results(algorithm)
        self.plot_results(algorithm, sequence)
    
    def compare_algorithms(self):
        """Compare all algorithms"""
        inputs = self.get_inputs()
        if not inputs:
            return
        
        initial_head, disk_size, requests, _, direction = inputs
        
        algorithms = ["FCFS", "SSTF", "SCAN", "C-SCAN"]
        self.results = {}
        
        for algo in algorithms:
            if algo == "FCFS":
                sequence, seek_time = self.algorithms.fcfs(requests, initial_head)
            elif algo == "SSTF":
                sequence, seek_time = self.algorithms.sstf(requests, initial_head)
            elif algo == "SCAN":
                sequence, seek_time = self.algorithms.scan(requests, initial_head, disk_size, direction)
            elif algo == "C-SCAN":
                sequence, seek_time = self.algorithms.c_scan(requests, initial_head, disk_size)
            
            self.results[algo] = {
                'sequence': sequence,
                'seek_time': seek_time,
                'avg_seek_time': seek_time / len(requests)
            }
        
        self.display_comparison()
        self.plot_comparison()
    
    def display_results(self, algorithm):
        """Display results for single algorithm"""
        self.results_text.delete(1.0, tk.END)
        
        result = self.results[algorithm]
        
        output = f"=== {algorithm} Algorithm Results ===\n"
        output += f"Sequence: {' -> '.join(map(str, result['sequence']))}\n"
        output += f"Total Seek Time: {result['seek_time']}\n"
        output += f"Average Seek Time: {result['avg_seek_time']:.2f}\n"
        output += f"Number of Requests: {len(result['sequence']) - 1}\n"
        
        self.results_text.insert(tk.END, output)
    
    def display_comparison(self):
        """Display comparison of all algorithms"""
        self.results_text.delete(1.0, tk.END)
        
        output = "=== Algorithm Comparison ===\n\n"
        
        for algo, result in self.results.items():
            output += f"{algo}:\n"
            output += f"  Total Seek Time: {result['seek_time']}\n"
            output += f"  Average Seek Time: {result['avg_seek_time']:.2f}\n"
            output += f"  Sequence: {' -> '.join(map(str, result['sequence']))}\n\n"
        
        # Find best algorithm
        best_algo = min(self.results.keys(), key=lambda x: self.results[x]['seek_time'])
        output += f"Best Algorithm: {best_algo} (Lowest total seek time: {self.results[best_algo]['seek_time']})\n"
        
        self.results_text.insert(tk.END, output)
    
    def plot_results(self, algorithm, sequence):
        """Plot results for single algorithm"""
        self.ax.clear()
        
        x_positions = range(len(sequence))
        self.ax.plot(x_positions, sequence, 'bo-', linewidth=2, markersize=8)
        
        self.ax.set_title(f'{algorithm} Disk Scheduling - Seek Sequence')
        self.ax.set_xlabel('Request Order')
        self.ax.set_ylabel('Track Number')
        self.ax.grid(True, alpha=0.3)
        
        # Annotate points
        for i, pos in enumerate(sequence):
            self.ax.annotate(f'{pos}', (i, pos), textcoords="offset points", 
                           xytext=(0,10), ha='center')
        
        # Add seek time info
        seek_time = self.results[algorithm]['seek_time']
        self.ax.text(0.02, 0.98, f'Total Seek Time: {seek_time}', 
                    transform=self.ax.transAxes, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        self.canvas.draw()
    
    def plot_comparison(self):
        """Plot comparison of all algorithms"""
        self.ax.clear()
        
        algorithms = list(self.results.keys())
        seek_times = [self.results[algo]['seek_time'] for algo in algorithms]
        
        bars = self.ax.bar(algorithms, seek_times, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'])
        
        self.ax.set_title('Algorithm Comparison - Total Seek Time')
        self.ax.set_ylabel('Total Seek Time')
        self.ax.set_xlabel('Algorithm')
        
        # Add value labels on bars
        for bar, seek_time in zip(bars, seek_times):
            height = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                        f'{seek_time}', ha='center', va='bottom')
        
        self.canvas.draw()
    
    def clear_results(self):
        """Clear all results"""
        self.results_text.delete(1.0, tk.END)
        self.ax.clear()
        self.canvas.draw()
        self.results = {}


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = DiskSchedulingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()