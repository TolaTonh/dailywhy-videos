"""Generic builder for default full-screen photo Shorts. Usage: python3 mk.py <key> [preview]"""
import sys, json
sys.path.insert(0, "/home/claude/shorts")
from v_whiteplanes2 import big, F, ACC, RED, GREEN, WHITE, T
import engine2
from PIL import Image
A, R, G, W = ACC, RED, GREEN, WHITE

def ov(items):
    def fn(P, t, sd, th):
        for delay, y, text, col, size in items:
            if t > delay: big(P, y, text, col, size, t - delay)
    return fn

def sc(s, pid, title=None, tc=None, o=(), off=0, hold=False, focus=(0.5, 0.5), zoom=(1.0, 1.12), dim=0.12):
    d = dict(s=s, fn=ov(o), photo=F(pid, focus=focus, zoom=zoom, dim=dim))
    if off: d["off"] = off
    if title: d["title"] = title
    if tc: d["title_color"] = tc
    if hold: d["hold"] = True
    return d
ZO = (1.12, 1.0)
SPECS = {
"fl350": dict(hook=["WHY 35,000", "FEET?"], mood="curious", scenes=[
    sc(0, "7443738", focus=(0.5, 0.45)),
    sc(0, "4053019", off=2.2, zoom=ZO, o=[(0.2, 760, "HIGHER THAN EVEREST", A, 76)]),
    sc(1, "1831265", "THIN AIR", o=[(0.6, 760, "LESS DRAG", G, 110)], focus=(0.6, 0.5)),
    sc(2, "1493756", "SO THE PLANE...", focus=(0.66, 0.4), zoom=(1.3, 1.5), o=[(0.3, 760, "FLIES FASTER", A, 96)]),
    sc(2, "30210231", "SO THE PLANE...", off=1.8, hold=True, zoom=ZO, focus=(0.5, 0.3), o=[(0.1, 760, "BURNS LESS FUEL", G, 86)]),
    sc(3, "8210858", "ABOVE THE WEATHER", focus=(0.55, 0.5), o=[(0.5, 760, "STORMS STAY BELOW", A, 78)]),
    sc(3, "3939833", "ABOVE THE WEATHER", off=1.8, hold=True, zoom=ZO, o=[(0.1, 760, "SMOOTHER RIDE", G, 96)]),
    sc(4, "6791741", "BUT...", R, o=[(0.2, 700, "THERE'S A LIMIT", R, 100)], dim=0.25),
    sc(5, "4618040", "TOO HIGH?", R, o=[(0.6, 760, "WINGS CAN'T LIFT", R, 84)], dim=0.2),
    sc(5, "459402", "TOO HIGH?", R, off=2.5, hold=True, zoom=ZO, o=[(0.1, 760, "ENGINES CAN'T PUSH", R, 78)], dim=0.3),
    sc(6, "6861359", "THE SWEET SPOT", G, o=[(0.4, 760, "ABOUT 35,000 FT", G, 86)], dim=0.2),
    sc(6, "12720523", "THE SWEET SPOT", G, off=2.3, hold=True, zoom=ZO, o=[(0.1, 760, "LIGHTER = HIGHER", A, 86)]),
    sc(7, "7443738", focus=(0.5, 0.45))]),
"earspop": dict(hook=["WHY DO YOUR", "EARS POP?"], mood="curious", scenes=[
    sc(0, "13794463", focus=(0.5, 0.45)),
    sc(0, "10839046", off=1.5, zoom=ZO, focus=(0.4, 0.5), o=[(0.3, 760, "WHY?", A, 150)]),
    sc(1, "2868978", "INSIDE YOUR EAR", focus=(0.6, 0.5), o=[(0.5, 760, "A POCKET OF AIR", A, 84)]),
    sc(2, "31922532", "THE PRESSURE CHANGES", focus=(0.5, 0.35), o=[(0.5, 760, "CLIMB OR DESCENT", A, 80)], dim=0.2),
    sc(2, "4606720", "THE PRESSURE CHANGES", off=2.8, hold=True, zoom=ZO, o=[(0.2, 760, "TOO FAST FOR YOUR EAR", R, 68)], dim=0.3),
    sc(3, "1828940", "THAT PAIN IS...", R, focus=(0.4, 0.5), o=[(0.6, 760, "PUSH ON THE EARDRUM", R, 72)]),
    sc(4, "635052", "THE FIX", G, focus=(0.55, 0.5), o=[(0.3, 640, "A TINY TUBE", G, 110), (1.2, 790, "EAR TO NOSE", W, 84)]),
    sc(5, "35486426", "HOW TO OPEN IT", G, focus=(0.4, 0.3), o=[(0.3, 760, "SWALLOW OR YAWN", G, 84)], dim=0.2),
    sc(5, "2076721", "HOW TO OPEN IT", G, off=2.6, hold=True, zoom=ZO, o=[(0.3, 720, "POP!", A, 200)], dim=0.3),
    sc(6, "11989285", "WHY BABIES CRY", focus=(0.6, 0.5), o=[(0.5, 760, "SHORTER, FLATTER TUBES", A, 68)], dim=0.3),
    sc(6, "5233240", "WHY BABIES CRY", off=2.8, hold=True, zoom=ZO, o=[(0.2, 760, "HARDER TO EQUALIZE", R, 76)], dim=0.3),
    sc(7, "13794463", focus=(0.5, 0.45))]),
"smoking": dict(hook=["WHY IS SMOKING", "BANNED?"], mood="tense", scenes=[
    sc(0, "764883", focus=(0.55, 0.45), dim=0.0),
    sc(0, "13722624", off=1.9, zoom=ZO, focus=(0.4, 0.3), o=[(0.3, 760, "ONE FIRE", R, 130)], dim=0.0),
    sc(1, "210199", "JULY 1973", focus=(0.52, 0.5), o=[(0.8, 760, "A BOEING 707", A, 90)]),
    sc(1, "12159813", "JULY 1973", off=3.0, hold=True, zoom=ZO, o=[(0.2, 760, "MINUTES FROM LANDING", W, 72)]),
    sc(2, "247040", "IN A REAR TOILET", R, focus=(0.6, 0.6), o=[(0.6, 760, "A FIRE STARTS", R, 96)], dim=0.2),
    sc(2, "8048552", "IN A REAR TOILET", R, off=2.6, hold=True, zoom=ZO, o=[(0.2, 760, "LIKELY A CIGARETTE", A, 76)], dim=0.2),
    sc(3, "10963854", "SMOKE FILLS THE CABIN", R, focus=(0.5, 0.4), dim=0.0),
    sc(4, "4280698", None, None, focus=(0.5, 0.35), dim=0.5, o=[(0.0, 560, "123", R, 280), (0.3, 760, "PEOPLE DIED", W, 84), (2.4, 880, "11 SURVIVED", A, 76)]),
    sc(5, "8920674", "THAT SAME YEAR", G, focus=(0.2, 0.5), zoom=(1.5, 1.65), o=[(0.6, 760, "BANNED IN TOILETS", G, 78)], dim=0.2),
    sc(6, "3119983", "BY 2000", G, o=[(0.6, 760, "ALL US AIRLINE FLIGHTS", G, 68)], dim=0.3),
    sc(6, "31113084", "BY 2000", G, off=3.4, hold=True, zoom=ZO, focus=(0.6, 0.4), o=[(0.3, 760, "ASHTRAYS STILL REQUIRED", A, 66)], dim=0.2),
    sc(6, "5383225", "BY 2000", G, off=5.8, hold=True, focus=(0.55, 0.5), o=[(0.1, 760, "JUST IN CASE", W, 96)], dim=0.2),
    sc(7, "764883", focus=(0.55, 0.45), dim=0.0)]),
"tenerife": dict(hook=["WHY PILOTS", "REPEAT IT ALL"], mood="tense", scenes=[
    sc(0, "3099043", focus=(0.45, 0.45)),
    sc(0, "12257586", off=1.8, zoom=ZO, focus=(0.5, 0.3), o=[(0.3, 760, "WHY?", A, 150)]),
    sc(1, "2253910", "TENERIFE, 1977", focus=(0.8, 0.62), zoom=(1.7, 1.85), o=[(0.8, 760, "TWO JUMBO JETS", A, 88)], dim=0.1),
    sc(1, "3768652", "TENERIFE, 1977", off=2.9, hold=True, zoom=ZO, focus=(0.5, 0.6), o=[(0.2, 760, "ONE FOGGY RUNWAY", W, 80)], dim=0.3),
    sc(2, "1815388", "NOBODY COULD SEE", R, focus=(0.4, 0.45), o=[(1.2, 760, "NOT EVEN THE TOWER", R, 74)]),
    sc(3, "7276731", "THEN...", R, focus=(0.5, 0.5), o=[(0.5, 760, "NO CLEARANCE", R, 100)], dim=0.3),
    sc(3, "29637932", "THEN...", R, off=2.7, hold=True, zoom=ZO, focus=(0.4, 0.6), o=[(0.3, 760, "A RADIO WARNING", A, 84)], dim=0.3),
    sc(3, "19098682", "THEN...", R, off=5.0, hold=True, focus=(0.5, 0.45), o=[(0.1, 760, "BLOCKED", R, 150)]),
    sc(4, "4280698", None, None, focus=(0.5, 0.35), dim=0.5, o=[(0.0, 560, "583", R, 280), (0.3, 760, "PEOPLE DIED", W, 84), (2.8, 880, "DEADLIEST EVER", A, 72)]),
    sc(5, "101522", "AFTER THAT", G, focus=(0.5, 0.5), o=[(0.4, 760, "NEW RADIO RULES", G, 86)], dim=0.3),
    sc(6, "36410538", "THE RULES", G, focus=(0.6, 0.5), o=[(0.3, 700, "\"TAKEOFF\"", A, 120), (1.4, 850, "ONLY WHEN CLEARED", W, 72)], dim=0.3),
    sc(6, "6861359", "THE RULES", G, off=4.2, hold=True, zoom=ZO, o=[(0.2, 760, "READ IT BACK", G, 110)], dim=0.3),
    sc(7, "3099043", focus=(0.45, 0.45))]),
"food": dict(hook=["WHY IS PLANE", "FOOD BLAND?"], mood="curious", scenes=[
    sc(0, "1640769", focus=(0.5, 0.5), zoom=(1.25, 1.4)),
    sc(0, "4637961", off=2.1, zoom=ZO, o=[(0.2, 760, "NOT THE CHEF", A, 110)], dim=0.25),
    sc(1, "7443738", "IN THE CABIN", focus=(0.5, 0.45), o=[(0.6, 640, "LIKE 8,000 FT", A, 110), (1.6, 800, "UP A MOUNTAIN", W, 84)], dim=0.25),
    sc(2, "3119983", "COOL, DRY AIR", o=[(0.6, 760, "DULLS YOUR NOSE", R, 84)], dim=0.3),
    sc(2, "4061487", "COOL, DRY AIR", off=2.6, hold=True, zoom=ZO, o=[(0.2, 760, "AND TASTE BUDS", R, 90)], dim=0.2),
    sc(3, "1640769", "THE RESULT", R, focus=(0.3, 0.5), zoom=(1.5, 1.7), dim=0.45, o=[(0.3, 560, "-30%", R, 260), (1.2, 770, "SALTY + SWEET", W, 84)]),
    sc(4, "30210231", "AND...", focus=(0.5, 0.3), o=[(0.2, 760, "EVEN THE NOISE", A, 96)], dim=0.2),
    sc(5, "459402", "ENGINE NOISE", focus=(0.48, 0.5), o=[(0.8, 760, "SWEET: WEAKER", R, 88)], dim=0.3),
    sc(5, "7801106", "ENGINE NOISE", off=3.6, hold=True, zoom=ZO, o=[(0.2, 760, "UMAMI: STRONGER", G, 84)], dim=0.3),
    sc(6, "5946664", "THE WINNER", G, focus=(0.5, 0.45), o=[(0.5, 780, "TOMATO JUICE", A, 100)], dim=0.2),
    sc(6, "5946655", "THE WINNER", G, off=3.2, hold=True, zoom=ZO, focus=(0.5, 0.55), o=[(0.3, 780, "AS POPULAR AS BEER", W, 74)], dim=0.3),
    sc(7, "1640769", focus=(0.5, 0.5), zoom=(1.25, 1.4))]),
"row13": dict(hook=["WHY NO", "ROW 13?"], mood="curious", scenes=[
    sc(0, "15873638", focus=(0.55, 0.5), zoom=(1.0, 1.1), dim=0.2),
    sc(0, "4061487", off=2.1, zoom=ZO, o=[(0.2, 640, "12...", W, 130), (0.8, 800, "14?", A, 170)], dim=0.3),
    sc(1, "4637961", "NOT A MISTAKE", o=[(0.9, 760, "SKIPPED ON PURPOSE", A, 76)], dim=0.3),
    sc(2, "15873638", "THE NUMBER 13", R, focus=(0.55, 0.5), zoom=(1.3, 1.45), o=[(0.9, 800, "\"UNLUCKY\"", R, 120)], dim=0.35),
    sc(3, "11989285", "ONE AIRLINE SAID", focus=(0.6, 0.5), o=[(1.2, 760, "ROWS 13 AND 17", A, 96)], dim=0.35),
    sc(3, "3119983", "ONE AIRLINE SAID", off=3.9, hold=True, zoom=ZO, o=[(0.3, 760, "\"UNLUCKY NUMBERS\"", R, 80)], dim=0.35),
    sc(4, "10963854", "WAIT...", focus=(0.5, 0.4), o=[(0.0, 700, "17?", A, 260)], dim=0.2),
    sc(5, "4280698", "FROM ITALY", focus=(0.5, 0.35), dim=0.5, o=[(0.4, 560, "XVII", A, 220), (2.2, 720, "VIXI", R, 220), (3.8, 880, "\"MY LIFE IS OVER\"", W, 72)]),
    sc(6, "4606720", "THE TRUTH", G, o=[(0.3, 760, "SAME SEATS", G, 110)], dim=0.3),
    sc(6, "5233240", "THE TRUTH", G, off=1.9, hold=True, zoom=ZO, o=[(0.1, 760, "ONLY THE NUMBER", W, 86)], dim=0.3),
    sc(7, "15873638", focus=(0.55, 0.5), zoom=(1.0, 1.1), dim=0.2)]),
"contrails": dict(hook=["WHY WHITE", "TRAILS?"], mood="curious", scenes=[
    sc(0, "11593192", focus=(0.6, 0.45), dim=0.0),
    sc(0, "12850", off=2.0, zoom=ZO, o=[(0.2, 760, "WHY?", A, 150)]),
    sc(1, "164646", "IT'S NOT SMOKE", focus=(0.36, 0.5), zoom=(1.0, 1.08), o=[(0.9, 760, "IT'S ICE", A, 150)], dim=0.0),
    sc(2, "30210231", "FROM THE ENGINE", focus=(0.5, 0.3), o=[(0.5, 760, "WATER VAPOR", A, 100)], dim=0.2),
    sc(3, "22819806", "UP HIGH", focus=(0.5, 0.5), o=[(1.0, 640, "-35 DEGREES", R, 120), (2.2, 800, "OR COLDER", W, 84)], dim=0.1),
    sc(3, "10112536", "UP HIGH", off=4.0, hold=True, zoom=ZO, o=[(0.3, 760, "ICE CRYSTALS", A, 104)], dim=0.1),
    sc(4, "12117651", "AND...", G, o=[(0.3, 760, "A WEATHER CLUE", G, 96)]),
    sc(5, "164646", "DRY AIR", focus=(0.36, 0.5), zoom=(1.1, 1.0), o=[(0.5, 760, "GONE IN MINUTES", A, 84)], dim=0.0),
    sc(6, "12850", "HUMID AIR", focus=(0.5, 0.4), o=[(0.5, 760, "LASTS FOR HOURS", A, 84)]),
    sc(6, "1831265", "HUMID AIR", off=2.4, hold=True, zoom=ZO, focus=(0.6, 0.5), o=[(0.2, 760, "BECOMES THIN CLOUD", W, 74)]),
    sc(7, "11593192", focus=(0.6, 0.45), dim=0.0)]),
"boardleft": dict(hook=["WHY BOARD", "ON THE LEFT?"], mood="bright", scenes=[
    sc(0, "3069147", focus=(0.6, 0.5)),
    sc(0, "27046715", off=1.9, zoom=ZO, o=[(0.2, 760, "ALWAYS LEFT", A, 110)]),
    sc(1, "952872", "IT STARTED AT SEA", focus=(0.45, 0.5), o=[(0.9, 760, "FROM SHIPS", A, 120)], dim=0.2),
    sc(1, "18518264", "IT STARTED AT SEA", off=2.3, hold=True, zoom=ZO, focus=(0.5, 0.5), o=[(0.3, 760, "PORT SIDE = LEFT", W, 84)], dim=0.25),
    sc(2, "5640195", "PLANES KEPT IT", focus=(0.3, 0.55), zoom=(1.2, 1.3)),
    sc(3, "36410538", "REASON 2", focus=(0.6, 0.5), o=[(0.5, 760, "CAPTAIN SITS LEFT", A, 82)], dim=0.3),
    sc(3, "27046715", "REASON 2", off=2.8, hold=True, zoom=(1.3, 1.15), focus=(0.6, 0.45), o=[(0.3, 760, "LINES UP THE DOOR", W, 80)], dim=0.2),
    sc(4, "11795378", "REASON 3", R, focus=(0.5, 0.6), o=[(0.3, 760, "THE BUSY SIDE", R, 100)], dim=0.2),
    sc(5, "12639108", "ON THE RIGHT", R, focus=(0.4, 0.6), o=[(0.6, 760, "FUEL + BAGGAGE", A, 96)], dim=0.3),
    sc(6, "5233240", "ON THE LEFT", G, o=[(0.3, 760, "PASSENGERS", G, 120)], dim=0.3),
    sc(6, "33366061", "ON THE LEFT", G, off=2.4, hold=True, zoom=ZO, focus=(0.45, 0.6), o=[(0.2, 760, "NOBODY IN THE WAY", W, 80)], dim=0.2),
    sc(7, "3069147", focus=(0.6, 0.5))]),
"wingsbend": dict(hook=["WINGS BEND.", "WORRY?"], mood="curious", scenes=[
    sc(0, "731217", focus=(0.6, 0.45)),
    sc(0, "14325264", off=2.4, zoom=ZO, focus=(0.55, 0.5), o=[(0.3, 760, "SHOULD YOU WORRY?", A, 78)]),
    sc(1, "5071151", "NO", G, focus=(0.6, 0.5), o=[(0.3, 760, "BUILT TO BEND", G, 110)]),
    sc(2, "10512949", "WHY FLEX?", focus=(0.55, 0.5), o=[(0.6, 760, "TAKES THE LOAD", A, 96)], dim=0.1),
    sc(2, "6791741", "WHY FLEX?", off=2.8, hold=True, zoom=ZO, o=[(0.2, 760, "SPRINGS BACK", G, 110)], dim=0.2),
    sc(3, "20640861", "THE RULE", focus=(0.5, 0.6), dim=0.45, o=[(0.6, 560, "1.5x", A, 280), (1.8, 770, "THE WORST LOAD", W, 84)]),
    sc(4, "5627575", "SO ENGINEERS...", focus=(0.3, 0.55), o=[(0.6, 760, "PROVE IT", A, 130)], dim=0.3),
    sc(5, "32155436", "787 WING TEST, 2010", focus=(0.42, 0.5), dim=0.4, o=[(1.6, 560, "25 FT", R, 280), (2.6, 770, "BENT UPWARD", W, 90)]),
    sc(6, "7443738", "THE RESULT", G, focus=(0.5, 0.45), o=[(0.0, 760, "IT PASSED", G, 130)], dim=0.2),
    sc(6, "1493756", "THE RESULT", G, off=1.4, hold=True, focus=(0.66, 0.4), zoom=(1.5, 1.3), o=[(0.2, 760, "STIFFER = HEAVIER", A, 80)], dim=0.2),
    sc(7, "731217", focus=(0.6, 0.45))]),
"gimli": dict(hook=["OUT OF FUEL", "AT 41,000 FT"], mood="tense", scenes=[
    sc(0, "6791741", focus=(0.5, 0.5)),
    sc(0, "4618040", off=3.2, zoom=ZO, o=[(0.3, 640, "1983", A, 200), (1.2, 820, "HOW?", W, 120)], dim=0.2),
    sc(1, "3402846", "THE GAUGES", R, o=[(0.5, 760, "NOT WORKING", R, 110)], dim=0.3),
    sc(1, "15860583", "THE GAUGES", R, off=2.1, hold=True, zoom=ZO, o=[(0.2, 760, "MEASURED BY HAND", A, 80)], dim=0.3),
    sc(2, "5262805", "THE MISTAKE", R, dim=0.45, o=[(0.2, 600, "POUNDS", A, 150), (0.9, 760, "vs KILOGRAMS", R, 110)]),
    sc(3, "1493756", "SO IT TOOK OFF WITH...", focus=(0.66, 0.4), zoom=(1.3, 1.5), dim=0.35, o=[(0.6, 620, "LESS THAN HALF", R, 100), (1.5, 790, "THE FUEL", W, 110)]),
    sc(4, "4280698", None, None, focus=(0.5, 0.35), dim=0.5, o=[(0.0, 600, "BOTH ENGINES", W, 110), (0.8, 790, "SILENT", R, 190)]),
    sc(5, "5869839", "THE CAPTAIN", G, focus=(0.75, 0.55), zoom=(1.3, 1.45), o=[(0.5, 800, "A GLIDER PILOT", G, 90)]),
    sc(5, "28487499", "THE CAPTAIN", G, off=2.6, hold=True, zoom=ZO, focus=(0.55, 0.65), dim=0.1, o=[(0.3, 620, "17", A, 280), (0.9, 820, "MINUTES GLIDING", W, 80)]),
    sc(6, "10106451", "THE RUNWAY?", R, focus=(0.5, 0.6), o=[(0.6, 760, "NOW A RACE TRACK", R, 80)], dim=0.2),
    sc(6, "368690", "THE RUNWAY?", R, off=3.0, hold=True, zoom=ZO, dim=0.4, o=[(0.3, 580, "69", G, 300), (1.2, 790, "ALL SURVIVED", G, 100)]),
    sc(7, "6791741", focus=(0.5, 0.5))]),
"aloharoof": dict(hook=["THE ROOF", "TORE OFF"], mood="tense", scenes=[
    sc(0, "595675", focus=(0.5, 0.5)),
    sc(0, "15663583", off=2.9, zoom=ZO, o=[(0.2, 640, "1988", A, 200), (1.0, 820, "HOW?", W, 120)], dim=0.25),
    sc(1, "16611426", "HAWAII", o=[(0.5, 640, "19 YEARS OLD", A, 100), (2.0, 800, "SHORT ISLAND HOPS", W, 76)], dim=0.3),
    sc(2, "5231889", "A HARD LIFE", R, dim=0.4, o=[(0.3, 580, "~90,000", A, 220), (1.2, 790, "FLIGHTS", W, 120)]),
    sc(3, "595675", "EVERY FLIGHT", R, focus=(0.3, 0.5), zoom=(1.5, 1.7), o=[(0.5, 760, "STRAINS THE METAL", R, 80)], dim=0.3),
    sc(3, "15663576", "EVERY FLIGHT", R, off=2.3, hold=True, zoom=ZO, o=[(0.2, 760, "SALT = CORROSION", A, 84)], dim=0.3),
    sc(4, "4280698", None, None, focus=(0.5, 0.35), dim=0.5, o=[(0.0, 560, "24,000 FT", W, 130), (1.4, 760, "18 FEET", R, 220), (2.0, 920, "OF ROOF GONE", W, 80)]),
    sc(5, "3119983", "INSIDE", R, o=[(2.0, 760, "SEAT BELTS HELD", G, 86)], dim=0.35),
    sc(5, "3768652", "INSIDE", R, off=4.0, hold=True, zoom=ZO, focus=(0.5, 0.6), dim=0.3, o=[(0.3, 600, "13 MINUTES", G, 130), (1.0, 780, "TO A SAFE LANDING", W, 76)]),
    sc(6, "20640861", "AFTER THAT", G, focus=(0.5, 0.6), o=[(0.6, 760, "SPECIAL INSPECTIONS", G, 74)], dim=0.3),
    sc(6, "30210231", "AFTER THAT", G, off=2.8, hold=True, zoom=ZO, focus=(0.5, 0.3), o=[(0.2, 760, "FIND TINY CRACKS", A, 84)], dim=0.3),
    sc(7, "595675", focus=(0.5, 0.5))]),
}
if __name__ == "__main__":
    key = sys.argv[1]; sp = SPECS[key]
    args = dict(key=key, scenes=sp["scenes"], theme=T, bg_img=Image.new("RGB", (1080, 1920), T["bg1"]), hook_lines=sp["hook"], mood=sp["mood"])
    if len(sys.argv) > 2:
        tm = json.load(open(f"/home/claude/shorts/{key}_timing.json"))["sentences"]
        ts = [0.3] + [tm[s["s"]]["start"] + s.get("off", 0) + 1.7 for s in sp["scenes"][1:-1]] + [tm[-1]["end"] + 0.5]
        engine2.render(preview=ts, **args)
    else:
        engine2.render(**args)
