"""Animate the Lemon story keyframes with Veo 3.1 Fast on MuAPI (skips clips that already exist)."""
import os, sys
sys.path.insert(0, "scripts")
import muapi_gen as m

K, C = "out/lemon_story/keyframes", "out/lemon_story/clips"
MOTION = {
    "k2": "Lenny waves hello hopefully; Sophie the strawberry, the grape and the apple pull disgusted sour puckered faces and lean away from him; Lenny's smile fades. Comedic timing, gentle camera push-in.",
    "k3": "Lenny sits alone on the windowsill hugging his knees, sighs deeply and looks down sadly; rain streams down the window glass; slow gentle camera push-in.",
    "k4": "Heat haze shimmers, the blazing sun pulses, the thermometer bursts its top; the grape, apple, orange and banana droop, sweat drips and they fan themselves desperately. Comedic, camera slowly pans.",
    "k5": "The crowd of sweaty desperate fruit rushes towards Lenny, Sophie at the front pleading with clasped hands; Lenny blinks in surprise. Energetic, camera pushes in on Lenny.",
    "k6": "Lenny in sunglasses smugly sips his lemonade and gives a cool little nod while the long queue of hot fruit waits eagerly; Lenny pushes his sunglasses up with one finger. Confident, comedic, slow push-in.",
    "k7": "Everyone laughs and clinks their glasses of lemonade together in celebration at golden sunset; Lenny laughs happily in the middle. Warm, joyful, camera slowly pulls back.",
}
os.makedirs(C, exist_ok=True)
total = 0.0
for k, motion in MOTION.items():
    out = f"{C}/c{k[1:]}.mp4"
    if os.path.exists(out):
        print("skip", out); continue
    url = open(f"{K}/{k}.url").read().strip()
    _, cost = m.video(url, motion + " Pixar-style 3D animation, smooth natural motion.", out, extra={"generate_audio": False})
    total += cost or 0
    print("made", out, flush=True)
print(f"ALL_CLIPS_DONE total ${total:.2f}")
