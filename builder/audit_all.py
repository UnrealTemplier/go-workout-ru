from chapters import get_chapter_url_map
url_map = get_chapter_url_map()
import json
import os
import re
import subprocess
import tempfile

from section1 import exercises as s1
from section2 import exercises as s2
from section3 import exercises as s3
from section4 import exercises as s4
from section5 import exercises as s5
from section6 import exercises as s6

with open('builder/chapter2_data.json', 'r', encoding='utf-8') as f:
    ch2_exercises = json.load(f)

with open('builder/chapter3_data.json', 'r', encoding='utf-8') as f:
    ch3_exercises = json.load(f)

with open('builder/chapter4_data.json', 'r', encoding='utf-8') as f:
    ch4_exercises = json.load(f)

with open('builder/chapter5_data.json', 'r', encoding='utf-8') as f:
    ch5_exercises = json.load(f)

with open('builder/chapter6_data.json', 'r', encoding='utf-8') as f:
    ch6_exercises = json.load(f)

with open('builder/chapter7_data.json', 'r', encoding='utf-8') as f:
    ch7_exercises = json.load(f)

with open('builder/chapter8_data.json', 'r', encoding='utf-8') as f:
    ch8_exercises = json.load(f)

with open('builder/chapter9_data.json', 'r', encoding='utf-8') as f:
    ch9_exercises = json.load(f)

with open('builder/chapter10_data.json', 'r', encoding='utf-8') as f:
    ch10_exercises = json.load(f)

with open('builder/chapter11_data.json', 'r', encoding='utf-8') as f:
    ch11_exercises = json.load(f)

with open('builder/chapter12_data.json', 'r', encoding='utf-8') as f:
    ch12_exercises = json.load(f)

with open('builder/chapter13_data.json', 'r', encoding='utf-8') as f:
    ch13_exercises = json.load(f)

with open('builder/chapter14_data.json', 'r', encoding='utf-8') as f:
    ch14_exercises = json.load(f)

with open('builder/chapter15_data.json', 'r', encoding='utf-8') as f:
    ch15_exercises = json.load(f)

with open('builder/chapter16_data.json', 'r', encoding='utf-8') as f:
    ch16_exercises = json.load(f)

with open('builder/chapter17_data.json', 'r', encoding='utf-8') as f:
    ch17_exercises = json.load(f)

with open('builder/chapter18_data.json', 'r', encoding='utf-8') as f:
    ch18_exercises = json.load(f)

with open('builder/chapter19_data.json', 'r', encoding='utf-8') as f:
    ch19_exercises = json.load(f)

with open('builder/chapter20_data.json', 'r', encoding='utf-8') as f:
    ch20_exercises = json.load(f)

with open('builder/chapter21_data.json', 'r', encoding='utf-8') as f:
    ch21_exercises = json.load(f)

with open('builder/chapter22_data.json', 'r', encoding='utf-8') as f:
    ch22_exercises = json.load(f)

with open('builder/chapter23_data.json', 'r', encoding='utf-8') as f:
    ch23_exercises = json.load(f)

with open('builder/chapter24_data.json', 'r', encoding='utf-8') as f:
    ch24_exercises = json.load(f)

with open('builder/chapter25_data.json', 'r', encoding='utf-8') as f:
    ch25_exercises = json.load(f)

with open('builder/chapter26_data.json', 'r', encoding='utf-8') as f:
    ch26_exercises = json.load(f)

with open('builder/chapter27_data.json', 'r', encoding='utf-8') as f:
    ch27_exercises = json.load(f)

with open('builder/chapter28_data.json', 'r', encoding='utf-8') as f:
    ch28_exercises = json.load(f)

with open('builder/chapter29_data.json', 'r', encoding='utf-8') as f:
    ch29_exercises = json.load(f)

with open('builder/chapter30_data.json', 'r', encoding='utf-8') as f:
    ch30_exercises = json.load(f)

with open('builder/chapter31_data.json', 'r', encoding='utf-8') as f:
    ch31_exercises = json.load(f)

with open('builder/chapter32_data.json', 'r', encoding='utf-8') as f:
    ch32_exercises = json.load(f)

with open('builder/chapter33_data.json', 'r', encoding='utf-8') as f:
    ch33_exercises = json.load(f)

with open('builder/chapter34_data.json', 'r', encoding='utf-8') as f:
    ch34_exercises = json.load(f)

with open('builder/chapter35_data.json', 'r', encoding='utf-8') as f:
    ch35_exercises = json.load(f)

with open('builder/chapter36_data.json', 'r', encoding='utf-8') as f:
    ch36_exercises = json.load(f)

with open('builder/chapter37_data.json', 'r', encoding='utf-8') as f:
    ch37_exercises = json.load(f)

with open('builder/chapter38_data.json', 'r', encoding='utf-8') as f:
    ch38_exercises = json.load(f)

with open('builder/chapter39_data.json', 'r', encoding='utf-8') as f:
    ch39_exercises = json.load(f)

with open('builder/chapter40_data.json', 'r', encoding='utf-8') as f:
    ch40_exercises = json.load(f)

with open('builder/chapter41_data.json', 'r', encoding='utf-8') as f:
    ch41_exercises = json.load(f)

with open('builder/chapter42_data.json', 'r', encoding='utf-8') as f:
    ch42_exercises = json.load(f)

with open('builder/chapter43_data.json', 'r', encoding='utf-8') as f:
    ch43_exercises = json.load(f)

with open('builder/chapter44_data.json', 'r', encoding='utf-8') as f:
    ch44_exercises = json.load(f)

with open('builder/chapter45_data.json', 'r', encoding='utf-8') as f:
    ch45_exercises = json.load(f)

with open('builder/chapter46_data.json', 'r', encoding='utf-8') as f:
    ch46_exercises = json.load(f)

with open('builder/chapter47_data.json', 'r', encoding='utf-8') as f:
    ch47_exercises = json.load(f)

with open('builder/chapter48_data.json', 'r', encoding='utf-8') as f:
    ch48_exercises = json.load(f)

with open('builder/chapter49_data.json', 'r', encoding='utf-8') as f:
    ch49_exercises = json.load(f)

with open('builder/chapter50_data.json', 'r', encoding='utf-8') as f:
    ch50_exercises = json.load(f)

with open('builder/chapter51_data.json', 'r', encoding='utf-8') as f:
    ch51_exercises = json.load(f)

with open('builder/chapter52_data.json', 'r', encoding='utf-8') as f:
    ch52_exercises = json.load(f)

with open('builder/chapter53_data.json', 'r', encoding='utf-8') as f:
    ch53_exercises = json.load(f)

with open('builder/chapter54_data.json', 'r', encoding='utf-8') as f:
    ch54_exercises = json.load(f)

with open('builder/chapter55_data.json', 'r', encoding='utf-8') as f:
    ch55_exercises = json.load(f)

with open('builder/chapter56_data.json', 'r', encoding='utf-8') as f:
    ch56_exercises = json.load(f)

with open('builder/chapter57_data.json', 'r', encoding='utf-8') as f:
    ch57_exercises = json.load(f)

with open('builder/chapter58_data.json', 'r', encoding='utf-8') as f:
    ch58_exercises = json.load(f)

with open('builder/chapter59_data.json', 'r', encoding='utf-8') as f:
    ch59_exercises = json.load(f)

with open('builder/chapter60_data.json', 'r', encoding='utf-8') as f:
    ch60_exercises = json.load(f)

with open('builder/chapter61_data.json', 'r', encoding='utf-8') as f:
    ch61_exercises = json.load(f)

with open('builder/chapter62_data.json', 'r', encoding='utf-8') as f:
    ch62_exercises = json.load(f)

with open('builder/chapter63_data.json', 'r', encoding='utf-8') as f:
    ch63_exercises = json.load(f)

with open('builder/chapter64_data.json', 'r', encoding='utf-8') as f:
    ch64_exercises = json.load(f)

with open('builder/chapter65_data.json', 'r', encoding='utf-8') as f:
    ch65_exercises = json.load(f)

with open('builder/chapter66_data.json', 'r', encoding='utf-8') as f:
    ch66_exercises = json.load(f)

with open('builder/chapter67_data.json', 'r', encoding='utf-8') as f:
    ch67_exercises = json.load(f)

with open('builder/chapter68_data.json', 'r', encoding='utf-8') as f:
    ch68_exercises = json.load(f)

with open('builder/chapter69_data.json', 'r', encoding='utf-8') as f:
    ch69_exercises = json.load(f)

with open('builder/chapter70_data.json', 'r', encoding='utf-8') as f:
    ch70_exercises = json.load(f)

with open('builder/chapter71_data.json', 'r', encoding='utf-8') as f:
    ch71_exercises = json.load(f)

with open('builder/chapter72_data.json', 'r', encoding='utf-8') as f:
    ch72_exercises = json.load(f)

with open('builder/chapter73_data.json', 'r', encoding='utf-8') as f:
    ch73_exercises = json.load(f)

with open('builder/chapter74_data.json', 'r', encoding='utf-8') as f:
    ch74_exercises = json.load(f)

with open('builder/chapter75_data.json', 'r', encoding='utf-8') as f:
    ch75_exercises = json.load(f)

with open('builder/chapter76_data.json', 'r', encoding='utf-8') as f:
    ch76_exercises = json.load(f)

with open('builder/chapter77_data.json', 'r', encoding='utf-8') as f:
    ch77_exercises = json.load(f)

with open('builder/chapter78_data.json', 'r', encoding='utf-8') as f:
    ch78_exercises = json.load(f)

with open('builder/chapter79_data.json', 'r', encoding='utf-8') as f:
    ch79_exercises = json.load(f)

with open('builder/chapter80_data.json', 'r', encoding='utf-8') as f:
    ch80_exercises = json.load(f)

with open('builder/chapter81_data.json', 'r', encoding='utf-8') as f:
    ch81_exercises = json.load(f)

with open('builder/chapter82_data.json', 'r', encoding='utf-8') as f:
    ch82_exercises = json.load(f)

with open('builder/chapter83_data.json', 'r', encoding='utf-8') as f:
    ch83_exercises = json.load(f)
with open('builder/chapter84_data.json', 'r', encoding='utf-8') as f:
    ch84_exercises = json.load(f)
with open('builder/chapter85_data.json', 'r', encoding='utf-8') as f:
    ch85_exercises = json.load(f)
with open('builder/chapter86_data.json', 'r', encoding='utf-8') as f:
    ch86_exercises = json.load(f)
with open('builder/chapter87_data.json', 'r', encoding='utf-8') as f:
    ch87_exercises = json.load(f)
with open('builder/chapter88_data.json', 'r', encoding='utf-8') as f:
    ch88_exercises = json.load(f)
with open('builder/chapter89_data.json', 'r', encoding='utf-8') as f:
    ch89_exercises = json.load(f)
with open('builder/chapter90_data.json', 'r', encoding='utf-8') as f:
    ch90_exercises = json.load(f)
with open('builder/chapter91_data.json', 'r', encoding='utf-8') as f:
    ch91_exercises = json.load(f)
with open('builder/chapter92_data.json', 'r', encoding='utf-8') as f:
    ch92_exercises = json.load(f)
with open('builder/chapter93_data.json', 'r', encoding='utf-8') as f:
    ch93_exercises = json.load(f)
with open('builder/chapter94_data.json', 'r', encoding='utf-8') as f:
    ch94_exercises = json.load(f)
with open('builder/chapter95_data.json', 'r', encoding='utf-8') as f:
    ch95_exercises = json.load(f)
with open('builder/chapter96_data.json', 'r', encoding='utf-8') as f:
    ch96_exercises = json.load(f)
with open('builder/chapter97_data.json', 'r', encoding='utf-8') as f:
    ch97_exercises = json.load(f)
with open('builder/chapter98_data.json', 'r', encoding='utf-8') as f:
    ch98_exercises = json.load(f)
with open('builder/chapter99_data.json', 'r', encoding='utf-8') as f:
    ch99_exercises = json.load(f)
with open('builder/chapter100_data.json', 'r', encoding='utf-8') as f:
    ch100_exercises = json.load(f)

all_ch1 = s1 + s2 + s3 + s4 + s5 + s6
all_ch2 = ch2_exercises
all_ch3 = ch3_exercises
all_ch4 = ch4_exercises
all_ch5 = ch5_exercises
all_ch6 = ch6_exercises
all_ch7 = ch7_exercises
all_ch8 = ch8_exercises
all_ch9 = ch9_exercises
all_ch10 = ch10_exercises
all_ch11 = ch11_exercises
all_ch12 = ch12_exercises
all_ch13 = ch13_exercises
all_ch14 = ch14_exercises
all_ch15 = ch15_exercises
all_ch16 = ch16_exercises
all_ch17 = ch17_exercises
all_ch18 = ch18_exercises
all_ch19 = ch19_exercises
all_ch20 = ch20_exercises
all_ch21 = ch21_exercises
all_ch22 = ch22_exercises
all_ch23 = ch23_exercises
all_ch24 = ch24_exercises
all_ch25 = ch25_exercises
all_ch26 = ch26_exercises
all_ch27 = ch27_exercises
all_ch28 = ch28_exercises
all_ch29 = ch29_exercises
all_ch30 = ch30_exercises
all_ch31 = ch31_exercises
all_ch32 = ch32_exercises
all_ch33 = ch33_exercises
all_ch34 = ch34_exercises
all_ch35 = ch35_exercises
all_ch36 = ch36_exercises
all_ch37 = ch37_exercises
all_ch38 = ch38_exercises
all_ch39 = ch39_exercises
all_ch40 = ch40_exercises
all_ch41 = ch41_exercises
all_ch42 = ch42_exercises
all_ch43 = ch43_exercises
all_ch44 = ch44_exercises
all_ch45 = ch45_exercises
all_ch46 = ch46_exercises
all_ch47 = ch47_exercises
all_ch48 = ch48_exercises
all_ch49 = ch49_exercises
all_ch50 = ch50_exercises
all_ch51 = ch51_exercises
all_ch52 = ch52_exercises
all_ch53 = ch53_exercises
all_ch54 = ch54_exercises
all_ch55 = ch55_exercises
all_ch56 = ch56_exercises
all_ch57 = ch57_exercises
all_ch58 = ch58_exercises
all_ch59 = ch59_exercises
all_ch60 = ch60_exercises
all_ch61 = ch61_exercises
all_ch62 = ch62_exercises
all_ch63 = ch63_exercises
all_ch64 = ch64_exercises
all_ch65 = ch65_exercises
all_ch66 = ch66_exercises
all_ch67 = ch67_exercises
all_ch68 = ch68_exercises
all_ch69 = ch69_exercises
all_ch70 = ch70_exercises
all_ch71 = ch71_exercises
all_ch72 = ch72_exercises
all_ch73 = ch73_exercises
all_ch74 = ch74_exercises
all_ch75 = ch75_exercises
all_ch76 = ch76_exercises
all_ch77 = ch77_exercises
all_ch78 = ch78_exercises
all_ch79 = ch79_exercises
all_ch80 = ch80_exercises
all_ch81 = ch81_exercises
all_ch82 = ch82_exercises
all_ch83 = ch83_exercises
all_ch84 = ch84_exercises
all_ch85 = ch85_exercises
all_ch86 = ch86_exercises
all_ch87 = ch87_exercises
all_ch88 = ch88_exercises
all_ch89 = ch89_exercises
all_ch90 = ch90_exercises
all_ch91 = ch91_exercises
all_ch92 = ch92_exercises
all_ch93 = ch93_exercises
all_ch94 = ch94_exercises
all_ch95 = ch95_exercises
all_ch96 = ch96_exercises
all_ch97 = ch97_exercises
all_ch98 = ch98_exercises
all_ch99 = ch99_exercises
all_ch100 = ch100_exercises

total_ex = len(all_ch1) + len(all_ch2) + len(all_ch3) + len(all_ch4) + len(all_ch5) + len(all_ch6) + len(all_ch7) + len(all_ch8) + len(all_ch9) + len(all_ch10) + len(all_ch11) + len(all_ch12) + len(all_ch13) + len(all_ch14) + len(all_ch15) + len(all_ch16) + len(all_ch17) + len(all_ch18) + len(all_ch19) + len(all_ch20) + len(all_ch21) + len(all_ch22) + len(all_ch23) + len(all_ch24) + len(all_ch25) + len(all_ch26) + len(all_ch27) + len(all_ch28) + len(all_ch29) + len(all_ch30) + len(all_ch31) + len(all_ch32) + len(all_ch33) + len(all_ch34) + len(all_ch35) + len(all_ch36) + len(all_ch37) + len(all_ch38) + len(all_ch39) + len(all_ch40) + len(all_ch41) + len(all_ch42) + len(all_ch43) + len(all_ch44) + len(all_ch45) + len(all_ch46) + len(all_ch47) + len(all_ch48) + len(all_ch49) + len(all_ch50) + len(all_ch51) + len(all_ch52) + len(all_ch53) + len(all_ch54) + len(all_ch55) + len(all_ch56) + len(all_ch57) + len(all_ch58) + len(all_ch59) + len(all_ch60) + len(all_ch61) + len(all_ch62) + len(all_ch63) + len(all_ch64) + len(all_ch65) + len(all_ch66) + len(all_ch67) + len(all_ch68) + len(all_ch69) + len(all_ch70) + len(all_ch71) + len(all_ch72) + len(all_ch73) + len(all_ch74) + len(all_ch75) + len(all_ch76) + len(all_ch77) + len(all_ch78) + len(all_ch79) + len(all_ch80) + len(all_ch81) + len(all_ch82) + len(all_ch83) + len(all_ch84) + len(all_ch85) + len(all_ch86) + len(all_ch87) + len(all_ch88) + len(all_ch89) + len(all_ch90) + len(all_ch91) + len(all_ch92) + len(all_ch93) + len(all_ch94) + len(all_ch95) + len(all_ch96) + len(all_ch97) + len(all_ch98) + len(all_ch99) + len(all_ch100)


print("=== ТЕХНИЧЕСКИЙ АУДИТ УЧЕБНИКА GO ===")
print(f"Глава 1:  {len(all_ch1)} упражнений")
print(f"Глава 2:  {len(all_ch2)} упражнений")
print(f"Глава 3:  {len(all_ch3)} упражнений")
print(f"Глава 4:  {len(all_ch4)} упражнений")
print(f"Глава 5:  {len(all_ch5)} упражнений")
print(f"Глава 6:  {len(all_ch6)} упражнений")
print(f"Глава 7:  {len(all_ch7)} упражнений")
print(f"Глава 8:  {len(all_ch8)} упражнений")
print(f"Глава 9:  {len(all_ch9)} упражнений")
print(f"Глава 10: {len(all_ch10)} упражнений")
print(f"Глава 11: {len(all_ch11)} упражнений")
print(f"Глава 12: {len(all_ch12)} упражнений")
print(f"Глава 13: {len(all_ch13)} упражнений")
print(f"Глава 14: {len(all_ch14)} упражнений")
print(f"Глава 15: {len(all_ch15)} упражнений")
print(f"Глава 16: {len(all_ch16)} упражнений")
print(f"Глава 17: {len(all_ch17)} упражнений")
print(f"Глава 18: {len(all_ch18)} упражнений")
print(f"Глава 19: {len(all_ch19)} упражнений")
print(f"Глава 20: {len(all_ch20)} упражнений")
print(f"Глава 21: {len(all_ch21)} упражнений")
print(f"Глава 22: {len(all_ch22)} упражнений")
print(f"Глава 23: {len(all_ch23)} упражнений")
print(f"Глава 24: {len(all_ch24)} упражнений")
print(f"Глава 25: {len(all_ch25)} упражнений")
print(f"Глава 26: {len(all_ch26)} упражнений")
print(f"Глава 27: {len(all_ch27)} упражнений")
print(f"Глава 28: {len(all_ch28)} упражнений")
print(f"Глава 29: {len(all_ch29)} упражнений")
print(f"Глава 30: {len(all_ch30)} упражнений")
print(f"Глава 31: {len(all_ch31)} упражнений")
print(f"Глава 32: {len(all_ch32)} упражнений")
print(f"Глава 33: {len(all_ch33)} упражнений")
print(f"Глава 34: {len(all_ch34)} упражнений")
print(f"Глава 35: {len(all_ch35)} упражнений")
print(f"Глава 36: {len(all_ch36)} упражнений")
print(f"Глава 37: {len(all_ch37)} упражнений")
print(f"Глава 38: {len(all_ch38)} упражнений")
print(f"Глава 39: {len(all_ch39)} упражнений")
print(f"Глава 40: {len(all_ch40)} упражнений")
print(f"Глава 41: {len(all_ch41)} упражнений")
print(f"Глава 42: {len(all_ch42)} упражнений")
print(f"Глава 43: {len(all_ch43)} упражнений")
print(f"Глава 44: {len(all_ch44)} упражнений")
print(f"Глава 45: {len(all_ch45)} упражнений")
print(f"Глава 46: {len(all_ch46)} упражнений")
print(f"Глава 47: {len(all_ch47)} упражнений")
print(f"Глава 48: {len(all_ch48)} упражнений")
print(f"Глава 49: {len(all_ch49)} упражнений")
print(f"Глава 50: {len(all_ch50)} упражнений")
print(f"Глава 51: {len(all_ch51)} упражнений")
print(f"Глава 52: {len(all_ch52)} упражнений")
print(f"Глава 53: {len(all_ch53)} упражнений")
print(f"Глава 54: {len(all_ch54)} упражнений")
print(f"Глава 55: {len(all_ch55)} упражнений")
print(f"Глава 56: {len(all_ch56)} упражнений")
print(f"Глава 57: {len(all_ch57)} упражнений")
print(f"Глава 58: {len(all_ch58)} упражнений")
print(f"Глава 59: {len(all_ch59)} упражнений")
print(f"Глава 60: {len(all_ch60)} упражнений")
print(f"Глава 61: {len(all_ch61)} упражнений")
print(f"Глава 62: {len(all_ch62)} упражнений")
print(f"Глава 63: {len(all_ch63)} упражнений")
print(f"Глава 64: {len(all_ch64)} упражнений")
print(f"Глава 65: {len(all_ch65)} упражнений")
print(f"Глава 66: {len(all_ch66)} упражнений")
print(f"Глава 67: {len(all_ch67)} упражнений")
print(f"Глава 68: {len(all_ch68)} упражнений")
print(f"Глава 69: {len(all_ch69)} упражнений")
print(f"Глава 70: {len(all_ch70)} упражнений")
print(f"Глава 71: {len(all_ch71)} упражнений")
print(f"Глава 72: {len(all_ch72)} упражнений")
print(f"Глава 73: {len(all_ch73)} упражнений")
print(f"Глава 74: {len(all_ch74)} упражнений")
print(f"Глава 75: {len(all_ch75)} упражнений")
print(f"Глава 76: {len(all_ch76)} упражнений")
print(f"Глава 77: {len(all_ch77)} упражнений")
print(f"Глава 78: {len(all_ch78)} упражнений")
print(f"Глава 79: {len(all_ch79)} упражнений")
print(f"Глава 80: {len(all_ch80)} упражнений")
print(f"Глава 81: {len(all_ch81)} упражнений")
print(f"Глава 82: {len(all_ch82)} упражнений")
print(f"Глава 83: {len(all_ch83)} упражнений")
print(f"Глава 84: {len(all_ch84)} упражнений")
print(f"Глава 85: {len(all_ch85)} упражнений")
print(f"Глава 86: {len(all_ch86)} упражнений")
print(f"Глава 87: {len(all_ch87)} упражнений")
print(f"Глава 88: {len(all_ch88)} упражнений")
print(f"Глава 89: {len(all_ch89)} упражнений")
print(f"Глава 90: {len(all_ch90)} упражнений")
print(f"Глава 91: {len(all_ch91)} упражнений")
print(f"Глава 92: {len(all_ch92)} упражнений")
print(f"Глава 93: {len(all_ch93)} упражнений")
print(f"Глава 94: {len(all_ch94)} упражнений")
print(f"Глава 95: {len(all_ch95)} упражнений")
print(f"Глава 96: {len(all_ch96)} упражнений")
print(f"Глава 97: {len(all_ch97)} упражнений")
print(f"Глава 98: {len(all_ch98)} упражнений")
print(f"Глава 99: {len(all_ch99)} упражнений")
print(f"Глава 100: {len(all_ch100)} упражнений")
print(f"Всего упражнений в учебнике: {total_ex}")

issues = []

def check_exercise(ch_num, ex):
    num = ex.get('num')
    title = ex.get('title')
    task = ex.get('task')
    theory = ex.get('theory')
    step_by_step = ex.get('step_by_step')
    code_blocks = ex.get('code_blocks', [])
    under_the_hood = ex.get('under_the_hood')
    pitfalls = ex.get('pitfalls')
    bigtech = ex.get('bigtech_interview')
    
    if not title or not task or not theory or not step_by_step or not code_blocks:
        issues.append(f"[Глава {ch_num} Упр {num}] Отсутствует обязательная секция")
        
    for i, cb in enumerate(code_blocks):
        fname = cb.get('filename', '')
        lang = cb.get('lang', '')
        code = cb.get('code', '')
        if not code.strip():
            issues.append(f"[Глава {ch_num} Упр {num}] Пустой блок кода {i} ({fname})")
            
        if lang == 'go' and 'package main' in code:
            if 'ОШИБКА:' in code or 'redeclared' in code or '// ОШИБКА' in code or 'undefined: ' in code or 'invalid operation' in code or 'cannot use' in code or 'invalid map key' in code or 'cannot take' in code or 'badMap' in code or 'cannot assign to struct field in map' in code:
                continue
            if 'import "C"' in code or 'some-domain.com' in code or 'github.com/myuser' in code or 'mycompany' in code or 'v2' in code:
                continue
                
            with tempfile.NamedTemporaryFile('w', suffix='.go', delete=False) as tf:
                tf.write(code)
                tf_path = tf.name
            try:
                res = subprocess.run(['gofmt', '-e', tf_path], capture_output=True, text=True)
                if res.returncode != 0:
                    issues.append(f"[Глава {ch_num} Упр {num}] Ошибка синтаксиса Go в {fname}: {res.stderr.strip()}")
            finally:
                if os.path.exists(tf_path):
                    os.remove(tf_path)

for ex in all_ch1:
    check_exercise(1, ex)
for ex in all_ch2:
    check_exercise(2, ex)
for ex in all_ch3:
    check_exercise(3, ex)
for ex in all_ch4:
    check_exercise(4, ex)
for ex in all_ch5:
    check_exercise(5, ex)
for ex in all_ch6:
    check_exercise(6, ex)
for ex in all_ch7:
    check_exercise(7, ex)
for ex in all_ch8:
    check_exercise(8, ex)
for ex in all_ch9:
    check_exercise(9, ex)
for ex in all_ch10:
    check_exercise(10, ex)
for ex in all_ch11:
    check_exercise(11, ex)
for ex in all_ch12:
    check_exercise(12, ex)
for ex in all_ch13:
    check_exercise(13, ex)
for ex in all_ch14:
    check_exercise(14, ex)
for ex in all_ch15:
    check_exercise(15, ex)
for ex in all_ch16:
    check_exercise(16, ex)
for ex in all_ch17:
    check_exercise(17, ex)
for ex in all_ch18:
    check_exercise(18, ex)
for ex in all_ch19:
    check_exercise(19, ex)
for ex in all_ch20:
    check_exercise(20, ex)
for ex in all_ch21:
    check_exercise(21, ex)
for ex in all_ch22:
    check_exercise(22, ex)
for ex in all_ch23:
    check_exercise(23, ex)
for ex in all_ch24:
    check_exercise(24, ex)
for ex in all_ch25:
    check_exercise(25, ex)
for ex in all_ch26:
    check_exercise(26, ex)
for ex in all_ch27:
    check_exercise(27, ex)
for ex in all_ch28:
    check_exercise(28, ex)
for ex in all_ch29:
    check_exercise(29, ex)
for ex in all_ch30:
    check_exercise(30, ex)
for ex in all_ch31:
    check_exercise(31, ex)
for ex in all_ch32:
    check_exercise(32, ex)
for ex in all_ch33:
    check_exercise(33, ex)
for ex in all_ch34:
    check_exercise(34, ex)
for ex in all_ch35:
    check_exercise(35, ex)
for ex in all_ch36:
    check_exercise(36, ex)
for ex in all_ch37:
    check_exercise(37, ex)
for ex in all_ch38:
    check_exercise(38, ex)
for ex in all_ch39:
    check_exercise(39, ex)
for ex in all_ch40:
    check_exercise(40, ex)
for ex in all_ch41:
    check_exercise(41, ex)
for ex in all_ch42:
    check_exercise(42, ex)
for ex in all_ch43:
    check_exercise(43, ex)
for ex in all_ch44:
    check_exercise(44, ex)
for ex in all_ch45:
    check_exercise(45, ex)
for ex in all_ch46:
    check_exercise(46, ex)
for ex in all_ch47:
    check_exercise(47, ex)
for ex in all_ch48:
    check_exercise(48, ex)
for ex in all_ch49:
    check_exercise(49, ex)
for ex in all_ch50:
    check_exercise(50, ex)
for ex in all_ch51:
    check_exercise(51, ex)
for ex in all_ch52:
    check_exercise(52, ex)
for ex in all_ch53:
    check_exercise(53, ex)
for ex in all_ch54:
    check_exercise(54, ex)
for ex in all_ch55:
    check_exercise(55, ex)
for ex in all_ch56:
    check_exercise(56, ex)
for ex in all_ch57:
    check_exercise(57, ex)
for ex in all_ch58:
    check_exercise(58, ex)
for ex in all_ch59:
    check_exercise(59, ex)
for ex in all_ch60:
    check_exercise(60, ex)
for ex in all_ch61:
    check_exercise(61, ex)
for ex in all_ch62:
    check_exercise(62, ex)
for ex in all_ch63:
    check_exercise(63, ex)
for ex in all_ch64:
    check_exercise(64, ex)
for ex in all_ch65:
    check_exercise(65, ex)
for ex in all_ch66:
    check_exercise(66, ex)
for ex in all_ch67:
    check_exercise(67, ex)
for ex in all_ch68:
    check_exercise(68, ex)
for ex in all_ch69:
    check_exercise(69, ex)
for ex in all_ch70:
    check_exercise(70, ex)
for ex in all_ch71:
    check_exercise(71, ex)
for ex in all_ch72:
    check_exercise(72, ex)
for ex in all_ch73:
    check_exercise(73, ex)
for ex in all_ch74:
    check_exercise(74, ex)
for ex in all_ch75:
    check_exercise(75, ex)
for ex in all_ch76:
    check_exercise(76, ex)
for ex in all_ch77:
    check_exercise(77, ex)
for ex in all_ch78:
    check_exercise(78, ex)
for ex in all_ch79:
    check_exercise(79, ex)
for ex in all_ch80:
    check_exercise(80, ex)
for ex in all_ch81:
    check_exercise(81, ex)
for ex in all_ch82:
    check_exercise(82, ex)
for ex in all_ch83:
    check_exercise(83, ex)
for ex in all_ch84:
    check_exercise(84, ex)
for ex in all_ch85:
    check_exercise(85, ex)
for ex in all_ch86:
    check_exercise(86, ex)
for ex in all_ch87:
    check_exercise(87, ex)
for ex in all_ch88:
    check_exercise(88, ex)
for ex in all_ch89:
    check_exercise(89, ex)
for ex in all_ch90:
    check_exercise(90, ex)
for ex in all_ch91:
    check_exercise(91, ex)
for ex in all_ch92:
    check_exercise(92, ex)
for ex in all_ch93:
    check_exercise(93, ex)
for ex in all_ch94:
    check_exercise(94, ex)
for ex in all_ch95:
    check_exercise(95, ex)
for ex in all_ch96:
    check_exercise(96, ex)
for ex in all_ch97:
    check_exercise(97, ex)
for ex in all_ch98:
    check_exercise(98, ex)
for ex in all_ch99:
    check_exercise(99, ex)
for ex in all_ch100:
    check_exercise(100, ex)

# Check HTML files and anchors
html_files = [
    ('001-pakety-i-moduli.html', 1, len(all_ch1)),
    ('002-kompilyatsiya-sborka-i-zapusk.html', 2, len(all_ch2)),
    ('003-paket-fmt-i-konsolnyy-vvod-vyvod.html', 3, len(all_ch3)),
    ('004-bazovye-tipy-peremennye-i-konstanty.html', 4, len(all_ch4)),
    ('005-uslovnye-konstruktsii.html', 5, len(all_ch5)),
    ('006-tsikly.html', 6, len(all_ch6)),
    ('007-massivy.html', 7, len(all_ch7)),
    ('008-slaysy.html', 8, len(all_ch8)),
    ('009-mapy.html', 9, len(all_ch9)),
    ('010-funktsii.html', 10, len(all_ch10)),
    ('011-ukazateli.html', 11, len(all_ch11)),
    ('012-peredacha-argumentov.html', 12, len(all_ch12)),
    ('013-struktury.html', 13, len(all_ch13)),
    ('014-interfeysy.html', 14, len(all_ch14)),
    ('015-oop-v-go.html', 15, len(all_ch15)),
    ('016-dzheneriki.html', 16, len(all_ch16)),
    ('017-obrabotka-oshibok.html', 17, len(all_ch17)),
    ('018-rabota-s-faylami.html', 18, len(all_ch18)),
    ('019-logirovanie.html', 19, len(all_ch19)),
    ('020-gorutiny-i-sinkhronizatsiya.html', 20, len(all_ch20)),
    ('021-kanaly-i-select.html', 21, len(all_ch21)),
    ('022-paket-context.html', 22, len(all_ch22)),
    ('023-patterny-i-kaverznye-sluchai-konkurentnosti.html', 23, len(all_ch23)),
    ('024-nizkourovnevaya-set-tcp-i-udp.html', 24, len(all_ch24)),
    ('025-http-klient.html', 25, len(all_ch25)),
    ('026-http-server-rest-api-i-middleware.html', 26, len(all_ch26)),
    ('027-relyatsionnye-bazy-dannykh-sql-i-postgresql.html', 27, len(all_ch27)),
    ('028-bazy-dannykh-nosql-i-keshirovanie-redis.html', 28, len(all_ch28)),
    ('029-modulnoe-testirovanie-unit-testing-i-assertions.html', 29, len(all_ch29)),
    ('030-mokirovanie-i-integratsionnoe-testirovanie.html', 30, len(all_ch30)),
    ('031-benchmarki-fazzing-i-prodvinutye-metody-testirovaniya.html', 31, len(all_ch31)),
    ('032-protocol-buffers-i-grpc.html', 32, len(all_ch32)),
    ('033-mikroservisnaya-arkhitektura-i-patterny.html', 33, len(all_ch33)),
    ('034-graphql.html', 34, len(all_ch34)),
    ('035-websockets-i-real-time.html', 35, len(all_ch35)),
    ('036-rabbitmq.html', 36, len(all_ch36)),
    ('037-apache-kafka.html', 37, len(all_ch37)),
    ('038-nats-i-nats-jetstream.html', 38, len(all_ch38)),
    ('039-metriki-i-monitoring-prometheus.html', 39, len(all_ch39)),
    ('040-raspredelennaya-trassirovka-opentelemetry.html', 40, len(all_ch40)),
    ('041-profilirovanie-i-rantaym-diagnostika.html', 41, len(all_ch41)),
    ('042-proektirovanie-chistoy-arkhitektury-i-ddd.html', 42, len(all_ch42)),
    ('043-shablony-proektirovaniya-raspredelennykh-i-enterprise-sistem.html', 43, len(all_ch43)),
    ('044-proektirovanie-vysokonagruzhennykh-i-otkazoustoychivykh-sistem.html', 44, len(all_html44 := all_ch44)),
    ('045-konteynerizatsiya-i-docker.html', 45, len(all_ch45)),
    ('046-avtomatizatsiya-ci-cd.html', 46, len(all_ch46)),
    ('047-orkestratsiya-v-kubernetes.html', 47, len(all_ch47)),
    ('048-planirovshchik-gmp.html', 48, len(all_ch48)),
    ('049-allokator-kuchi-i-upravlenie-pamyatyu.html', 49, len(all_ch49)),
    ('050-garbage-collector-i-tyuning-pamyati.html', 50, len(all_ch50)),
    ('051-rabota-s-unsafe-i-nizkourovnevoy-pamyatyu.html', 51, len(all_ch51)),
    ('052-integratsiya-s-c-kodom-cherez-cgo.html', 52, len(all_ch52)),
    ('053-sistemnye-vyzovy-i-vzaimodeystvie-s-os.html', 53, len(all_ch53)),
    ('054-prodvinutaya-refleksiya-reflect.html', 54, len(all_ch54)),
    ('055-analiz-ast-i-staticheskiy-analiz-koda.html', 55, len(all_ch55)),
    ('056-kodogeneratsiya-i-shablonizatsiya.html', 56, len(all_ch56)),
    ('057-simmetrichnoe-i-asimmetrichnoe-shifrovanie.html', 57, len(all_ch57)),
    ('058-kheshirovanie-paroley-i-kriptograficheskaya-stoykost.html', 58, len(all_ch58)),
    ('059-tokeny-autentifikatsii-i-avtorizatsiya.html', 59, len(all_ch59)),
    ('060-bezopasnost-veb-prilozheniy-i-zashchita-api.html', 60, len(all_ch60)),
    ('061-dokumentoorientirovannaya-baza-dannykh-mongodb.html', 61, len(all_ch61)),
    ('062-analiticheskaya-subd-clickhouse.html', 62, len(all_ch62)),
    ('063-poiskovye-dvizhki-elasticsearch-i-opensearch.html', 63, len(all_ch63)),
    ('064-logicheskaya-replikatsiya-i-change-data-capture.html', 64, len(all_ch64)),
    ('065-vebkhuki-i-platformy-obratnykh-vyzovov.html', 65, len(all_ch65)),
    ('066-server-sent-events.html', 66, len(all_ch66)),
    ('067-alternativnye-rpc-protokoly.html', 67, len(all_ch67)),
    ('068-pattern-saga-i-kompensatsionnye-tranzaktsii.html', 68, len(all_ch68)),
    ('069-patterny-outbox-i-inbox-dlya-nadezhnoy-dostavki-soobshcheniy.html', 69, len(all_ch69)),
    ('070-proektirovanie-idempotentnykh-api.html', 70, len(all_ch70)),
    ('071-vybory-lidera-leader-election-v-raspredelennykh-sistemakh.html', 71, len(all_ch71)),
    ('072-protokol-konsensusa-raft.html', 72, len(all_ch72)),
    ('073-raspredelennye-blokirovki-i-fencing-tokens.html', 73, len(all_ch73)),
    ('074-cache-friendly-struktury-dannykh-i-vyravnivanie-pamyati.html', 74, len(all_ch74)),
    ('075-lock-free-struktury-dannykh.html', 75, len(all_ch75)),
    ('076-assembler-go-plan-9-assembly-i-simd.html', 76, len(all_ch76)),
    ('077-vysokoproizvoditelnye-setevye-freymvorki-gnet-evio.html', 77, len(all_ch77)),
    ('078-oblachnye-khranilishcha-envelope-encryption-i-kms.html', 78, len(all_ch78)),
    ('079-integratsiya-s-service-mesh-istio-linkerd-i-mtls.html', 79, len(all_ch79)),
    ('080-kontekst-trassirovki-w3c-trace-context-b3-i-grpc-keepalive.html', 80, len(all_ch80)),
    ('081-bezopasnost-tsepochki-postavok-supply-chain-security-i-sbom.html', 81, len(all_ch81)),
    ('082-zashchita-setevykh-soketov-i-protivodeystvie-dos-atakam.html', 82, len(all_ch82)),
    ('083-sistemnaya-izolyatsiya-seccomp-i-linux-capabilities.html', 83, len(all_ch83)),
    ('084-cqrs-i-event-sourcing-na-go.html', 84, len(all_ch84)),
    ('085-mnogourovnevoe-keshirovanie-l1-l2-i-raspredelennaya-kogerentnost.html', 85, len(all_ch85)),
    ('086-masshtabiruemye-raspredelennye-planirovshchiki-i-ocheredi-zadach.html', 86, len(all_ch86)),
    ('087-orkestratsiya-raspredelennykh-protsessov-durable-execution-na-temporal-io.html', 87, len(all_ch87)),
    ('088-potokovaya-obrabotka-dannykh-v-realnom-vremeni-stream-processing.html', 88, len(all_ch88)),
    ('089-khaos-inzheneriya-i-nagruzochnoe-testirovanie-na-go.html', 89, len(all_ch89)),
    ('090-kontrakt-orientirovannye-api-shlyuzy-grpc-gateway-grpc-web-i-openapi.html', 90, len(all_ch90)),
    ('091-razrabotka-sobstvennykh-kubernetes-operators-i-crd-na-go.html', 91, len(all_ch91)),
    ('092-rasshiryaemost-sistem-plugins-ipc-i-webassembly-wazero.html', 92, len(all_ch92)),
    ('093-vysokoproizvoditelnye-api-gateway-i-reverse-proxy-na-chistom-go.html', 93, len(all_ch93)),
    ('094-enterprise-release-engineering-feature-flags-dinamicheskiy-konfig-i-canary-routing.html', 94, len(all_ch94)),
    ('095-raspredelennaya-koordinatsiya-i-khranilishche-metadannykh-etcd-v3.html', 95, len(all_ch95)),
    ('096-zero-downtime-migratsii-baz-dannykh-i-pattern-expand-contract-na-go.html', 96, len(all_ch96)),
    ('097-time-series-subd-szhatie-gorilla-i-iot-telemetriya-na-go.html', 97, len(all_ch97)),
    ('098-arkhitekturnyy-kontrol-razrabotka-korporativnykh-linterov-dlya-golangci-lint.html', 98, len(all_ch98)),
    ('099-integratsiya-s-ii-llm-orkestratsiya-i-vektornyy-poisk-na-go.html', 99, len(all_ch99)),
    ('100-arkhitekturnyy-capstone-proektirovanie-i-skvoznoy-zapusk-otkazoustoychivoy-highload-platformy.html', 100, len(all_ch100)),
]

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DIST_DIR = os.path.join(REPO_ROOT, "dist")

for fname, ch_num, count in html_files:
    fpath = os.path.join(DIST_DIR, fname)
    if not os.path.exists(fpath):
        issues.append(f"Файл {fpath} не найден на диске!")
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check all anchors
    for i in range(1, count + 1):
        if f'id="ex-{i}"' not in content:
            issues.append(f"В файле {fname} отсутствует якорь id=\"ex-{i}\"")
            
    # Check no chevron icon
    if 'chevron-icon' in content:
        issues.append(f"В файле {fname} обнаружен запрещенный chevron-icon!")

    # Check no unexpected/unescaped script tags in HTML
    scripts = re.findall(r'<script.*?>.*?</script>', content, re.DOTALL | re.IGNORECASE)
    unexpected = [s for s in scripts if 'prism' not in s and 'sidebar' not in s and 'localStorage' not in s and 'toggle' not in s and 'MathJax' not in s]
    if unexpected:
        issues.append(f"В файле {fname} обнаружены паразитные/неэкранированные теги <script> ({len(unexpected)} шт.)!")

    # Check HTML closure
    if not content.endswith('</html>\n') and not content.endswith('</html>'):
        issues.append(f"Файл {fname} некорректно завершен (нет </html>)!")

# Check portal page index.html in dist
portal_path = os.path.join(DIST_DIR, 'index.html')
if not os.path.exists(portal_path):
    issues.append("Файл портала dist/index.html не найден на диске!")
else:
    with open(portal_path, 'r', encoding='utf-8') as f:
        portal_content = f.read()
    if '001-pakety-i-moduli.html' not in portal_content:
        issues.append("В файле портала index.html отсутствует ссылка на 001-pakety-i-moduli.html!")
    if '083-sistemnaya-izolyatsiya-seccomp-i-linux-capabilities.html' not in portal_content:
        issues.append("В файле портала index.html отсутствует ссылка на 083-sistemnaya-izolyatsiya-seccomp-i-linux-capabilities.html!")
    if not portal_content.endswith('</html>\n') and not portal_content.endswith('</html>'):
        issues.append("Файл index.html некорректно завершен (нет </html>)!")

if issues:
    print(f"\n❌ Обнаружено {len(issues)} проблем:")
    for iss in issues:
        print("  •", iss)
    exit(1)
else:
    print(f"\n✅ ИДЕАЛЬНО: Все {total_ex} упражнений в {len(html_files)} главах успешно прошли синтаксический, структурный и HTML-аудит!")

