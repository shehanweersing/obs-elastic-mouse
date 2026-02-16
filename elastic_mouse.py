import obspython as obs
import ctypes
import math

# --- 1. GLOBAL VARIABLES ---
source_name = ""
smoothness = 0.1  # Lower = slower/smoother, Higher = faster/snappier
follow_active = False

# Current position (for smoothing)
current_x = 0.0
current_y = 0.0

# Windows API structure for mouse coordinates
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

# --- 2. CORE FUNCTIONS ---

def get_global_mouse_pos():
    """Gets the raw mouse position from Windows API."""
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

def lerp(start, end, alpha):
    """Linear Interpolation for smooth movement."""
    return start + (end - start) * alpha

# --- 3. OBS SCRIPT CALLBACKS ---

def script_description():
    return "Elastic Mouse Tracker\n\nA smooth, cinematic mouse tracking script for OBS.\nAuthor: You\nGitHub: YourGithubLink"

def script_properties():
    """Define the UI settings in OBS."""
    props = obs.obs_properties_create()
    
    # Dropdown to select the source (e.g., a cursor image or highlight circle)
    p = obs.obs_properties_add_list(props, "source", "Source to Move", 
                                    obs.OBS_COMBO_TYPE_EDITABLE, 
                                    obs.OBS_COMBO_FORMAT_STRING)
    
    # Populate the dropdown with current sources
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_id(source)
            name = obs.obs_source_get_name(source)
            obs.obs_property_list_add_string(p, name, name)
        obs.source_list_release(sources)

    # Slider for smoothness
    obs.obs_properties_add_float_slider(props, "smoothness", "Smoothness (Low=Cinematic)", 0.01, 1.0, 0.01)
    
    return props

def script_update(settings):
    """Called when settings are changed by the user."""
    global source_name, smoothness, follow_active
    source_name = obs.obs_data_get_string(settings, "source")
    smoothness = obs.obs_data_get_double(settings, "smoothness")
    follow_active = True

def script_tick(seconds):
    """Called every frame. This is the movement engine."""
    global current_x, current_y
    
    if not follow_active or not source_name:
        return

    # 1. Get the Scene Item
    current_scene = obs.obs_frontend_get_current_scene()
    scene = obs.obs_scene_from_source(current_scene)
    scene_item = obs.obs_scene_find_source_recursive(scene, source_name)
    
    if scene_item:
        # 2. Get Target Mouse Position
        target_x, target_y = get_global_mouse_pos()
        
        # 3. Apply "Elastic" Smoothing (Lerp)
        # If we just set x=target_x, it looks jittery. Lerp makes it float.
        current_x = lerp(current_x, target_x, smoothness)
        current_y = lerp(current_y, target_y, smoothness)

        # 4. Update Position in OBS
        pos = obs.vec2()
        pos.x = current_x
        pos.y = current_y
        
        # We need to offset by half the source size to center it (optional refinement)
        # For now, we set the top-left corner to the mouse
        obs.obs_sceneitem_set_pos(scene_item, pos)

    obs.obs_source_release(current_scene)