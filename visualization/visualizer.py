import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import random
import config
from mpl_toolkits.mplot3d import Axes3D
import time
from matplotlib.lines import Line2D

class Visualizer:
    def __init__(self, tracker):
        self.tracker = tracker

    def animate(self):
        fig = plt.figure(figsize=(16, 7))
        gs = fig.add_gridspec(1, 2, width_ratios=[1, 3])
        ax_info = fig.add_subplot(gs[0, 0])
        ax = fig.add_subplot(gs[0, 1], projection='3d')
        ax.set_xlim(*config.X_RANGE)
        ax.set_ylim(*config.Y_RANGE)
        ax.set_zlim(*config.Z_RANGE)
        ax.set_title('Ruch, wykrywanie i zestrzelenia celów (3D)')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z (wysokość)')
        ax.grid(True)

        ax_info.axis('off')
        info_text = None

        legend_elements = [
            Line2D([0], [0], marker='o', color='blue', label='Niewykryty', markerfacecolor='blue', alpha=0.4, markersize=10),
            Line2D([0], [0], marker='o', color='green', label='Wykryty', markerfacecolor='green', alpha=0.4, markersize=10),
            Line2D([0], [0], marker='o', color='gray', label='Zestrzelony', markerfacecolor='gray', alpha=0.5, markersize=10)
        ]
        ax.legend(handles=legend_elements, loc='upper right')

        scat_niew = ax.scatter([], [], [], c='blue', alpha=0.4, s=40, label='Niewykryty')
        scat_wyk = ax.scatter([], [], [], c='green', alpha=0.4, s=40, label='Wykryty')
        scat_zest = ax.scatter([], [], [], c='gray', marker='o', alpha=0.5, s=40, label='Zestrzelony')

        wyk_texts = []
        stats_text = None
        lines = []
        info_texts = []

        def get_data():
            niew_x, niew_y, niew_z = [], [], []
            wyk_x, wyk_y, wyk_z, wyk_speeds = [], [], [], []
            zest_x, zest_y, zest_z = [], [], []
            smugi = []
            for t in self.tracker.targets:
                if t.left_field:
                    continue
                elif not t.alive:
                    zest_x.append(t.x)
                    zest_y.append(t.y)
                    zest_z.append(t.z)
                elif t.is_marked:
                    wyk_x.append(t.x)
                    wyk_y.append(t.y)
                    wyk_z.append(t.z)
                    wyk_speeds.append(t.speed)
                    if hasattr(t, 'last_scanned_positions') and len(t.last_scanned_positions) > 1:
                        pts = list(t.last_scanned_positions)
                        if len(pts) > 1:
                            smugi.append([(x, y, z) for x, y, z, _ in pts])
                else:
                    niew_x.append(t.x)
                    niew_y.append(t.y)
                    niew_z.append(t.z)
            return niew_x, niew_y, niew_z, wyk_x, wyk_y, wyk_z, wyk_speeds, zest_x, zest_y, zest_z, smugi

        def update(frame):
            nonlocal info_text, wyk_texts, stats_text, lines, info_texts
            niew_x, niew_y, niew_z, wyk_x, wyk_y, wyk_z, wyk_speeds, zest_x, zest_y, zest_z, smugi = get_data()
            scat_niew._offsets3d = (niew_x, niew_y, niew_z)
            scat_wyk._offsets3d = (wyk_x, wyk_y, wyk_z)
            scat_zest._offsets3d = (zest_x, zest_y, zest_z)
            for txt in wyk_texts:
                txt.remove()
            wyk_texts = []
            for x, y, z, speed in zip(wyk_x, wyk_y, wyk_z, wyk_speeds):
                wyk_texts.append(ax.text(x, y, z, f"v={speed:.1f}", color='green', fontsize=8, alpha=0.7))
            for l in lines:
                l.remove()
            lines = []
            
            for txt in info_texts:
                try:
                    txt.remove()
                except:
                    pass
            info_texts = []
            
            shooter_stats = self.tracker.shooter.get_stats() if hasattr(self.tracker, 'shooter') else {'shots_fired': 0, 'hits': 0, 'misses': 0, 'accuracy': 0}
            
            info_lines = [
                f"Radar X: {config.X_RANGE}",
                f"Radar Y: {config.Y_RANGE}",
                f"Radar Z: {config.Z_RANGE}",
                f"Szansa wykrycia: {1-min(config.CAMOUFLAGE_RANGE):.2f}-{1-max(config.CAMOUFLAGE_RANGE):.2f}",
                f"Czas skanu: {config.DETECTION_TIME}s",
                f"Czas próby zestrzelenia: {config.SHOOT_TIME}s",
                f"Animacja: {config.ANIMATION_INTERVAL}ms",
                f"Tolerancja przewidywania: {config.PREDICTION_TOLERANCE}",
                f"Maksymalne strzały: {config.MAX_SIMULTANEOUS_SHOTS}",
                f"Na polu: {sum(1 for t in self.tracker.targets if t.alive and not t.left_field and t.x < config.X_RANGE[1])}",
                f"Wykryte: {sum(1 for t in self.tracker.targets if t.is_marked and t.alive and not t.left_field and t.x < config.X_RANGE[1])}",
                f"Zestrzelone: {sum(1 for t in self.tracker.targets if not t.alive)}",
                f"Niewykryte: {sum(1 for t in self.tracker.targets if not t.is_marked and t.alive and not t.left_field and t.x < config.X_RANGE[1])}",
                f"Opuściło pole: {sum(1 for t in self.tracker.targets if t.left_field)}",
                f"Strzały: {shooter_stats['shots_fired']}",
                f"Trafienia: {shooter_stats['hits']}",
                f"Pudła: {shooter_stats['misses']}",
                f"Celność: {shooter_stats['accuracy']:.1f}%"
            ]
            
            y_pos = 0.99
            for i, line in enumerate(info_lines):
                if "Niewykryte:" in line:
                    color = 'blue'
                    alpha = 0.8
                elif "Wykryte:" in line:
                    color = 'green'
                    alpha = 0.8
                elif "Zestrzelone:" in line:
                    color = 'gray'
                    alpha = 0.8
                else:
                    color = 'black'
                    alpha = 0.7
                
                text_obj = ax_info.text(0.5, y_pos, line, fontsize=10, color=color, va='top', ha='center', 
                                       bbox=dict(facecolor='white', alpha=alpha, edgecolor='none'), 
                                       transform=ax_info.transAxes)
                info_texts.append(text_obj)
                y_pos -= 0.06
            
            ax.set_title("")
            return scat_niew, scat_wyk, scat_zest, *lines

        anim = FuncAnimation(fig, update, interval=max(config.ANIMATION_INTERVAL, 50), blit=False, repeat=False, cache_frame_data=False, save_count=1000)
        plt.show()