# System Obrony Powietrznej - Symulator 3D

## Opis Projektu

System Obrony Powietrznej to symulator 3D, który demonstruje działanie radaru, wykrywanie celów powietrznych oraz ich zestrzeliwanie w czasie rzeczywistym. Projekt wykorzystuje programowanie współbieżne, metaprogramowanie oraz algorytmy przewidywania trajektorii.

## Założenia Projektu

### Cel Główny
Symulacja realistycznego systemu obrony powietrznej z następującymi komponentami:
- **Radar 3D** - skanowanie przestrzeni powietrznej
- **Wykrywanie celów** - z uwzględnieniem kamuflażu
- **Przewidywanie trajektorii** - algorytmy predykcji pozycji
- **System strzelania** - zestrzeliwanie na podstawie przewidywań
- **Wizualizacja 3D** - interaktywny interfejs graficzny

### Wymagania Techniczne
- **Programowanie współbieżne** - wielowątkowe przetwarzanie
- **Metaprogramowanie** - dynamiczne tworzenie typów celów
- **Algorytmy predykcji** - przewidywanie pozycji celów
- **Wizualizacja w czasie rzeczywistym** - animacja 3D

## Architektura Systemu

### Struktura Katalogów
```
AirDefenceSystem3DSimulator/
├── config.py                 # Konfiguracja systemu
├── main.py                   # Główny punkt wejścia
├── core/                     # Logika biznesowa
│   ├── tracker.py           # Śledzenie celów
│   ├── targets/             # Zarządzanie celami
│   │   ├── air_target.py    # Klasa bazowa celu
│   │   ├── generator.py     # Generowanie celów
│   │   ├── target_factory.py # Fabryka typów celów
│   │   └── target_creator.py # Tworzenie celów
│   ├── shooting/            # System strzelania
│   │   ├── shooter.py       # Logika strzelania
│   │   └── predictor.py     # Przewidywanie pozycji
│   ├── detection/           # Wykrywanie celów
│   │   └── marker.py        # Oznaczanie celów
│   └── movetypes/           # Typy ruchu
│       ├── straight.py      # Ruch prostoliniowy
│       ├── eight.py         # Ruch po ósemce
│       └── sine.py          # Ruch sinusoidalny
├── simulation/              # Pętle symulacji
│   ├── move_loop.py         # Pętla ruchu
│   ├── scan_loop.py         # Pętla skanowania
│   ├── detect_loop.py       # Pętla wykrywania
│   └── shoot_loop.py        # Pętla strzelania
└── visualization/           # Wizualizacja
    └── visualizer.py        # Interfejs 3D
```

## Diagram Klas

![ClassDiagram (2)](https://github.com/user-attachments/assets/72c851d2-5db0-4cb8-aa29-93f09396694c)


## Działanie Programu

### 1. Inicjalizacja
```python
# main.py - główny punkt wejścia
targets = generate_targets(config)  # Generowanie celów
tracker = Tracker(targets)          # Tworzenie tracker'a
shooter = Shooter(tracker)          # Tworzenie systemu strzelania
visualizer = Visualizer(tracker)    # Tworzenie wizualizacji
```

### 2. Pętle Współbieżne
Program uruchamia 4 wątki działające równolegle:

- **move_loop** - aktualizuje pozycje celów
- **scan_loop** - skanuje pozycje celów
- **detect_loop** - wykrywa nowe cele
- **shoot_loop** - zestrzeliwuje wykryte cele

### 3. Proces Wykrywania
1. **Skanowanie** - radar skanuje pozycje wszystkich celów
2. **Wykrywanie** - cele są wykrywane z prawdopodobieństwem zależnym od kamuflażu
3. **Oznaczanie** - wykryte cele są oznaczane do zestrzelenia

### 4. Proces Strzelania
1. **Przewidywanie** - na podstawie historii pozycji przewiduje się przyszłą pozycję
2. **Sprawdzanie** - porównuje przewidzianą pozycję z rzeczywistą
3. **Zestrzelenie** - jeśli pozycje się zgadzają, cel zostaje zestrzelony

## Przykłady Kodu

### Konfiguracja Systemu (config.py)
```python
# Stałe konfiguracyjne systemu obrony powietrznej
ANIMATION_INTERVAL = 100  # ms - interwał animacji
NUM_TARGETS = 30          # liczba celów
X_RANGE = (0, 4000)       # zakres osi X
Y_RANGE = (0, 3000)       # zakres osi Y
Z_RANGE = (0, 1500)       # zakres osi Z
SPEEDS = [2, 4]           # zakres prędkości
CAMOUFLAGE_RANGE = (0.7, 0.90)  # zakres kamuflażu
DETECTION_TIME = 2        # czas wykrywania (s)
SHOOT_TIME = 1            # czas strzelania (s)
PREDICTION_TOLERANCE = 30.0     # tolerancja przewidywania
MAX_SIMULTANEOUS_SHOTS = 3      # maksymalne strzały
```

### Główny Program (main.py)
```python
import threading
import time
import config
from core.targets.generator import generate_targets
from core.tracker import Tracker
from core.shooting.shooter import Shooter
from visualization.visualizer import Visualizer
from simulation.move_loop import move_loop
from simulation.scan_loop import scan_loop
from simulation.detect_loop import detect_loop
from simulation.shoot_loop import shoot_loop

def main():
    targets = generate_targets(config)
    tracker = Tracker(targets)
    shooter = Shooter(tracker)
    tracker.shooter = shooter
    visualizer = Visualizer(tracker)

    # Uruchomienie wątków współbieżnych
    move_thread = threading.Thread(target=move_loop, args=(tracker, stop_threads), daemon=True)
    scan_thread = threading.Thread(target=scan_loop, args=(tracker, stop_threads), daemon=True)
    detect_thread = threading.Thread(target=detect_loop, args=(tracker, stop_threads), daemon=True)
    shoot_thread = threading.Thread(target=shoot_loop, args=(tracker, shooter, stop_threads), daemon=True)
    
    move_thread.start()
    scan_thread.start()
    detect_thread.start()
    shoot_thread.start()

    visualizer.animate()
```

## Metaprogramowanie

System wykorzystuje metaprogramowanie do dynamicznego tworzenia typów celów z różnymi trajektoriami:

```python
def create_target_type(name, speed, camouflage=0.0, move_type='straight'):
    """
    Metaprogramowanie: dynamiczne tworzenie podklas z różnymi trajektoriami
    """
    from core.targets.air_target import AirTarget
    base = AirTarget
    
    def move(self):
        if move_type == 'eight':
            move_eight(self)
        elif move_type == 'sine':
            move_sine(self)
        else:
            move_straight(self)
    
    return type(name, (base,), {
        "default_speed": speed, 
        "default_camouflage": camouflage, 
        "move": move
    })
```

## Programowanie Współbieżne

System wykorzystuje `threading.Lock` do bezpiecznego dostępu do współdzielonych zasobów:

```python
class Tracker:
    def __init__(self, targets):
        self.targets = targets
        self.lock = threading.Lock()

    def update_positions(self):
        with self.lock:  # Bezpieczny dostęp do listy celów
            for target in self.targets:
                if target.alive:
                    target.move()
```

## Algorytmy Predykcji

System wykorzystuje zaawansowane algorytmy do przewidywania pozycji celów:

```python
def predict_position(positions, timestamps, current_time):
    """Przewiduje przyszłą pozycję na podstawie historii"""
    if len(positions) < 3:
        return None
    
    # Obliczanie prędkości
    velocities = []
    for i in range(1, len(positions)):
        dt = timestamps[i] - timestamps[i-1]
        if dt > 0:
            vx = (positions[i][0] - positions[i-1][0]) / dt
            vy = (positions[i][1] - positions[i-1][1]) / dt
            vz = (positions[i][2] - positions[i-1][2]) / dt
            velocities.append((vx, vy, vz))
    
    if not velocities:
        return None
    
    # Średnia prędkość
    avg_vx = sum(v[0] for v in velocities) / len(velocities)
    avg_vy = sum(v[1] for v in velocities) / len(velocities)
    avg_vz = sum(v[2] for v in velocities) / len(velocities)
    
    # Przewidywanie pozycji
    dt = current_time - timestamps[-1]
    predicted_x = positions[-1][0] + avg_vx * dt
    predicted_y = positions[-1][1] + avg_vy * dt
    predicted_z = positions[-1][2] + avg_vz * dt
    
    return (predicted_x, predicted_y, predicted_z)
```

## Wizualizacja

System oferuje interaktywną wizualizację 3D z:
- **Kolorystyką celów**: niebieski (niewykryty), zielony (wykryty), szary (zestrzelony)
- **Panel informacyjny**: statystyki w czasie rzeczywistym
- **Animacja 3D**: płynna animacja ruchu celów
- **Legenda**: opis typów celów

## Instalacja i Uruchomienie

### Wymagania
```bash
pip install matplotlib numpy
```

### Uruchomienie
```bash
python main.py
```

## Statystyki Systemu

Program wyświetla następujące statystyki w czasie rzeczywistym:
- **Radar**: zakresy X, Y, Z
- **Wykrywanie**: szansa wykrycia, czas skanu
- **Strzelanie**: czas próby, tolerancja, maksymalne strzały
- **Cele**: na polu, wykryte, zestrzelone, niewykryte, opuściły pole
- **Skuteczność**: strzały, trafienia, pudła, celność

## Zrzut Ekranu

![image](https://github.com/user-attachments/assets/dc9268b5-14fd-46da-95cd-ea4206bf16a6)


## Podsumowanie

System Obrony Powietrznej demonstruje zaawansowane techniki programowania:
- **Programowanie współbieżne** - wielowątkowe przetwarzanie
- **Metaprogramowanie** - dynamiczne tworzenie typów
- **Algorytmy predykcji** - przewidywanie trajektorii
- **Wizualizacja 3D** - interaktywny interfejs
- **Architektura modułowa** - czytelna struktura kodu

Projekt stanowi doskonały przykład praktycznego zastosowania zaawansowanych koncepcji programistycznych w realistycznej symulacji systemu obrony powietrznej. 
