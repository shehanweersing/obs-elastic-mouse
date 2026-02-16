#  SmoothStream: Elastic Mouse Tracker for OBS (tracking image(window)according to mouse point)

##  Want Zoom & Follow?
If you want the screen to Zoom and Track the mouse point instead of just an overlay, 
I created another repo for that! Check it out here: **[zoom-track-obs](https://github.com/shehanweersing/zoom-track-obs)**

> A lightweight, Python-based mouse tracker for OBS Studio that actually works. 
> Features cinematic "elastic" movement using Linear Interpolation (Lerp).

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![OBS](https://img.shields.io/badge/OBS-Studio-white) ![Status](https://img.shields.io/badge/Status-Active-brightgreen)

##  The Story (Why I built this)
I'm an undergraduate student, and I recently wanted to add a mouse tracker to my OBS setup. I tried about 4 or 5 different plugins from the forums, but they all had issues:
* Most were outdated C++ plugins that crashed the latest OBS.
* The ones that did work were extremely "jittery" (snapping instantly to the mouse), which looked bad on recordings.
* Others required installing heavy external libraries.

I decided to write my own script using **Python** to solve this. Instead of raw tracking, I implemented a smoothing algorithm to give it a professional, "elastic" feel.

##  Features
* **Zero Dependencies:** Uses the native Windows API (`ctypes`) so you don't need to `pip install` anything.
* **Cinematic Smoothing:** Uses a custom **Lerp (Linear Interpolation)** function to make the tracking object "float" behind the cursor rather than snapping instantly.
* **Crash-Free:** Runs as a native OBS Python script, not a compiled DLL.
* **Customizable:** You can attach *any* OBS source (Image, Text, Group) to the mouse.

##  Installation

### Prerequisites
* **OBS Studio** (Latest version recommended)
* **Python 3.10 or 3.11** installed on your system.

### Steps
1.  **Clone this repo** (or download the ZIP):
    ```bash
    git clone [https://github.com/yourusername/obs-elastic-mouse.git](https://github.com/yourusername/obs-elastic-mouse.git)
    ```
2.  **Link Python to OBS**:
    * Open OBS -> `Tools` -> `Scripts`.
    * Go to the `Python Settings` tab.
    * Select your Python install path (e.g., `C:/Users/You/AppData/Local/Programs/Python/Python310`).
3.  **Load the Script**:
    * Go to the `Scripts` tab in OBS.
    * Click `+` and select `elastic_mouse.py` from this folder.
4.  **Setup your Source**:
    * Add an **Image Source** (like a cursor icon or a halo ring) to your OBS scene.
    * **Pro Tip:** Right-click the source -> `Transform` -> `Edit Transform` -> Set **Positional Alignment** to `Center`.
5.  **Configure**:
    * In the Scripts window, select your image source from the dropdown.
    * Adjust the `Smoothness` slider (0.10 is usually the sweet spot!).

##  How it Works (The Math)
The core of the smoothness comes from this simple formula in the `script_tick` function:

```python
# Linear Interpolation (Lerp)
current_x = start_x + (target_x - start_x) * smoothness
