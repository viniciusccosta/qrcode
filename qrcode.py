from copy import deepcopy

# ========== CONSTANTS =================================================================================================
PADS_BYTES              = ["11101100",
                           "00010001"]
MODE_IND                = {'Numeric'     : '0001',
                       'Alphanumeric': '0010',
                       'Byte'        : '0100',
                       'Kanji'       : '1000',
                       'ECI'         : '0111',}
ALPHANUMERIC_TABLE      = {'0':  0, '1':  1, '2':  2, '3':  3, '4':  4, '5':  5, '6':  6, '7':  7, '8':  8, '9':  9,
                       'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19,
                       'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29,
                       'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35, ' ': 36, '$': 37, '%': 38, '*': 39,
                       '+': 40, '-': 41, '.': 42, '/': 43, ':': 44,}
UPPER_LIMITS            = {  ( 1, 'L'): {'Numeric':   41, 'Alphanumeric':   25, 'Byte':   17, 'Kanji':   10}, (1, 'M'): {'Numeric': 34, 'Alphanumeric': 20, 'Byte': 14, 'Kanji': 8}, (1, 'Q'): {'Numeric': 27, 'Alphanumeric': 16, 'Byte': 11, 'Kanji': 7}, (1, 'H'): {'Numeric': 17, 'Alphanumeric': 10, 'Byte': 7, 'Kanji': 4},
                             ( 2, 'L'): {'Numeric':   77, 'Alphanumeric':   47, 'Byte':   32, 'Kanji':   20}, (2, 'M'): {'Numeric': 63, 'Alphanumeric': 38, 'Byte': 26, 'Kanji': 16}, (2, 'Q'): {'Numeric': 48, 'Alphanumeric': 29, 'Byte': 20, 'Kanji': 12}, (2, 'H'): {'Numeric': 34, 'Alphanumeric': 20, 'Byte': 14, 'Kanji': 8},
                             ( 3, 'L'): {'Numeric':  127, 'Alphanumeric':   77, 'Byte':   53, 'Kanji':   32}, (3, 'M'): {'Numeric': 101, 'Alphanumeric': 61, 'Byte': 42, 'Kanji': 26}, (3, 'Q'): {'Numeric': 77, 'Alphanumeric': 47, 'Byte': 32, 'Kanji': 20}, (3, 'H'): {'Numeric': 58, 'Alphanumeric': 35, 'Byte': 24, 'Kanji': 15},
                             ( 4, 'L'): {'Numeric':  187, 'Alphanumeric':  114, 'Byte':   78, 'Kanji':   48}, (4, 'M'): {'Numeric': 149, 'Alphanumeric': 90, 'Byte': 62, 'Kanji': 38}, (4, 'Q'): {'Numeric': 111, 'Alphanumeric': 67, 'Byte': 46, 'Kanji': 28}, (4, 'H'): {'Numeric': 82, 'Alphanumeric': 50, 'Byte': 34, 'Kanji': 21},
                             ( 5, 'L'): {'Numeric':  255, 'Alphanumeric':  154, 'Byte':  106, 'Kanji':   65}, (5, 'M'): {'Numeric': 202, 'Alphanumeric': 122, 'Byte': 84, 'Kanji': 52}, (5, 'Q'): {'Numeric': 144, 'Alphanumeric': 87, 'Byte': 60, 'Kanji': 37}, (5, 'H'): {'Numeric': 106, 'Alphanumeric': 64, 'Byte': 44, 'Kanji': 27},
                             ( 6, 'L'): {'Numeric':  322, 'Alphanumeric':  195, 'Byte':  134, 'Kanji':   82}, (6, 'M'): {'Numeric': 255, 'Alphanumeric': 154, 'Byte': 106, 'Kanji': 65}, (6, 'Q'): {'Numeric': 178, 'Alphanumeric': 108, 'Byte': 74, 'Kanji': 45}, (6, 'H'): {'Numeric': 139, 'Alphanumeric': 84, 'Byte': 58, 'Kanji': 36},
                             ( 7, 'L'): {'Numeric':  370, 'Alphanumeric':  224, 'Byte':  154, 'Kanji':   95}, (7, 'M'): {'Numeric': 293, 'Alphanumeric': 178, 'Byte': 122, 'Kanji': 75}, (7, 'Q'): {'Numeric': 207, 'Alphanumeric': 125, 'Byte': 86, 'Kanji': 53}, (7, 'H'): {'Numeric': 154, 'Alphanumeric': 93, 'Byte': 64, 'Kanji': 39},
                             ( 8, 'L'): {'Numeric':  461, 'Alphanumeric':  279, 'Byte':  192, 'Kanji':  118}, (8, 'M'): {'Numeric': 365, 'Alphanumeric': 221, 'Byte': 152, 'Kanji': 93}, (8, 'Q'): {'Numeric': 259, 'Alphanumeric': 157, 'Byte': 108, 'Kanji': 66}, (8, 'H'): {'Numeric': 202, 'Alphanumeric': 122, 'Byte': 84, 'Kanji': 52},
                             ( 9, 'L'): {'Numeric':  552, 'Alphanumeric':  335, 'Byte':  230, 'Kanji':  141}, (9, 'M'): {'Numeric': 432, 'Alphanumeric': 262, 'Byte': 180, 'Kanji': 111}, (9, 'Q'): {'Numeric': 312, 'Alphanumeric': 189, 'Byte': 130, 'Kanji': 80}, (9, 'H'): {'Numeric': 235, 'Alphanumeric': 143, 'Byte': 98, 'Kanji': 60},
                             (10, 'L'): {'Numeric':  652, 'Alphanumeric':  395, 'Byte':  271, 'Kanji':  167}, (10, 'M'): {'Numeric': 513, 'Alphanumeric': 311, 'Byte': 213, 'Kanji': 131}, (10, 'Q'): {'Numeric': 364, 'Alphanumeric': 221, 'Byte': 151, 'Kanji': 93}, (10, 'H'): {'Numeric': 288, 'Alphanumeric': 174, 'Byte': 119, 'Kanji': 74},
                             (11, 'L'): {'Numeric':  772, 'Alphanumeric':  468, 'Byte':  321, 'Kanji':  198}, (11, 'M'): {'Numeric': 604, 'Alphanumeric': 366, 'Byte': 251, 'Kanji': 155}, (11, 'Q'): {'Numeric': 427, 'Alphanumeric': 259, 'Byte': 177, 'Kanji': 109}, (11, 'H'): {'Numeric': 331, 'Alphanumeric': 200, 'Byte': 137, 'Kanji': 85},
                             (12, 'L'): {'Numeric':  883, 'Alphanumeric':  535, 'Byte':  367, 'Kanji':  226}, (12, 'M'): {'Numeric': 691, 'Alphanumeric': 419, 'Byte': 287, 'Kanji': 177}, (12, 'Q'): {'Numeric': 489, 'Alphanumeric': 296, 'Byte': 203, 'Kanji': 125}, (12, 'H'): {'Numeric': 374, 'Alphanumeric': 227, 'Byte': 155, 'Kanji': 96},
                             (13, 'L'): {'Numeric': 1022, 'Alphanumeric':  619, 'Byte':  425, 'Kanji':  262}, (13, 'M'): {'Numeric': 796, 'Alphanumeric': 483, 'Byte': 331, 'Kanji': 204}, (13, 'Q'): {'Numeric': 580, 'Alphanumeric': 352, 'Byte': 241, 'Kanji': 149}, (13, 'H'): {'Numeric': 427, 'Alphanumeric': 259, 'Byte': 177, 'Kanji': 109},
                             (14, 'L'): {'Numeric': 1101, 'Alphanumeric':  667, 'Byte':  458, 'Kanji':  282}, (14, 'M'): {'Numeric': 871, 'Alphanumeric': 528, 'Byte': 362, 'Kanji': 223}, (14, 'Q'): {'Numeric': 621, 'Alphanumeric': 376, 'Byte': 258, 'Kanji': 159}, (14, 'H'): {'Numeric': 468, 'Alphanumeric': 283, 'Byte': 194, 'Kanji': 120},
                             (15, 'L'): {'Numeric': 1250, 'Alphanumeric':  758, 'Byte':  520, 'Kanji':  320}, (15, 'M'): {'Numeric': 991, 'Alphanumeric': 600, 'Byte': 412, 'Kanji': 254}, (15, 'Q'): {'Numeric': 703, 'Alphanumeric': 426, 'Byte': 292, 'Kanji': 180}, (15, 'H'): {'Numeric': 530, 'Alphanumeric': 321, 'Byte': 220, 'Kanji': 136},
                             (16, 'L'): {'Numeric': 1408, 'Alphanumeric':  854, 'Byte':  586, 'Kanji':  361}, (16, 'M'): {'Numeric': 1082, 'Alphanumeric': 656, 'Byte': 450, 'Kanji': 277}, (16, 'Q'): {'Numeric': 775, 'Alphanumeric': 470, 'Byte': 322, 'Kanji': 198}, (16, 'H'): {'Numeric': 602, 'Alphanumeric': 365, 'Byte': 250, 'Kanji': 154},
                             (17, 'L'): {'Numeric': 1548, 'Alphanumeric':  938, 'Byte':  644, 'Kanji':  397}, (17, 'M'): {'Numeric': 1212, 'Alphanumeric': 734, 'Byte': 504, 'Kanji': 310}, (17, 'Q'): {'Numeric': 876, 'Alphanumeric': 531, 'Byte': 364, 'Kanji': 224}, (17, 'H'): {'Numeric': 674, 'Alphanumeric': 408, 'Byte': 280, 'Kanji': 173},
                             (18, 'L'): {'Numeric': 1725, 'Alphanumeric': 1046, 'Byte':  718, 'Kanji':  442}, (18, 'M'): {'Numeric': 1346, 'Alphanumeric': 816, 'Byte': 560, 'Kanji': 345}, (18, 'Q'): {'Numeric': 948, 'Alphanumeric': 574, 'Byte': 394, 'Kanji': 243}, (18, 'H'): {'Numeric': 746, 'Alphanumeric': 452, 'Byte': 310, 'Kanji': 191},
                             (19, 'L'): {'Numeric': 1903, 'Alphanumeric': 1153, 'Byte':  792, 'Kanji':  488}, (19, 'M'): {'Numeric': 1500, 'Alphanumeric': 909, 'Byte': 624, 'Kanji': 384}, (19, 'Q'): {'Numeric': 1063, 'Alphanumeric': 644, 'Byte': 442, 'Kanji': 272}, (19, 'H'): {'Numeric': 813, 'Alphanumeric': 493, 'Byte': 338, 'Kanji': 208},
                             (20, 'L'): {'Numeric': 2061, 'Alphanumeric': 1249, 'Byte':  858, 'Kanji':  528}, (20, 'M'): {'Numeric': 1600, 'Alphanumeric': 970, 'Byte': 666, 'Kanji': 410}, (20, 'Q'): {'Numeric': 1159, 'Alphanumeric': 702, 'Byte': 482, 'Kanji': 297}, (20, 'H'): {'Numeric': 919, 'Alphanumeric': 557, 'Byte': 382, 'Kanji': 235},
                             (21, 'L'): {'Numeric': 2232, 'Alphanumeric': 1352, 'Byte':  929, 'Kanji':  572}, (21, 'M'): {'Numeric': 1708, 'Alphanumeric': 1035, 'Byte': 711, 'Kanji': 438}, (21, 'Q'): {'Numeric': 1224, 'Alphanumeric': 742, 'Byte': 509, 'Kanji': 314}, (21, 'H'): {'Numeric': 969, 'Alphanumeric': 587, 'Byte': 403, 'Kanji': 248},
                             (22, 'L'): {'Numeric': 2409, 'Alphanumeric': 1460, 'Byte': 1003, 'Kanji':  618}, (22, 'M'): {'Numeric': 1872, 'Alphanumeric': 1134, 'Byte': 779, 'Kanji': 480}, (22, 'Q'): {'Numeric': 1358, 'Alphanumeric': 823, 'Byte': 565, 'Kanji': 348}, (22, 'H'): {'Numeric': 1056, 'Alphanumeric': 640, 'Byte': 439, 'Kanji': 270},
                             (23, 'L'): {'Numeric': 2620, 'Alphanumeric': 1588, 'Byte': 1091, 'Kanji':  672}, (23, 'M'): {'Numeric': 2059, 'Alphanumeric': 1248, 'Byte': 857, 'Kanji': 528}, (23, 'Q'): {'Numeric': 1468, 'Alphanumeric': 890, 'Byte': 611, 'Kanji': 376}, (23, 'H'): {'Numeric': 1108, 'Alphanumeric': 672, 'Byte': 461, 'Kanji': 284},
                             (24, 'L'): {'Numeric': 2812, 'Alphanumeric': 1704, 'Byte': 1171, 'Kanji':  721}, (24, 'M'): {'Numeric': 2188, 'Alphanumeric': 1326, 'Byte': 911, 'Kanji': 561}, (24, 'Q'): {'Numeric': 1588, 'Alphanumeric': 963, 'Byte': 661, 'Kanji': 407}, (24, 'H'): {'Numeric': 1228, 'Alphanumeric': 744, 'Byte': 511, 'Kanji': 315},
                             (25, 'L'): {'Numeric': 3057, 'Alphanumeric': 1853, 'Byte': 1273, 'Kanji':  784}, (25, 'M'): {'Numeric': 2395, 'Alphanumeric': 1451, 'Byte': 997, 'Kanji': 614}, (25, 'Q'): {'Numeric': 1718, 'Alphanumeric': 1041, 'Byte': 715, 'Kanji': 440}, (25, 'H'): {'Numeric': 1286, 'Alphanumeric': 779, 'Byte': 535, 'Kanji': 330},
                             (26, 'L'): {'Numeric': 3283, 'Alphanumeric': 1990, 'Byte': 1367, 'Kanji':  842}, (26, 'M'): {'Numeric': 2544, 'Alphanumeric': 1542, 'Byte': 1059, 'Kanji': 652}, (26, 'Q'): {'Numeric': 1804, 'Alphanumeric': 1094, 'Byte': 751, 'Kanji': 462}, (26, 'H'): {'Numeric': 1425, 'Alphanumeric': 864, 'Byte': 593, 'Kanji': 365},
                             (27, 'L'): {'Numeric': 3517, 'Alphanumeric': 2132, 'Byte': 1465, 'Kanji':  902}, (27, 'M'): {'Numeric': 2701, 'Alphanumeric': 1637, 'Byte': 1125, 'Kanji': 692}, (27, 'Q'): {'Numeric': 1933, 'Alphanumeric': 1172, 'Byte': 805, 'Kanji': 496}, (27, 'H'): {'Numeric': 1501, 'Alphanumeric': 910, 'Byte': 625, 'Kanji': 385},
                             (28, 'L'): {'Numeric': 3669, 'Alphanumeric': 2223, 'Byte': 1528, 'Kanji':  940}, (28, 'M'): {'Numeric': 2857, 'Alphanumeric': 1732, 'Byte': 1190, 'Kanji': 732}, (28, 'Q'): {'Numeric': 2085, 'Alphanumeric': 1263, 'Byte': 868, 'Kanji': 534}, (28, 'H'): {'Numeric': 1581, 'Alphanumeric': 958, 'Byte': 658, 'Kanji': 405},
                             (29, 'L'): {'Numeric': 3909, 'Alphanumeric': 2369, 'Byte': 1628, 'Kanji': 1002}, (29, 'M'): {'Numeric': 3035, 'Alphanumeric': 1839, 'Byte': 1264, 'Kanji': 778}, (29, 'Q'): {'Numeric': 2181, 'Alphanumeric': 1322, 'Byte': 908, 'Kanji': 559}, (29, 'H'): {'Numeric': 1677, 'Alphanumeric': 1016, 'Byte': 698, 'Kanji': 430},
                             (30, 'L'): {'Numeric': 4158, 'Alphanumeric': 2520, 'Byte': 1732, 'Kanji': 1066}, (30, 'M'): {'Numeric': 3289, 'Alphanumeric': 1994, 'Byte': 1370, 'Kanji': 843}, (30, 'Q'): {'Numeric': 2358, 'Alphanumeric': 1429, 'Byte': 982, 'Kanji': 604}, (30, 'H'): {'Numeric': 1782, 'Alphanumeric': 1080, 'Byte': 742, 'Kanji': 457},
                             (31, 'L'): {'Numeric': 4417, 'Alphanumeric': 2677, 'Byte': 1840, 'Kanji': 1132}, (31, 'M'): {'Numeric': 3486, 'Alphanumeric': 2113, 'Byte': 1452, 'Kanji': 894}, (31, 'Q'): {'Numeric': 2473, 'Alphanumeric': 1499, 'Byte': 1030, 'Kanji': 634}, (31, 'H'): {'Numeric': 1897, 'Alphanumeric': 1150, 'Byte': 790, 'Kanji': 486},
                             (32, 'L'): {'Numeric': 4686, 'Alphanumeric': 2840, 'Byte': 1952, 'Kanji': 1201}, (32, 'M'): {'Numeric': 3693, 'Alphanumeric': 2238, 'Byte': 1538, 'Kanji': 947}, (32, 'Q'): {'Numeric': 2670, 'Alphanumeric': 1618, 'Byte': 1112, 'Kanji': 684}, (32, 'H'): {'Numeric': 2022, 'Alphanumeric': 1226, 'Byte': 842, 'Kanji': 518},
                             (33, 'L'): {'Numeric': 4965, 'Alphanumeric': 3009, 'Byte': 2068, 'Kanji': 1273}, (33, 'M'): {'Numeric': 3909, 'Alphanumeric': 2369, 'Byte': 1628, 'Kanji': 1002}, (33, 'Q'): {'Numeric': 2805, 'Alphanumeric': 1700, 'Byte': 1168, 'Kanji': 719}, (33, 'H'): {'Numeric': 2157, 'Alphanumeric': 1307, 'Byte': 898, 'Kanji': 553},
                             (34, 'L'): {'Numeric': 5253, 'Alphanumeric': 3183, 'Byte': 2188, 'Kanji': 1347}, (34, 'M'): {'Numeric': 4134, 'Alphanumeric': 2506, 'Byte': 1722, 'Kanji': 1060}, (34, 'Q'): {'Numeric': 2949, 'Alphanumeric': 1787, 'Byte': 1228, 'Kanji': 756}, (34, 'H'): {'Numeric': 2301, 'Alphanumeric': 1394, 'Byte': 958, 'Kanji': 590},
                             (35, 'L'): {'Numeric': 5529, 'Alphanumeric': 3351, 'Byte': 2303, 'Kanji': 1417}, (35, 'M'): {'Numeric': 4343, 'Alphanumeric': 2632, 'Byte': 1809, 'Kanji': 1113}, (35, 'Q'): {'Numeric': 3081, 'Alphanumeric': 1867, 'Byte': 1283, 'Kanji': 790}, (35, 'H'): {'Numeric': 2361, 'Alphanumeric': 1431, 'Byte': 983, 'Kanji': 605},
                             (36, 'L'): {'Numeric': 5836, 'Alphanumeric': 3537, 'Byte': 2431, 'Kanji': 1496}, (36, 'M'): {'Numeric': 4588, 'Alphanumeric': 2780, 'Byte': 1911, 'Kanji': 1176}, (36, 'Q'): {'Numeric': 3244, 'Alphanumeric': 1966, 'Byte': 1351, 'Kanji': 832}, (36, 'H'): {'Numeric': 2524, 'Alphanumeric': 1530, 'Byte': 1051, 'Kanji': 647},
                             (37, 'L'): {'Numeric': 6153, 'Alphanumeric': 3729, 'Byte': 2563, 'Kanji': 1577}, (37, 'M'): {'Numeric': 4775, 'Alphanumeric': 2894, 'Byte': 1989, 'Kanji': 1224}, (37, 'Q'): {'Numeric': 3417, 'Alphanumeric': 2071, 'Byte': 1423, 'Kanji': 876}, (37, 'H'): {'Numeric': 2625, 'Alphanumeric': 1591, 'Byte': 1093, 'Kanji': 673},
                             (38, 'L'): {'Numeric': 6479, 'Alphanumeric': 3927, 'Byte': 2699, 'Kanji': 1661}, (38, 'M'): {'Numeric': 5039, 'Alphanumeric': 3054, 'Byte': 2099, 'Kanji': 1292}, (38, 'Q'): {'Numeric': 3599, 'Alphanumeric': 2181, 'Byte': 1499, 'Kanji': 923}, (38, 'H'): {'Numeric': 2735, 'Alphanumeric': 1658, 'Byte': 1139, 'Kanji': 701},
                             (39, 'L'): {'Numeric': 6743, 'Alphanumeric': 4087, 'Byte': 2809, 'Kanji': 1729}, (39, 'M'): {'Numeric': 5313, 'Alphanumeric': 3220, 'Byte': 2213, 'Kanji': 1362}, (39, 'Q'): {'Numeric': 3791, 'Alphanumeric': 2298, 'Byte': 1579, 'Kanji': 972}, (39, 'H'): {'Numeric': 2927, 'Alphanumeric': 1774, 'Byte': 1219, 'Kanji': 750},
                             (40, 'L'): {'Numeric': 7089, 'Alphanumeric': 4296, 'Byte': 2953, 'Kanji': 1817}, (40, 'M'): {'Numeric': 5596, 'Alphanumeric': 3391, 'Byte': 2331, 'Kanji': 1435}, (40, 'Q'): {'Numeric': 3993, 'Alphanumeric': 2420, 'Byte': 1663, 'Kanji': 1024}, (40, 'H'): {'Numeric': 3057, 'Alphanumeric': 1852, 'Byte': 1273, 'Kanji': 784}}
CHAR_CNT_IND            = [None,
                       {'Numeric': 10, 'Alphanumeric':  9, 'Byte':  8, 'Kanji':  8},{'Numeric': 10, 'Alphanumeric':  9, 'Byte':  8, 'Kanji':  8},
                       {'Numeric': 10, 'Alphanumeric':  9, 'Byte':  8, 'Kanji':  8},{'Numeric': 10, 'Alphanumeric':  9, 'Byte':  8, 'Kanji':  8},
                       {'Numeric': 10, 'Alphanumeric':  9, 'Byte':  8, 'Kanji':  8},{'Numeric': 10, 'Alphanumeric':  9, 'Byte':  8, 'Kanji':  8},
                       {'Numeric': 10, 'Alphanumeric':  9, 'Byte':  8, 'Kanji':  8},{'Numeric': 10, 'Alphanumeric':  9, 'Byte':  8, 'Kanji':  8},
                       {'Numeric': 10, 'Alphanumeric':  9, 'Byte':  8, 'Kanji':  8},

                       {'Numeric': 12, 'Alphanumeric': 11, 'Byte': 16, 'Kanji': 10},{'Numeric': 12, 'Alphanumeric': 11, 'Byte': 16, 'Kanji': 10},
                       {'Numeric': 12, 'Alphanumeric': 11, 'Byte': 16, 'Kanji': 10},{'Numeric': 12, 'Alphanumeric': 11, 'Byte': 16, 'Kanji': 10},
                       {'Numeric': 12, 'Alphanumeric': 11, 'Byte': 16, 'Kanji': 10},{'Numeric': 12, 'Alphanumeric': 11, 'Byte': 16, 'Kanji': 10},
                       {'Numeric': 12, 'Alphanumeric': 11, 'Byte': 16, 'Kanji': 10},{'Numeric': 12, 'Alphanumeric': 11, 'Byte': 16, 'Kanji': 10},
                       {'Numeric': 12, 'Alphanumeric': 11, 'Byte': 16, 'Kanji': 10},{'Numeric': 12, 'Alphanumeric': 11, 'Byte': 16, 'Kanji': 10},
                       {'Numeric': 12, 'Alphanumeric': 11, 'Byte': 16, 'Kanji': 10},{'Numeric': 12, 'Alphanumeric': 11, 'Byte': 16, 'Kanji': 10},
                       {'Numeric': 12, 'Alphanumeric': 11, 'Byte': 16, 'Kanji': 10},{'Numeric': 12, 'Alphanumeric': 11, 'Byte': 16, 'Kanji': 10},
                       {'Numeric': 12, 'Alphanumeric': 11, 'Byte': 16, 'Kanji': 10},{'Numeric': 12, 'Alphanumeric': 11, 'Byte': 16, 'Kanji': 10},
                       {'Numeric': 12, 'Alphanumeric': 11, 'Byte': 16, 'Kanji': 10},

                       {'Numeric': 14, 'Alphanumeric': 13, 'Byte': 16, 'Kanji': 12},{'Numeric': 14, 'Alphanumeric': 13, 'Byte': 16, 'Kanji': 12},
                       {'Numeric': 14, 'Alphanumeric': 13, 'Byte': 16, 'Kanji': 12},{'Numeric': 14, 'Alphanumeric': 13, 'Byte': 16, 'Kanji': 12},
                       {'Numeric': 14, 'Alphanumeric': 13, 'Byte': 16, 'Kanji': 12},{'Numeric': 14, 'Alphanumeric': 13, 'Byte': 16, 'Kanji': 12},
                       {'Numeric': 14, 'Alphanumeric': 13, 'Byte': 16, 'Kanji': 12},{'Numeric': 14, 'Alphanumeric': 13, 'Byte': 16, 'Kanji': 12},
                       {'Numeric': 14, 'Alphanumeric': 13, 'Byte': 16, 'Kanji': 12},{'Numeric': 14, 'Alphanumeric': 13, 'Byte': 16, 'Kanji': 12},
                       {'Numeric': 14, 'Alphanumeric': 13, 'Byte': 16, 'Kanji': 12},{'Numeric': 14, 'Alphanumeric': 13, 'Byte': 16, 'Kanji': 12},
                       {'Numeric': 14, 'Alphanumeric': 13, 'Byte': 16, 'Kanji': 12},{'Numeric': 14, 'Alphanumeric': 13, 'Byte': 16, 'Kanji': 12},
                       {'Numeric': 14, 'Alphanumeric': 13, 'Byte': 16, 'Kanji': 12}, ]
TOTAL_CODEWORDS         = { ( 1, 'L'): {'TotalData':   19, 'ECPerBlock':   7, 'BlocksGroup1':   1, 'DataGroup1':   19, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        ( 1, 'M'): {'TotalData':   16, 'ECPerBlock':  10, 'BlocksGroup1':   1, 'DataGroup1':   16, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        ( 1, 'Q'): {'TotalData':   13, 'ECPerBlock':  13, 'BlocksGroup1':   1, 'DataGroup1':   13, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        ( 1, 'H'): {'TotalData':    9, 'ECPerBlock':  17, 'BlocksGroup1':   1, 'DataGroup1':    9, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        ( 2, 'L'): {'TotalData':   34, 'ECPerBlock':  10, 'BlocksGroup1':   1, 'DataGroup1':   34, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        ( 2, 'M'): {'TotalData':   28, 'ECPerBlock':  16, 'BlocksGroup1':   1, 'DataGroup1':   28, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        ( 2, 'Q'): {'TotalData':   22, 'ECPerBlock':  22, 'BlocksGroup1':   1, 'DataGroup1':   22, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        ( 2, 'H'): {'TotalData':   16, 'ECPerBlock':  28, 'BlocksGroup1':   1, 'DataGroup1':   16, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        ( 3, 'L'): {'TotalData':   55, 'ECPerBlock':  15, 'BlocksGroup1':   1, 'DataGroup1':   55, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        ( 3, 'M'): {'TotalData':   44, 'ECPerBlock':  26, 'BlocksGroup1':   1, 'DataGroup1':   44, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        ( 3, 'Q'): {'TotalData':   34, 'ECPerBlock':  18, 'BlocksGroup1':   2, 'DataGroup1':   17, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        ( 3, 'H'): {'TotalData':   26, 'ECPerBlock':  22, 'BlocksGroup1':   2, 'DataGroup1':   13, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        ( 4, 'L'): {'TotalData':   80, 'ECPerBlock':  20, 'BlocksGroup1':   1, 'DataGroup1':   80, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        ( 4, 'M'): {'TotalData':   64, 'ECPerBlock':  18, 'BlocksGroup1':   2, 'DataGroup1':   32, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        ( 4, 'Q'): {'TotalData':   48, 'ECPerBlock':  26, 'BlocksGroup1':   2, 'DataGroup1':   24, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        ( 4, 'H'): {'TotalData':   36, 'ECPerBlock':  16, 'BlocksGroup1':   4, 'DataGroup1':    9, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        ( 5, 'L'): {'TotalData':  108, 'ECPerBlock':  26, 'BlocksGroup1':   1, 'DataGroup1':  108, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        ( 5, 'M'): {'TotalData':   86, 'ECPerBlock':  24, 'BlocksGroup1':   2, 'DataGroup1':   43, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        ( 5, 'Q'): {'TotalData':   62, 'ECPerBlock':  18, 'BlocksGroup1':   2, 'DataGroup1':   15, 'BlocksGroup2':   2, 'DataGroup2': 16},
                        ( 5, 'H'): {'TotalData':   46, 'ECPerBlock':  22, 'BlocksGroup1':   2, 'DataGroup1':   11, 'BlocksGroup2':   2, 'DataGroup2': 12},
                        ( 6, 'L'): {'TotalData':  136, 'ECPerBlock':  18, 'BlocksGroup1':   2, 'DataGroup1':   68, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        ( 6, 'M'): {'TotalData':  108, 'ECPerBlock':  16, 'BlocksGroup1':   4, 'DataGroup1':   27, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        ( 6, 'Q'): {'TotalData':   76, 'ECPerBlock':  24, 'BlocksGroup1':   4, 'DataGroup1':   19, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        ( 6, 'H'): {'TotalData':   60, 'ECPerBlock':  28, 'BlocksGroup1':   4, 'DataGroup1':   15, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        ( 7, 'L'): {'TotalData':  156, 'ECPerBlock':  20, 'BlocksGroup1':   2, 'DataGroup1':   78, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        ( 7, 'M'): {'TotalData':  124, 'ECPerBlock':  18, 'BlocksGroup1':   4, 'DataGroup1':   31, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        ( 7, 'Q'): {'TotalData':   88, 'ECPerBlock':  18, 'BlocksGroup1':   2, 'DataGroup1':   14, 'BlocksGroup2':   4, 'DataGroup2': 15},
                        ( 7, 'H'): {'TotalData':   66, 'ECPerBlock':  26, 'BlocksGroup1':   4, 'DataGroup1':   13, 'BlocksGroup2':   1, 'DataGroup2': 14},
                        ( 8, 'L'): {'TotalData':  194, 'ECPerBlock':  24, 'BlocksGroup1':   2, 'DataGroup1':   97, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        ( 8, 'M'): {'TotalData':  154, 'ECPerBlock':  22, 'BlocksGroup1':   2, 'DataGroup1':   38, 'BlocksGroup2':   2, 'DataGroup2': 39},
                        ( 8, 'Q'): {'TotalData':  110, 'ECPerBlock':  22, 'BlocksGroup1':   4, 'DataGroup1':   18, 'BlocksGroup2':   2, 'DataGroup2': 19},
                        ( 8, 'H'): {'TotalData':   86, 'ECPerBlock':  26, 'BlocksGroup1':   4, 'DataGroup1':   14, 'BlocksGroup2':   2, 'DataGroup2': 15},
                        ( 9, 'L'): {'TotalData':  232, 'ECPerBlock':  30, 'BlocksGroup1':   2, 'DataGroup1':  116, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        ( 9, 'M'): {'TotalData':  182, 'ECPerBlock':  22, 'BlocksGroup1':   3, 'DataGroup1':   36, 'BlocksGroup2':   2, 'DataGroup2': 37},
                        ( 9, 'Q'): {'TotalData':  132, 'ECPerBlock':  20, 'BlocksGroup1':   4, 'DataGroup1':   16, 'BlocksGroup2':   4, 'DataGroup2': 17},
                        ( 9, 'H'): {'TotalData':  100, 'ECPerBlock':  24, 'BlocksGroup1':   4, 'DataGroup1':   12, 'BlocksGroup2':   4, 'DataGroup2': 13},
                        (10, 'L'): {'TotalData':  274, 'ECPerBlock':  18, 'BlocksGroup1':   2, 'DataGroup1':   68, 'BlocksGroup2':   2, 'DataGroup2': 69},
                        (10, 'M'): {'TotalData':  216, 'ECPerBlock':  26, 'BlocksGroup1':   4, 'DataGroup1':   43, 'BlocksGroup2':   1, 'DataGroup2': 44},
                        (10, 'Q'): {'TotalData':  154, 'ECPerBlock':  24, 'BlocksGroup1':   6, 'DataGroup1':   19, 'BlocksGroup2':   2, 'DataGroup2': 20},
                        (10, 'H'): {'TotalData':  122, 'ECPerBlock':  28, 'BlocksGroup1':   6, 'DataGroup1':   15, 'BlocksGroup2':   2, 'DataGroup2': 16},
                        (11, 'L'): {'TotalData':  324, 'ECPerBlock':  20, 'BlocksGroup1':   4, 'DataGroup1':   81, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        (11, 'M'): {'TotalData':  254, 'ECPerBlock':  30, 'BlocksGroup1':   1, 'DataGroup1':   50, 'BlocksGroup2':   4, 'DataGroup2': 51},
                        (11, 'Q'): {'TotalData':  180, 'ECPerBlock':  28, 'BlocksGroup1':   4, 'DataGroup1':   22, 'BlocksGroup2':   4, 'DataGroup2': 23},
                        (11, 'H'): {'TotalData':  140, 'ECPerBlock':  24, 'BlocksGroup1':   3, 'DataGroup1':   12, 'BlocksGroup2':   8, 'DataGroup2': 13},
                        (12, 'L'): {'TotalData':  370, 'ECPerBlock':  24, 'BlocksGroup1':   2, 'DataGroup1':   92, 'BlocksGroup2':   2, 'DataGroup2': 93},
                        (12, 'M'): {'TotalData':  290, 'ECPerBlock':  22, 'BlocksGroup1':   6, 'DataGroup1':   36, 'BlocksGroup2':   2, 'DataGroup2': 37},
                        (12, 'Q'): {'TotalData':  206, 'ECPerBlock':  26, 'BlocksGroup1':   4, 'DataGroup1':   20, 'BlocksGroup2':   6, 'DataGroup2': 21},
                        (12, 'H'): {'TotalData':  158, 'ECPerBlock':  28, 'BlocksGroup1':   7, 'DataGroup1':   14, 'BlocksGroup2':   4, 'DataGroup2': 15},
                        (13, 'L'): {'TotalData':  428, 'ECPerBlock':  26, 'BlocksGroup1':   4, 'DataGroup1':  107, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        (13, 'M'): {'TotalData':  334, 'ECPerBlock':  22, 'BlocksGroup1':   8, 'DataGroup1':   37, 'BlocksGroup2':   1, 'DataGroup2': 38},
                        (13, 'Q'): {'TotalData':  244, 'ECPerBlock':  24, 'BlocksGroup1':   8, 'DataGroup1':   20, 'BlocksGroup2':   4, 'DataGroup2': 21},
                        (13, 'H'): {'TotalData':  180, 'ECPerBlock':  22, 'BlocksGroup1':  12, 'DataGroup1':   11, 'BlocksGroup2':   4, 'DataGroup2': 12},
                        (14, 'L'): {'TotalData':  461, 'ECPerBlock':  30, 'BlocksGroup1':   3, 'DataGroup1':  115, 'BlocksGroup2':   1, 'DataGroup2': 116},
                        (14, 'M'): {'TotalData':  365, 'ECPerBlock':  24, 'BlocksGroup1':   4, 'DataGroup1':   40, 'BlocksGroup2':   5, 'DataGroup2': 41},
                        (14, 'Q'): {'TotalData':  261, 'ECPerBlock':  20, 'BlocksGroup1':  11, 'DataGroup1':   16, 'BlocksGroup2':   5, 'DataGroup2': 17},
                        (14, 'H'): {'TotalData':  197, 'ECPerBlock':  24, 'BlocksGroup1':  11, 'DataGroup1':   12, 'BlocksGroup2':   5, 'DataGroup2': 13},
                        (15, 'L'): {'TotalData':  523, 'ECPerBlock':  22, 'BlocksGroup1':   5, 'DataGroup1':   87, 'BlocksGroup2':   1, 'DataGroup2': 88},
                        (15, 'M'): {'TotalData':  415, 'ECPerBlock':  24, 'BlocksGroup1':   5, 'DataGroup1':   41, 'BlocksGroup2':   5, 'DataGroup2': 42},
                        (15, 'Q'): {'TotalData':  295, 'ECPerBlock':  30, 'BlocksGroup1':   5, 'DataGroup1':   24, 'BlocksGroup2':   7, 'DataGroup2': 25},
                        (15, 'H'): {'TotalData':  223, 'ECPerBlock':  24, 'BlocksGroup1':  11, 'DataGroup1':   12, 'BlocksGroup2':   7, 'DataGroup2': 13},
                        (16, 'L'): {'TotalData':  589, 'ECPerBlock':  24, 'BlocksGroup1':   5, 'DataGroup1':   98, 'BlocksGroup2':   1, 'DataGroup2': 99},
                        (16, 'M'): {'TotalData':  453, 'ECPerBlock':  28, 'BlocksGroup1':   7, 'DataGroup1':   45, 'BlocksGroup2':   3, 'DataGroup2': 46},
                        (16, 'Q'): {'TotalData':  325, 'ECPerBlock':  24, 'BlocksGroup1':  15, 'DataGroup1':   19, 'BlocksGroup2':   2, 'DataGroup2': 20},
                        (16, 'H'): {'TotalData':  253, 'ECPerBlock':  30, 'BlocksGroup1':   3, 'DataGroup1':   15, 'BlocksGroup2':  13, 'DataGroup2': 16},
                        (17, 'L'): {'TotalData':  647, 'ECPerBlock':  28, 'BlocksGroup1':   1, 'DataGroup1':  107, 'BlocksGroup2':   5, 'DataGroup2': 108},
                        (17, 'M'): {'TotalData':  507, 'ECPerBlock':  28, 'BlocksGroup1':  10, 'DataGroup1':   46, 'BlocksGroup2':   1, 'DataGroup2': 47},
                        (17, 'Q'): {'TotalData':  367, 'ECPerBlock':  28, 'BlocksGroup1':   1, 'DataGroup1':   22, 'BlocksGroup2':  15, 'DataGroup2': 23},
                        (17, 'H'): {'TotalData':  283, 'ECPerBlock':  28, 'BlocksGroup1':   2, 'DataGroup1':   14, 'BlocksGroup2':  17, 'DataGroup2': 15},
                        (18, 'L'): {'TotalData':  721, 'ECPerBlock':  30, 'BlocksGroup1':   5, 'DataGroup1':  120, 'BlocksGroup2':   1, 'DataGroup2': 121},
                        (18, 'M'): {'TotalData':  563, 'ECPerBlock':  26, 'BlocksGroup1':   9, 'DataGroup1':   43, 'BlocksGroup2':   4, 'DataGroup2': 44},
                        (18, 'Q'): {'TotalData':  397, 'ECPerBlock':  28, 'BlocksGroup1':  17, 'DataGroup1':   22, 'BlocksGroup2':   1, 'DataGroup2': 23},
                        (18, 'H'): {'TotalData':  313, 'ECPerBlock':  28, 'BlocksGroup1':   2, 'DataGroup1':   14, 'BlocksGroup2':  19, 'DataGroup2': 15},
                        (19, 'L'): {'TotalData':  795, 'ECPerBlock':  28, 'BlocksGroup1':   3, 'DataGroup1':  113, 'BlocksGroup2':   4, 'DataGroup2': 114},
                        (19, 'M'): {'TotalData':  627, 'ECPerBlock':  26, 'BlocksGroup1':   3, 'DataGroup1':   44, 'BlocksGroup2':  11, 'DataGroup2': 45},
                        (19, 'Q'): {'TotalData':  445, 'ECPerBlock':  26, 'BlocksGroup1':  17, 'DataGroup1':   21, 'BlocksGroup2':   4, 'DataGroup2': 22},
                        (19, 'H'): {'TotalData':  341, 'ECPerBlock':  26, 'BlocksGroup1':   9, 'DataGroup1':   13, 'BlocksGroup2':  16, 'DataGroup2': 14},
                        (20, 'L'): {'TotalData':  861, 'ECPerBlock':  28, 'BlocksGroup1':   3, 'DataGroup1':  107, 'BlocksGroup2':   5, 'DataGroup2': 108},
                        (20, 'M'): {'TotalData':  669, 'ECPerBlock':  26, 'BlocksGroup1':   3, 'DataGroup1':   41, 'BlocksGroup2':  13, 'DataGroup2': 42},
                        (20, 'Q'): {'TotalData':  485, 'ECPerBlock':  30, 'BlocksGroup1':  15, 'DataGroup1':   24, 'BlocksGroup2':   5, 'DataGroup2': 25},
                        (20, 'H'): {'TotalData':  385, 'ECPerBlock':  28, 'BlocksGroup1':  15, 'DataGroup1':   15, 'BlocksGroup2':  10, 'DataGroup2': 16},
                        (21, 'L'): {'TotalData':  932, 'ECPerBlock':  28, 'BlocksGroup1':   4, 'DataGroup1':  116, 'BlocksGroup2':   4, 'DataGroup2': 117},
                        (21, 'M'): {'TotalData':  714, 'ECPerBlock':  26, 'BlocksGroup1':  17, 'DataGroup1':   42, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        (21, 'Q'): {'TotalData':  512, 'ECPerBlock':  28, 'BlocksGroup1':  17, 'DataGroup1':   22, 'BlocksGroup2':   6, 'DataGroup2': 23},
                        (21, 'H'): {'TotalData':  406, 'ECPerBlock':  30, 'BlocksGroup1':  19, 'DataGroup1':   16, 'BlocksGroup2':   6, 'DataGroup2': 17},
                        (22, 'L'): {'TotalData': 1006, 'ECPerBlock':  28, 'BlocksGroup1':   2, 'DataGroup1':  111, 'BlocksGroup2':   7, 'DataGroup2': 112},
                        (22, 'M'): {'TotalData':  782, 'ECPerBlock':  28, 'BlocksGroup1':  17, 'DataGroup1':   46, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        (22, 'Q'): {'TotalData':  568, 'ECPerBlock':  30, 'BlocksGroup1':   7, 'DataGroup1':   24, 'BlocksGroup2':  16, 'DataGroup2': 25},
                        (22, 'H'): {'TotalData':  442, 'ECPerBlock':  24, 'BlocksGroup1':  34, 'DataGroup1':   13, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        (23, 'L'): {'TotalData': 1094, 'ECPerBlock':  30, 'BlocksGroup1':   4, 'DataGroup1':  121, 'BlocksGroup2':   5, 'DataGroup2': 122},
                        (23, 'M'): {'TotalData':  860, 'ECPerBlock':  28, 'BlocksGroup1':   4, 'DataGroup1':   47, 'BlocksGroup2':  14, 'DataGroup2': 48},
                        (23, 'Q'): {'TotalData':  614, 'ECPerBlock':  30, 'BlocksGroup1':  11, 'DataGroup1':   24, 'BlocksGroup2':  14, 'DataGroup2': 25},
                        (23, 'H'): {'TotalData':  464, 'ECPerBlock':  30, 'BlocksGroup1':  16, 'DataGroup1':   15, 'BlocksGroup2':  14, 'DataGroup2': 16},
                        (24, 'L'): {'TotalData': 1174, 'ECPerBlock':  30, 'BlocksGroup1':   6, 'DataGroup1':  117, 'BlocksGroup2':   4, 'DataGroup2': 118},
                        (24, 'M'): {'TotalData':  914, 'ECPerBlock':  28, 'BlocksGroup1':   6, 'DataGroup1':   45, 'BlocksGroup2':  14, 'DataGroup2': 46},
                        (24, 'Q'): {'TotalData':  664, 'ECPerBlock':  30, 'BlocksGroup1':  11, 'DataGroup1':   24, 'BlocksGroup2':  16, 'DataGroup2': 25},
                        (24, 'H'): {'TotalData':  514, 'ECPerBlock':  30, 'BlocksGroup1':  30, 'DataGroup1':   16, 'BlocksGroup2':   2, 'DataGroup2': 17},
                        (25, 'L'): {'TotalData': 1276, 'ECPerBlock':  26, 'BlocksGroup1':   8, 'DataGroup1':  106, 'BlocksGroup2':   4, 'DataGroup2': 107},
                        (25, 'M'): {'TotalData': 1000, 'ECPerBlock':  28, 'BlocksGroup1':   8, 'DataGroup1':   47, 'BlocksGroup2':  13, 'DataGroup2': 48},
                        (25, 'Q'): {'TotalData':  718, 'ECPerBlock':  30, 'BlocksGroup1':   7, 'DataGroup1':   24, 'BlocksGroup2':  22, 'DataGroup2': 25},
                        (25, 'H'): {'TotalData':  538, 'ECPerBlock':  30, 'BlocksGroup1':  22, 'DataGroup1':   15, 'BlocksGroup2':  13, 'DataGroup2': 16},
                        (26, 'L'): {'TotalData': 1370, 'ECPerBlock':  28, 'BlocksGroup1':  10, 'DataGroup1':  114, 'BlocksGroup2':   2, 'DataGroup2': 115},
                        (26, 'M'): {'TotalData': 1062, 'ECPerBlock':  28, 'BlocksGroup1':  19, 'DataGroup1':   46, 'BlocksGroup2':   4, 'DataGroup2': 47},
                        (26, 'Q'): {'TotalData':  754, 'ECPerBlock':  28, 'BlocksGroup1':  28, 'DataGroup1':   22, 'BlocksGroup2':   6, 'DataGroup2': 23},
                        (26, 'H'): {'TotalData':  596, 'ECPerBlock':  30, 'BlocksGroup1':  33, 'DataGroup1':   16, 'BlocksGroup2':   4, 'DataGroup2': 17},
                        (27, 'L'): {'TotalData': 1468, 'ECPerBlock':  30, 'BlocksGroup1':   8, 'DataGroup1':  122, 'BlocksGroup2':   4, 'DataGroup2': 123},
                        (27, 'M'): {'TotalData': 1128, 'ECPerBlock':  28, 'BlocksGroup1':  22, 'DataGroup1':   45, 'BlocksGroup2':   3, 'DataGroup2': 46},
                        (27, 'Q'): {'TotalData':  808, 'ECPerBlock':  30, 'BlocksGroup1':   8, 'DataGroup1':   23, 'BlocksGroup2':  26, 'DataGroup2': 24},
                        (27, 'H'): {'TotalData':  628, 'ECPerBlock':  30, 'BlocksGroup1':  12, 'DataGroup1':   15, 'BlocksGroup2':  28, 'DataGroup2': 16},
                        (28, 'L'): {'TotalData': 1531, 'ECPerBlock':  30, 'BlocksGroup1':   3, 'DataGroup1':  117, 'BlocksGroup2':  10, 'DataGroup2': 118},
                        (28, 'M'): {'TotalData': 1193, 'ECPerBlock':  28, 'BlocksGroup1':   3, 'DataGroup1':   45, 'BlocksGroup2':  23, 'DataGroup2': 46},
                        (28, 'Q'): {'TotalData':  871, 'ECPerBlock':  30, 'BlocksGroup1':   4, 'DataGroup1':   24, 'BlocksGroup2':  31, 'DataGroup2': 25},
                        (28, 'H'): {'TotalData':  661, 'ECPerBlock':  30, 'BlocksGroup1':  11, 'DataGroup1':   15, 'BlocksGroup2':  31, 'DataGroup2': 16},
                        (29, 'L'): {'TotalData': 1631, 'ECPerBlock':  30, 'BlocksGroup1':   7, 'DataGroup1':  116, 'BlocksGroup2':   7, 'DataGroup2': 117},
                        (29, 'M'): {'TotalData': 1267, 'ECPerBlock':  28, 'BlocksGroup1':  21, 'DataGroup1':   45, 'BlocksGroup2':   7, 'DataGroup2': 46},
                        (29, 'Q'): {'TotalData':  911, 'ECPerBlock':  30, 'BlocksGroup1':   1, 'DataGroup1':   23, 'BlocksGroup2':  37, 'DataGroup2': 24},
                        (29, 'H'): {'TotalData':  701, 'ECPerBlock':  30, 'BlocksGroup1':  19, 'DataGroup1':   15, 'BlocksGroup2':  26, 'DataGroup2': 16},
                        (30, 'L'): {'TotalData': 1735, 'ECPerBlock':  30, 'BlocksGroup1':   5, 'DataGroup1':  115, 'BlocksGroup2':  10, 'DataGroup2': 116},
                        (30, 'M'): {'TotalData': 1373, 'ECPerBlock':  28, 'BlocksGroup1':  19, 'DataGroup1':   47, 'BlocksGroup2':  10, 'DataGroup2': 48},
                        (30, 'Q'): {'TotalData':  985, 'ECPerBlock':  30, 'BlocksGroup1':  15, 'DataGroup1':   24, 'BlocksGroup2':  25, 'DataGroup2': 25},
                        (30, 'H'): {'TotalData':  745, 'ECPerBlock':  30, 'BlocksGroup1':  23, 'DataGroup1':   15, 'BlocksGroup2':  25, 'DataGroup2': 16},
                        (31, 'L'): {'TotalData': 1843, 'ECPerBlock':  30, 'BlocksGroup1':  13, 'DataGroup1':  115, 'BlocksGroup2':   3, 'DataGroup2': 116},
                        (31, 'M'): {'TotalData': 1455, 'ECPerBlock':  28, 'BlocksGroup1':   2, 'DataGroup1':   46, 'BlocksGroup2':  29, 'DataGroup2': 47},
                        (31, 'Q'): {'TotalData': 1033, 'ECPerBlock':  30, 'BlocksGroup1':  42, 'DataGroup1':   24, 'BlocksGroup2':   1, 'DataGroup2': 25},
                        (31, 'H'): {'TotalData':  793, 'ECPerBlock':  30, 'BlocksGroup1':  23, 'DataGroup1':   15, 'BlocksGroup2':  28, 'DataGroup2': 16},
                        (32, 'L'): {'TotalData': 1955, 'ECPerBlock':  30, 'BlocksGroup1':  17, 'DataGroup1':  115, 'BlocksGroup2':   0, 'DataGroup2': 0},
                        (32, 'M'): {'TotalData': 1541, 'ECPerBlock':  28, 'BlocksGroup1':  10, 'DataGroup1':   46, 'BlocksGroup2':  23, 'DataGroup2': 47},
                        (32, 'Q'): {'TotalData': 1115, 'ECPerBlock':  30, 'BlocksGroup1':  10, 'DataGroup1':   24, 'BlocksGroup2':  35, 'DataGroup2': 25},
                        (32, 'H'): {'TotalData':  845, 'ECPerBlock':  30, 'BlocksGroup1':  19, 'DataGroup1':   15, 'BlocksGroup2':  35, 'DataGroup2': 16},
                        (33, 'L'): {'TotalData': 2071, 'ECPerBlock':  30, 'BlocksGroup1':  17, 'DataGroup1':  115, 'BlocksGroup2':   1, 'DataGroup2': 116},
                        (33, 'M'): {'TotalData': 1631, 'ECPerBlock':  28, 'BlocksGroup1':  14, 'DataGroup1':   46, 'BlocksGroup2':  21, 'DataGroup2': 47},
                        (33, 'Q'): {'TotalData': 1171, 'ECPerBlock':  30, 'BlocksGroup1':  29, 'DataGroup1':   24, 'BlocksGroup2':  19, 'DataGroup2': 25},
                        (33, 'H'): {'TotalData':  901, 'ECPerBlock':  30, 'BlocksGroup1':  11, 'DataGroup1':   15, 'BlocksGroup2':  46, 'DataGroup2': 16},
                        (34, 'L'): {'TotalData': 2191, 'ECPerBlock':  30, 'BlocksGroup1':  13, 'DataGroup1':  115, 'BlocksGroup2':   6, 'DataGroup2': 116},
                        (34, 'M'): {'TotalData': 1725, 'ECPerBlock':  28, 'BlocksGroup1':  14, 'DataGroup1':   46, 'BlocksGroup2':  23, 'DataGroup2': 47},
                        (34, 'Q'): {'TotalData': 1231, 'ECPerBlock':  30, 'BlocksGroup1':  44, 'DataGroup1':   24, 'BlocksGroup2':   7, 'DataGroup2': 25},
                        (34, 'H'): {'TotalData':  961, 'ECPerBlock':  30, 'BlocksGroup1':  59, 'DataGroup1':   16, 'BlocksGroup2':   1, 'DataGroup2': 17},
                        (35, 'L'): {'TotalData': 2306, 'ECPerBlock':  30, 'BlocksGroup1':  12, 'DataGroup1':  121, 'BlocksGroup2':   7, 'DataGroup2': 122},
                        (35, 'M'): {'TotalData': 1812, 'ECPerBlock':  28, 'BlocksGroup1':  12, 'DataGroup1':   47, 'BlocksGroup2':  26, 'DataGroup2': 48},
                        (35, 'Q'): {'TotalData': 1286, 'ECPerBlock':  30, 'BlocksGroup1':  39, 'DataGroup1':   24, 'BlocksGroup2':  14, 'DataGroup2': 25},
                        (35, 'H'): {'TotalData':  986, 'ECPerBlock':  30, 'BlocksGroup1':  22, 'DataGroup1':   15, 'BlocksGroup2':  41, 'DataGroup2': 16},
                        (36, 'L'): {'TotalData': 2434, 'ECPerBlock':  30, 'BlocksGroup1':   6, 'DataGroup1':  121, 'BlocksGroup2':  14, 'DataGroup2': 122},
                        (36, 'M'): {'TotalData': 1914, 'ECPerBlock':  28, 'BlocksGroup1':   6, 'DataGroup1':   47, 'BlocksGroup2':  34, 'DataGroup2': 48},
                        (36, 'Q'): {'TotalData': 1354, 'ECPerBlock':  30, 'BlocksGroup1':  46, 'DataGroup1':   24, 'BlocksGroup2':  10, 'DataGroup2': 25},
                        (36, 'H'): {'TotalData': 1054, 'ECPerBlock':  30, 'BlocksGroup1':   2, 'DataGroup1':   15, 'BlocksGroup2':  64, 'DataGroup2': 16},
                        (37, 'L'): {'TotalData': 2566, 'ECPerBlock':  30, 'BlocksGroup1':  17, 'DataGroup1':  122, 'BlocksGroup2':   4, 'DataGroup2': 123},
                        (37, 'M'): {'TotalData': 1992, 'ECPerBlock':  28, 'BlocksGroup1':  29, 'DataGroup1':   46, 'BlocksGroup2':  14, 'DataGroup2': 47},
                        (37, 'Q'): {'TotalData': 1426, 'ECPerBlock':  30, 'BlocksGroup1':  49, 'DataGroup1':   24, 'BlocksGroup2':  10, 'DataGroup2': 25},
                        (37, 'H'): {'TotalData': 1096, 'ECPerBlock':  30, 'BlocksGroup1':  24, 'DataGroup1':   15, 'BlocksGroup2':  46, 'DataGroup2': 16},
                        (38, 'L'): {'TotalData': 2702, 'ECPerBlock':  30, 'BlocksGroup1':   4, 'DataGroup1':  122, 'BlocksGroup2':  18, 'DataGroup2': 123},
                        (38, 'M'): {'TotalData': 2102, 'ECPerBlock':  28, 'BlocksGroup1':  13, 'DataGroup1':   46, 'BlocksGroup2':  32, 'DataGroup2': 47},
                        (38, 'Q'): {'TotalData': 1502, 'ECPerBlock':  30, 'BlocksGroup1':  48, 'DataGroup1':   24, 'BlocksGroup2':  14, 'DataGroup2': 25},
                        (38, 'H'): {'TotalData': 1142, 'ECPerBlock':  30, 'BlocksGroup1':  42, 'DataGroup1':   15, 'BlocksGroup2':  32, 'DataGroup2': 16},
                        (39, 'L'): {'TotalData': 2812, 'ECPerBlock':  30, 'BlocksGroup1':  20, 'DataGroup1':  117, 'BlocksGroup2':   4, 'DataGroup2': 118},
                        (39, 'M'): {'TotalData': 2216, 'ECPerBlock':  28, 'BlocksGroup1':  40, 'DataGroup1':   47, 'BlocksGroup2':   7, 'DataGroup2': 48},
                        (39, 'Q'): {'TotalData': 1582, 'ECPerBlock':  30, 'BlocksGroup1':  43, 'DataGroup1':   24, 'BlocksGroup2':  22, 'DataGroup2': 25},
                        (39, 'H'): {'TotalData': 1222, 'ECPerBlock':  30, 'BlocksGroup1':  10, 'DataGroup1':   15, 'BlocksGroup2':  67, 'DataGroup2': 16},
                        (40, 'L'): {'TotalData': 2956, 'ECPerBlock':  30, 'BlocksGroup1':  19, 'DataGroup1':  118, 'BlocksGroup2':   6, 'DataGroup2': 119},
                        (40, 'M'): {'TotalData': 2334, 'ECPerBlock':  28, 'BlocksGroup1':  18, 'DataGroup1':   47, 'BlocksGroup2':  31, 'DataGroup2': 48},
                        (40, 'Q'): {'TotalData': 1666, 'ECPerBlock':  30, 'BlocksGroup1':  34, 'DataGroup1':   24, 'BlocksGroup2':  34, 'DataGroup2': 25},
                        (40, 'H'): {'TotalData': 1276, 'ECPerBlock':  30, 'BlocksGroup1':  20, 'DataGroup1':   15, 'BlocksGroup2':  61, 'DataGroup2': 16}}
LOG_VALUES              = [   1,   2,   4,   8,  16,  32,  64, 128,  29,  58, 116, 232, 205, 135,  19,  38,  76, 152,  45,  90,
                        180, 117, 234, 201, 143,  3,    6,  12,  24,  48,  96, 192, 157,  39,  78, 156,  37,  74, 148,  53,
                        106, 212, 181, 119, 238, 193, 159,  35,  70, 140,   5,  10,  20,  40,  80, 160,  93, 186, 105, 210,
                        185, 111, 222, 161,  95, 190,  97, 194, 153,  47,  94, 188, 101, 202, 137,  15,  30,  60, 120, 240,
                        253, 231, 211, 187, 107, 214, 177, 127, 254, 225, 223, 163,  91, 182, 113, 226, 217, 175,  67, 134,
                         17,  34,  68, 136,  13,  26,  52, 104, 208, 189, 103, 206, 129,  31,  62, 124, 248, 237, 199, 147,
                         59, 118, 236, 197, 151,  51, 102, 204, 133,  23,  46,  92, 184, 109, 218, 169,  79, 158,  33,  66,
                        132,  21,  42,  84, 168,  77, 154,  41,  82, 164,  85, 170,  73, 146,  57, 114, 228, 213, 183, 115,
                        230, 209, 191,  99, 198, 145,  63, 126, 252, 229, 215, 179, 123, 246, 241, 255, 227, 219, 171,  75,
                        150,  49,  98, 196, 149,  55, 110, 220, 165,  87, 174,  65, 130,  25,  50, 100, 200, 141,   7,  14,
                         28,  56, 112, 224, 221, 167,  83, 166,  81, 162,  89, 178, 121, 242, 249, 239, 195, 155,  43,  86,
                        172,  69, 138,   9,  18,  36,  72, 144,  61, 122, 244, 245, 247, 243, 251, 235, 203, 139,  11,  22,
                         44,  88, 176, 125, 250, 233, 207, 131,  27,  54, 108, 216, 173,  71, 142, 1,]    # Alpha to Number
LOG_ANTIVALUES          = [None,
                      0,   1,  25,   2,  50,  26, 198,   3, 223,  51, 238,  27, 104, 199,  75,   4, 100, 224,  14,  52,
                    141, 239, 129,  28, 193, 105, 248, 200,   8,  76, 113,   5, 138, 101,  47, 225,  36,  15,  33,  53,
                    147, 142, 218, 240,  18, 130,  69,  29, 181, 194, 125, 106,  39, 249, 185, 201, 154,   9, 120,  77,
                    228, 114, 166,   6, 191, 139,  98, 102, 221,  48, 253, 226, 152,  37, 179,  16, 145,  34, 136,  54,
                    208, 148, 206, 143, 150, 219, 189, 241, 210,  19,  92, 131,  56,  70,  64,  30,  66, 182, 163, 195,
                     72, 126, 110, 107,  58,  40,  84, 250, 133, 186,  61, 202,  94, 155, 159,  10,  21, 121,  43,  78,
                    212, 229, 172, 115, 243, 167,  87,   7, 112, 192, 247, 140, 128,  99,  13, 103,  74, 222, 237,  49,
                    197, 254,  24, 227, 165, 153, 119,  38, 184, 180, 124,  17,  68, 146, 217,  35,  32, 137,  46,  55,
                     63, 209,  91, 149, 188, 207, 205, 144, 135, 151, 178, 220, 252, 190,  97, 242,  86, 211, 171,  20,
                     42,  93, 158, 132,  60,  57,  83,  71, 109,  65, 162,  31,  45,  67, 216, 183, 123, 164, 118, 196,
                     23,  73, 236, 127,  12, 111, 246, 108, 161,  59,  82,  41, 157,  85, 170, 251,  96, 134, 177, 187,
                    204,  62,  90, 203,  89,  95, 176, 156, 169, 160,  81,  11, 245,  22, 235, 122, 117,  44, 215,  79,
                    174, 213, 233, 230, 231, 173, 232, 116, 214, 244, 234, 168,  80,  88, 175,]    # Number to Alpha
GENERATORS_POLYS        = [None,None,None,None,None,None,None,
                        [0, 87, 229, 146, 149, 238, 102, 21],
                        [0, 175, 238, 208, 249, 215, 252, 196, 28],
                        [0, 95, 246, 137, 231, 235, 149, 11, 123, 36],
                        [0, 251, 67, 46, 61, 118, 70, 64, 94, 32, 45],
                        [0, 220, 192, 91, 194, 172, 177, 209, 116, 227, 10, 55],
                        [0, 102, 43, 98, 121, 187, 113, 198, 143, 131, 87, 157, 66],
                        [0, 74, 152, 176, 100, 86, 100, 106, 104, 130, 218, 206, 140, 78],
                        [0, 199, 249, 155, 48, 190, 124, 218, 137, 216, 87, 207, 59, 22, 91],
                        [0, 8, 183, 61, 91, 202, 37, 51, 58, 58, 237, 140, 124, 5, 99, 105],
                        [0, 120, 104, 107, 109, 102, 161, 76, 3, 91, 191, 147, 169, 182, 194, 225, 120],
                        [0, 43, 139, 206, 78, 43, 239, 123, 206, 214, 147, 24, 99, 150, 39, 243, 163, 136],
                        [0, 215, 234, 158, 94, 184, 97, 118, 170, 79, 187, 152, 148, 252, 179, 5, 98, 96, 153],
                        [0, 67, 3, 105, 153, 52, 90, 83, 17, 150, 159, 44, 128, 153, 133, 252, 222, 138, 220, 171],
                        [0, 17, 60, 79, 50, 61, 163, 26, 187, 202, 180, 221, 225, 83, 239, 156, 164, 212, 212, 188, 190],
                        [0, 240, 233, 104, 247, 181, 140, 67, 98, 85, 200, 210, 115, 148, 137, 230, 36, 122, 254, 148, 175, 210],
                        [0, 210, 171, 247, 242, 93, 230, 14, 109, 221, 53, 200, 74, 8, 172, 98, 80, 219, 134, 160, 105, 165, 231],
                        [0, 171, 102, 146, 91, 49, 103, 65, 17, 193, 150, 14, 25, 183, 248, 94, 164, 224, 192, 0, 78, 56, 147, 253],
                        [0, 229, 121, 135, 48, 211, 117, 251, 126, 159, 180, 169, 152, 192, 226, 228, 218, 111, 0, 117, 232, 87, 96, 227, 21],
                        [0, 231, 181, 156, 39, 170, 26, 12, 59, 15, 148, 201, 54, 66, 237, 208, 99, 167, 144, 182, 95, 243, 129, 178, 252, 45],
                        [0, 173, 125, 158, 2, 103, 182, 118, 17, 145, 201, 111, 28, 165, 53, 161, 21, 245, 142, 13, 102, 48, 227, 153, 145, 218, 70],
                        [0, 79, 228, 8, 165, 227, 21, 180, 29, 9, 237, 70, 99, 45, 58, 138, 135, 73, 126, 172, 94, 216, 193, 157, 26, 17, 149, 96],
                        [0, 168, 223, 200, 104, 224, 234, 108, 180, 110, 190, 195, 147, 205, 27, 232, 201, 21, 43, 245, 87, 42, 195, 212, 119, 242, 37, 9, 123],
                        [0, 156, 45, 183, 29, 151, 219, 54, 96, 249, 24, 136, 5, 241, 175, 189, 28, 75, 234, 150, 148, 23, 9, 202, 162, 68, 250, 140, 24, 151],
                        [0, 41, 173, 145, 152, 216, 31, 179, 182, 50, 48, 110, 86, 239, 96, 222, 125, 42, 173, 226, 193, 224, 130, 156, 37, 251, 216, 238, 40, 192, 180],]    # We should have calculated it programmatically... haha --> https://www.thonky.com/qr-code-tutorial/generator-polynomial-tool
REQUIRED_REMAINDER_BITS = [None,
                           0,
                           7,7,7,7,7,
                           0,0,0,0,0,0,0,
                           3,3,3,3,3,3,3,
                           4,4,4,4,4,4,4,
                           3,3,3,3,3,3,3,
                           0,0,0,0,0,0,]
FIND_PATTERN            = [  [1,1,1,1,1,1,1,],
                         [1,0,0,0,0,0,1,],
                         [1,0,1,1,1,0,1,],
                         [1,0,1,1,1,0,1,],
                         [1,0,1,1,1,0,1,],
                         [1,0,0,0,0,0,1,],
                         [1,1,1,1,1,1,1,], ]
ALIGNMENT_PATTERN       = [   [1,1,1,1,1,],
                          [1,0,0,0,1,],
                          [1,0,1,0,1,],
                          [1,0,0,0,1,],
                          [1,1,1,1,1,], ]
ALIGNMENT_PATTERN_POS   = [None,
                         None,
                         [6, 18], [6, 22], [6, 26], [6, 30], [6, 34],
                         [6, 22, 38], [6, 24, 42], [6, 26, 46], [6, 28, 50], [6, 30, 54], [6, 32, 58], [6, 34, 62],
                         [6, 26, 46, 66], [6, 26, 48, 70], [6, 26, 50, 74], [6, 30, 54, 78], [6, 30, 56, 82], [6, 30, 58, 86], [6, 34, 62, 90],
                         [6, 28, 50, 72, 94], [6, 26, 50, 74, 98], [6, 30, 54, 78, 102], [6, 28, 54, 80, 106], [6, 32, 58, 84, 110],
                         [6, 30, 58, 86, 114], [6, 34, 62, 90, 118], [6, 26, 50, 74, 98, 122], [6, 30, 54, 78, 102, 126], [6, 26, 52, 78, 104, 130],
                         [6, 30, 56, 82, 108, 134], [6, 34, 60, 86, 112, 138], [6, 30, 58, 86, 114, 142], [6, 34, 62, 90, 118, 146],
                         [6, 30, 54, 78, 102, 126, 150], [6, 24, 50, 76, 102, 128, 154], [6, 28, 54, 80, 106, 132, 158],
                         [6, 32, 58, 84, 110, 136, 162], [6, 26, 54, 82, 110, 138, 166], [6, 30, 58, 86, 114, 142, 170]]
MASK_PATTERNS           = ['(i + j) % 2',
                       'i % 2',
                       'j % 3',
                       '(i + j) % 3',
                       '( floor(i/2) + floor(j/3)) % 2',
                       '(i*j)%2 + (i*j)%3',
                       '((i*j)%3 + i * j) % 2',
                       '((i*j)%3 + i + j) % 2']
ERROR_CORRECTION_BITS   = {'L':	'01',
                           'M': '00',
                           'Q': '11',
                           'H': '10',}
FORMAT_STRINGS          = { ("L",0): "111011111000100",
                            ("L",1): "111001011110011",
                            ("L",2): "111110110101010",
                            ("L",3): "111100010011101",
                            ("L",4): "110011000101111",
                            ("L",5): "110001100011000",
                            ("L",6): "110110001000001",
                            ("L",7): "110100101110110",
                            ("M",0): "101010000010010",
                            ("M",1): "101000100100101",
                            ("M",2): "101111001111100",
                            ("M",3): "101101101001011",
                            ("M",4): "100010111111001",
                            ("M",5): "100000011001110",
                            ("M",6): "100111110010111",
                            ("M",7): "100101010100000",
                            ("Q",0): "011010101011111",
                            ("Q",1): "011000001101000",
                            ("Q",2): "011111100110001",
                            ("Q",3): "011101000000110",
                            ("Q",4): "010010010110100",
                            ("Q",5): "010000110000011",
                            ("Q",6): "010111011011010",
                            ("Q",7): "010101111101101",
                            ("H",0): "001011010001001",
                            ("H",1): "001001110111110",
                            ("H",2): "001110011100111",
                            ("H",3): "001100111010000",
                            ("H",4): "000011101100010",
                            ("H",5): "000001001010101",
                            ("H",6): "000110100001100",
                            ("H",7): "000100000111011",}
VERSION_STRINGS         = [ None,None,None,None,None,None,None,
                            "000111110010010100",
                            "001000010110111100",
                            "001001101010011001",
                            "001010010011010011",
                            "001011101111110110",
                            "001100011101100010",
                            "001101100001000111",
                            "001110011000001101",
                            "001111100100101000",
                            "010000101101111000",
                            "010001010001011101",
                            "010010101000010111",
                            "010011010100110010",
                            "010100100110100110",
                            "010101011010000011",
                            "010110100011001001",
                            "010111011111101100",
                            "011000111011000100",
                            "011001000111100001",
                            "011010111110101011",
                            "011011000010001110",
                            "011100110000011010",
                            "011101001100111111",
                            "011110110101110101",
                            "011111001001010000",
                            "100000100111010101",
                            "100001011011110000",
                            "100010100010111010",
                            "100011011110011111",
                            "100100101100001011",
                            "100101010000101110",
                            "100110101001100100",
                            "100111010101000001",
                            "101000110001101001",]
QUIT_ZONE_SIZE          = 4         # "Please note that the QR code specification requires that the QR matrix be surrounded by a quiet zone: a 4-module-wide area of light modules."

# ========== CLASSES ===================================================================================================
class QrCode():
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, string_input, version = 1, error_corretion_level = 'L', print_steps = False):
        self.string_input   = string_input              # User's message
        self.msg_len        = len(self.string_input)    #
        self.version        = version                   #
        self.er_cor_level   = error_corretion_level     # L = 7%, M = 15%, Q = 25% or H = 30%

        self.mode           = None                      # Numeric, Alphanumeric, Bytes, ...
        self.data_string    = None                      # Mode Indicator (0000) + Character Count Indicator + Encoded Data
        self.final_msg      = None                      # Interleaved Data Codewords + Interleaved Error Correction CodeWords
        self.mask           = None                      # Best mask (000)

        self.data_codewords = None                      # Data String Split into Codewords ( 8 characteres of 0s and 1s )
        self.ec_codewords   = None                      # Error Correction Codewords

        self.size           = None                      # Version 1: 21x21, Version 2: 25x25, ...
        self.matrix         = None                      # QR Code it self

        self.format_string  = None                      # Mode + Mask + EC
        self.version_string = None                      # 18 bit long string

        self.print_steps    = print_steps
        self.generate()

    # ------------------------------------------------------------------------------------------------------------------
    def generate(self):
        self._dataAnalysis()
        self._dataEnconding()
        self._errorCorrectionCoding()
        self._structureFinalMessage()
        self._modulePlacementMatrix()
        self._dataMasking()
        self._formatAndVersionInformation()

        # QuitZone:
        n           = QUIT_ZONE_SIZE
        self.matrix = [ ["0" if col < n/2 or row < n/2 or col >= self.size+n/2 or row >= self.size+n/2 else self.matrix[row-int(n/2)][col-int(n/2)] for col in range(self.size + n)] for row in range(self.size + n)]
        self.size   = len(self.matrix) # TODO: Should We Change it Now ?

        if self.print_steps:
            print(f'Input: |{self.string_input}|\n'
                  f'Version String: {self.version_string}\n'
                  f'Format String: {self.format_string}\n')

    # ------------------------------------------------------------------------------------------------------------------
    def print(self, cnvToHashtag = False):
        n = 3
        print('\n' + "="*self.size * n)
        for rows in self.matrix:
            for value in rows:
                if cnvToHashtag:
                    value = '#' if value == '1' else ''
                #print( f"|{value:^{n}}", end = '' )
                print(f"{value:^{n}}", end='')
            #print("|")
            print("")
        print("=" * self.size * n + '\n')

    # ------------------------------------------------------------------------------------------------------------------
    def getQRCodeMatrix(self):
        aux     = deepcopy(self.matrix)
        result  = [ [255 if value == "0" else 0 for value in rows ] for rows in aux ]

        return result

    # ------------------------------------------------------------------------------------------------------------------
    def show(self):
        import matplotlib.pyplot as plt
        import numpy as np

        npa = np.asarray(self.getQRCodeMatrix())

        plt.suptitle(self.string_input)
        plt.title(f'{self.version}-{self.er_cor_level}')
        plt.imshow(npa, cmap="gray")
        plt.show()

    # ------------------------------------------------------------------------------------------------------------------
    def bmp(self,filename,scale = 10):
        from PIL import Image
        import numpy as np

        # Convert:
        matrix_np = np.asarray( self.getQRCodeMatrix() )    # 0 becomes white (255), 1 becomes black (0) and then we convert it to an Numpy Array

        # Scaling it (how many pixels per 'module'):
        image_matrix = np.zeros( ((self.size+QUIT_ZONE_SIZE)*scale,(self.size+QUIT_ZONE_SIZE)*scale), dtype=int ) # Size + Quit Zone (4 rows, 4 cols)
        for row, rows in enumerate(matrix_np):
            for col, value in enumerate(rows):
                image_matrix[row*scale:(row+1)*scale,col*scale:(col+1)*scale] = value

        image = Image.fromarray( image_matrix )
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image.save(f"{filename}.bmp", format='BMP')

    # ------------------------------------------------------------------------------------------------------------------
    def _dataAnalysis(self,):
        """
        https://www.thonky.com/qr-code-tutorial/data-analysis
        :return:
        """
        # TODO: Kanji Mode, Extended Channel Interpretation (ECI), Structed, FNC1 and etc.
        from re import fullmatch

        #print("Executing data analysis...")
        if self.string_input.isdecimal():
            self.mode = "Numeric"
        elif fullmatch("[0-9A-Z$%*+./ \-]*",self.string_input):
            self.mode = "Alphanumeric"
        else:
            self.mode = "Byte"

        if self.print_steps:
            print("Mode: {}".format(self.mode))

    # ------------------------------------------------------------------------------------------------------------------
    def _dataEnconding(self,):
        """
        https://www.thonky.com/qr-code-tutorial/data-encoding
        :return:
        """
        # ....................................................
        def encodeNumeric():
            """
            https://www.thonky.com/qr-code-tutorial/numeric-mode-encoding
            :return:
            """
            n           = 3
            groups      = [self.string_input[i:i+n] for i in range(0, self.msg_len, n)]
            groups_bits = []
            
            #print(groups)
            for group in groups:
                aux = group.lstrip('0')
                if len(aux) == 1:   # 4 bits
                    groups_bits.append( "{:04b}".format(int(aux)) )
                elif len(aux) == 2: # 7 bits
                    groups_bits.append( "{:07b}".format(int(aux)) )
                elif len(aux) == 3: # 10 bits
                    groups_bits.append( "{:010b}".format(int(aux)) )
            #print(groups_bits)
            return groups_bits

        # ....................................................
        def encodeAlphanumeric():
            """
            https://www.thonky.com/qr-code-tutorial/alphanumeric-mode-encoding
            :return:
            """
            n           = 2
            groups      = [self.string_input[i:i+n] for i in range(0, self.msg_len, n)]
            groups_bits = []

            #print(groups)
            for group in groups:
                if len(group) == 1: # 6 bits
                    aux = ALPHANUMERIC_TABLE[group[0]]                                      # TODO: Should we multiply by 45 or not ?
                    groups_bits.append( "{:06b}".format(int(aux)) )
                else:               # 11 bits
                    aux = ALPHANUMERIC_TABLE[group[0]] * 45 + ALPHANUMERIC_TABLE[group[1]]
                    groups_bits.append( "{:011b}".format(int(aux)) )
            #print(groups_bits)
            return groups_bits

        # ....................................................
        def encodeByte():
            """
            https://www.thonky.com/qr-code-tutorial/byte-mode-encoding
            :return:
            """
            return ["{:08b}".format(ord(letra)) for letra in self.string_input]

        # ....................................................

        # Determine the Smallest Version for the Data:
        if UPPER_LIMITS[(self.version,self.er_cor_level)][self.mode] - self.msg_len < 0:                     # We only have to change if it wasn't good version-er_cor_level
            if self.print_steps:
                print("Finding the best version and error correction level...")

            options = {'L': [], 'M': [], 'Q': [], 'H': []}
            for key, value in UPPER_LIMITS.items():
                valor   = value[self.mode]
                dif     = valor - self.msg_len
                if dif >= 0:
                    options[key[1]].append([dif, key[0], key[1]])
            options = { key: sorted(lista) for key,lista in options.items() }   # Sorting every list

            if len(options[self.er_cor_level]) == 0:
                best_options = sorted( list( options.values() ) )

                if len(best_options[0]) == 0 and len(best_options[1]) == 0 and len(best_options[2]) == 0 and len(best_options[3]) == 0:
                    print("It's impossible to encode this data")
                    exit(1)
                else:
                    print(f"It's not possible to encode this data using {self.er_cor_level}")
                    self.version = best_options[0][1]
                    self.er_cor_level = best_options[0][2]
            else:
                self.version = options[self.er_cor_level][0][1]

        if self.print_steps:
            print(f"Version: {self.version}-{self.er_cor_level}")

        groups_bits = []
        if self.mode == "Numeric":
            groups_bits = encodeNumeric()
        elif self.mode == "Alphanumeric":
            groups_bits = encodeAlphanumeric()
        elif self.mode == "Byte":
            groups_bits = encodeByte()

        if self.print_steps:
            print(f"Groups Bits ({len(groups_bits)}):",groups_bits)

        # Data String:
        self.data_string  = MODE_IND[self.mode]
        self.data_string += "{:0{}b}".format(self.msg_len, CHAR_CNT_IND[self.version][self.mode])
        self.data_string += ''.join(groups_bits)

        # Add a Terminator of 0's if Necessary:
        total_bits_req  = TOTAL_CODEWORDS[(self.version,self.er_cor_level)]["TotalData"] * 8 #
        dif             = total_bits_req - len(self.data_string)
        if dif > 4:
            self.data_string += "0000"
        else:
            self.data_string += "0" * dif

        # Add More 0s to Make the Length a Multiple of 8:
        self.data_string += "0" * ( (8 - (len(self.data_string) % 8) ) % 8)   # If mod 8 == 1 --> pad (8-1)%8 zeros | ... | mod 8 == 0 --> pad (8-0)%8 zeros

        # Add Pad Bytes if the String if Still too Short:
        pads_bytes = int((total_bits_req - len(self.data_string)) / 8)
        for pb in range( pads_bytes ):
            pad_byte = PADS_BYTES[pb % 2]
            self.data_string += pad_byte

        if self.print_steps:
            print( f"Data String ({len(self.data_string)}):", self.data_string )

    # ------------------------------------------------------------------------------------------------------------------
    def _errorCorrectionCoding(self):
        """
        https://www.thonky.com/qr-code-tutorial/error-correction-coding
        :return:
        """
        # ....................................................
        def generateErrorCorrectionCodewords(EC_per_block):
            ec_codewords = []
            for i, blocks in enumerate(self.data_codewords):
                #print("Group",i)
                for j, block in enumerate(blocks):
                    #print("\tBlock",j)
                    msg_poly = []
                    for k, codeword in enumerate(block):
                        msg_poly.append( int(codeword,2) )

                    if self.print_steps:
                        print("\tMSG POLY:", msg_poly)
                    min_len     = EC_per_block +1
                    gen_poly    = deepcopy(GENERATORS_POLYS[EC_per_block])                                          # Generator Polynom
                    result      = msg_poly.copy()

                    for CONT in range(len(msg_poly)):
                        result = result + [0 for _ in range(min_len - len(result) + 1)]                             # Padding zeros to be the same length of min_len

                        if result[0] == 0:
                            result = result[1:]                                                                     # Remove remaining counts as a step
                        else:
                            LTerm           = result[0]                                                             # Lead Term
                            LTerm_a         = LOG_ANTIVALUES[LTerm]                                                 # Lead Term Converted to Alpha
                            genVSlead_alpha = [ (LTerm_a + v) % 255 for v in gen_poly ]                             # Multiplication ignoring the pad's zeros (result in Alpha)
                            genVSlead_nmb   = [ LOG_VALUES[v] for v in genVSlead_alpha ]                            # Multiplication in Numbers
                            genVSlead_pad   = genVSlead_nmb + [ 0 for _ in range( max(min_len,len(result)) - len(genVSlead_nmb)) ]    # Padding Zeros to be the same length of MSG POLY
                            xor             = [ result[i] ^ genVSlead_pad[i] for i in range( max(len(result),min_len) ) ]              # Previous Result XOR Multiplication
                            result          = xor[1:]                                                               # Discarting the leading zero

                    if len(result) > EC_per_block:
                        result = result[0 : EC_per_block + 1]   # TODO: Check if it's correct...
                    ec_codewords.append( result )
            return ec_codewords

        # ....................................................
        # Data Codewords:
        self.data_string = [ self.data_string[i:i+8] for i in range(0,len(self.data_string),8)]     # Split the Data String into Codewords
        if self.print_steps:
            print(f'Data String Splitinto Codewords ({len(self.data_string)}):{self.data_string}')

        total_codewords         = TOTAL_CODEWORDS[(self.version,self.er_cor_level)]
        self.data_codewords     = [ [],[] ]  # 2 Groups

        blocks_groups    = [ total_codewords["BlocksGroup1"] , total_codewords["BlocksGroup2"] ]    # How many blocks per group
        codewords_groups = [ total_codewords["DataGroup1"]   , total_codewords["DataGroup2"]   ]    # How many codewords in each block

        cnt = 0
        for group_index, group in enumerate(self.data_codewords):
            for _ in range(blocks_groups[group_index]):
                group.append(self.data_string[cnt: cnt + codewords_groups[group_index]])
                cnt += codewords_groups[group_index]

        if self.print_steps:
            print(f"Data Codewords ({len(self.data_codewords)})({len(self.data_codewords[0])})({len(self.data_codewords[1])}):",self.data_codewords)

        # EC Codewords:
        self.ec_codewords  = generateErrorCorrectionCodewords(total_codewords["ECPerBlock"] )
        if self.print_steps:
            print(f"Error Correction Codewords ({len(self.ec_codewords)})({len(self.ec_codewords[0])}):", self.ec_codewords)
            print("Error Codewords Per Block:", total_codewords["ECPerBlock"])

    # ------------------------------------------------------------------------------------------------------------------
    def _structureFinalMessage(self,):
        """
        https://www.thonky.com/qr-code-tutorial/structure-final-message
        :return:
        """
        aux = []

        # Interleaving Data CodeWords
        blocks      = self.data_codewords[0] + self.data_codewords[1]
        long_len    = len( max(blocks, key=len) )
        for i in range(long_len):
            for b in range(len(blocks)):
                if i < len( blocks[b] ):
                    aux.append( int(blocks[b][i],2) )            # EC_Codewords are Integers, so let's convert this to Interger too, so in future we can convert everything to binary

        # Interleaving Error Correction CodeWords
        long_len = len(max(self.ec_codewords, key=len))
        for i in range(long_len):
            for b in range(len(self.ec_codewords)):
                if i < len(self.ec_codewords[b]):
                    aux.append( self.ec_codewords[b][i] )

        # Convert to Binary:
        aux = [ f"{v:08b}" for v in aux ]

        # Add Remainder Bits if Necessary:
        aux.append( "0"*REQUIRED_REMAINDER_BITS[self.version] )# TODO: just add if it's in the table?

        # Result:
        self.final_msg = ''.join(aux)
        if self.print_steps:
            print(f'Final MSG ({len(self.final_msg)}) = {self.final_msg}')

    # ------------------------------------------------------------------------------------------------------------------
    def _modulePlacementMatrix(self,):
        """
        https://www.thonky.com/qr-code-tutorial/module-placement-matrix
        :return:
        """
        # ....................................................
        def placeDataBits():
            rightCol    = self.size - 1
            leftCol     = self.size - 2
            curCol      = rightCol
            curRow      = self.size - 1
            data_indx   = 0
            rowCnt      = 0
            dir         = "up"

            while rightCol >= 0 and leftCol >= 0:
                if self.matrix[curRow][curCol] == "":
                    self.matrix[curRow][curCol] = self.final_msg[data_indx]
                    data_indx += 1

                curCol  = leftCol if curCol == rightCol else rightCol # ZigZag
                rowCnt += 1
                if rowCnt % 2 == 0:
                    if dir == "up":
                        curRow -= 1
                    else:
                        curRow += 1

                if curRow < 0 or curRow >= self.size:
                    if rightCol - 2 == 6:   # Timing Pattern
                        rightCol -= 3
                        leftCol  -= 3
                    else:
                        rightCol -= 2
                        leftCol  -= 2

                    curRow  = 0      if curRow < 0  else self.size - 1
                    dir     = "down" if curRow == 0 else "up"
                    curCol  = rightCol

        # ....................................................
        self.size   = (self.version - 1)*4 + 21
        self.matrix = [ ['' for col in range(self.size)] for row in range(self.size) ]

        # Find Patterns
        for row in range(7):
            for col in range(7):
                self.matrix[0               + row][0                + col] = f"FP{FIND_PATTERN[row][col]}"
                self.matrix[self.size - 7   + row][0                + col] = f"FP{FIND_PATTERN[row][col]}"
                self.matrix[0               + row][self.size - 7    + col] = f"FP{FIND_PATTERN[row][col]}"

        # Separators
        for row in range(8):
            self.matrix[row][7]                 = "VS0"   # TOP LEFT
            self.matrix[row][self.size - 8]     = "VS0"   # TOP RIGHT
            self.matrix[self.size - 8 + row][7] = "VS0"   # BOTTOM LEFT
        for col in range(7):
            self.matrix[7][col]                 = "HS0"   # TOP LEFT
            self.matrix[7][self.size - 7 + col] = "HS0"   # TOP RIGHT
            self.matrix[self.size - 8][col]     = "HS0"   # BOTTOM LEFT

        # Aligment Patterns
        algmnt_pat_pos = ALIGNMENT_PATTERN_POS[self.version]
        if algmnt_pat_pos is not None:
            for center_row in algmnt_pat_pos:
                for center_col in algmnt_pat_pos:
                    if center_col <= 11:                # The Aligment Pattern is way too close to left Finder Patterns
                        if center_row < 11 or center_row > self.size - 11:
                            continue
                    elif center_col > self.size - 11:   # The Aligment Patter is way too close the right Finder Patterns
                        if center_row < 11:
                            continue

                    for row in range(5):
                        row_offset = row - 2
                        for col in range(5):
                            col_offset = col - 2
                            self.matrix[center_row + row_offset][center_col + col_offset] = f"AP{ALIGNMENT_PATTERN[row][col]}"

        # Timing Patterns
        for i in range(8,self.size - 8, 1):
            self.matrix[6][i] = f'TP{(i+1)%2}'
            self.matrix[i][6] = f'TP{(i+1)%2}'

        # Dark Module
        self.matrix[(4 * self.version) + 9][8] = "BM1"

        # Reserve Format Information Area
        for row in range(9):
            if self.matrix[row][8] == "":
                self.matrix[row][8] = "FA0"
            if self.size - 7 + row < self.size and self.matrix[self.size - 7 + row][8] == "":
                self.matrix[self.size - 7 + row][8] = "FA0"
        for col in range(8):
            if self.matrix[8][col] == "":
                self.matrix[8][col] = "FA0"
            if self.matrix[8][self.size - 8 + col] == "":
                self.matrix[8][self.size - 8 + col] = "FA0"

        # Reserve Version Information Area
        if self.version >= 7:
            for i in range(6):
                for j in range(3):
                    self.matrix[i][self.size - 11 + j] = "VA0"
                    self.matrix[self.size - 11 + j][i] = "VA0"

        # Before Data Bits:
        #self.print()

        # Data Bits:
        placeDataBits()

    # ------------------------------------------------------------------------------------------------------------------
    def _dataMasking(self,):
        """
        https://www.thonky.com/qr-code-tutorial/data-masking
        :return:
        """
        """
        Mask patterns must ONLY be applied to data modules and error correction modules. In other words:
            Do not mask function patterns (finder patterns, timing patterns, separators, alignment patterns)
            Do not mask reserved areas (format information area, version information area)
            
        Resuming:
            Only there is 0 or 1 in our current matrix.
        """
        # ....................................................
        def applyMask(mask, matrix_input):
            from math import floor  # We're using it even if your IDE it's telling you otherwise

            for i in range(self.size):
                for j in range(self.size):
                    value = str(matrix_input[i][j])
                    #print(i, j, value, type(value))
                    if eval(MASK_PATTERNS[mask]) == 0:
                        if value == '0' or value == '1':
                            #print(i, j, value, type(value))
                            #print("\tmasking module")
                            matrix_input[i][j] = "0" if value == "1" else "1"

            return matrix_input

        # ....................................................
        def replaceStringToValue(matrix_input):
            for row in range(self.size):
                for col in range(self.size):
                    if matrix_input[row][col].isdecimal():
                        continue
                    matrix_input[row][col] = matrix_input[row][col][2]

            return matrix_input

        # ....................................................
        def showMaskedMatrix(matrix,mask):
            n = 3
            print('\nMASK',mask,"=" * self.size * (n + 2))
            for row in range(self.size):
                for col in range(self.size):
                    print(f"|{matrix[row][col]:^{n}}", end='')
                print("|")
            print()

        # ....................................................

        mask_scores     = [0 for _ in range(8)]
        forbidden_bits  = [ ['1','0','1','1','1','0','1','0','0','0','0'], ['0','0','0','0','1','0','1','1','1','0','1'] ]

        #self.print()
        for maskIndex in range(8):
            matrix = applyMask( maskIndex, deepcopy(self.matrix) )      # Aux Matrix masked
            #showMaskedMatrix(matrix, maskIndex)
            matrix = replaceStringToValue(matrix)                       # TODO: We have to change all string to 0 and 1, but, what about the FormatInformationArea and the VersionInformationArea ? For now, i'm placing 0's

            # Since it's a square matrix, we can 'cheat it' iterating through all column in a row and in the same time, all the rows in a column
            darkModules = 0
            for i in range(self.size):
                cntSameColorROW = 0
                cntSameColorCOL = 0
                lastColorROW    = matrix[i][0]
                lastColorCOL    = matrix[0][i]

                for j in range(self.size):
                    # Evaluation Condition 1 (row by row, column by column)
                    if lastColorROW == matrix[i][j]:
                        cntSameColorROW += 1
                        if cntSameColorROW == 5:
                            mask_scores[maskIndex] += 3
                        elif cntSameColorROW > 5:
                            mask_scores[maskIndex] += 1
                    else:
                        cntSameColorROW = 0

                    if lastColorCOL == matrix[j][i]:
                        cntSameColorCOL += 1
                        if cntSameColorCOL == 5:
                            mask_scores[maskIndex] += 3
                        elif cntSameColorCOL > 5:
                            mask_scores[maskIndex] += 1
                    else:
                        cntSameColorCOL = 0

                    # Evaluation Condition 2 (2x2 squares)
                    same = []
                    for row_square in range(2):
                        for col_square in range(2):
                            if i + row_square < self.size and j + col_square < self.size:
                                same.append( matrix[i][j] == matrix[i+row_square][j+col_square] )
                    if all(same):
                        mask_scores[maskIndex] += 3

                    # Evaluation Condition 3 (1 011 101 or 1 011 101 both directions)
                    if i + 10 < self.size:
                        aux = [matrix[i][j], matrix[i+1][j], matrix[i+2][j], matrix[i+3][j], matrix[i+4][j], matrix[i+5][j], matrix[i+6][j], matrix[i+7][j], matrix[i+8][j], matrix[i+9][j], matrix[i+10][j]]
                        if aux == forbidden_bits[0] or aux == forbidden_bits[1]:
                            mask_scores[maskIndex] += 40
                            #print(f"{'VERTC':<5} ({i:03},{j:03})", aux,)
                    if j + 10 < self.size:
                        if matrix[i][j:j+11] == forbidden_bits[0] or matrix[i][j:j+11] == forbidden_bits[1]:
                            mask_scores[maskIndex] += 40
                            #print(f"{'HORIZ':<5} ({i:03},{j:03})", matrix[i][j:j + 11],)

                    # Evaluation Condition 4 (Percentage of Dark Modules)
                    if matrix[i][j] == '1':
                        darkModules += 1

                    # Update:
                    lastColorROW = matrix[i][j]
                    lastColorCOL = matrix[j][i]

            # Evaluation Condition 4 (Percentage of Dark Modules)
            total_modules           = self.size * self.size
            percentage              = (darkModules / total_modules) * 100
            prev_mult_5             = (int(percentage/5) + 0) * 5
            next_mult_5             = (int(percentage/5) + 1) * 5
            prev                    = abs(50 - prev_mult_5) / 5
            next                    = abs(50 - next_mult_5) / 5
            mask_scores[maskIndex] += min(prev,next) * 10

        (min_score, mask) = min((v, i) for i, v in enumerate(mask_scores))
        if self.print_steps:
            print("Mask Scores: {}".format(mask_scores))
            print("Mask {} has the minimum score: {}".format(mask,min_score))

        self.mask   = mask
        self.matrix = applyMask(self.mask,self.matrix)
        self.matrix = replaceStringToValue(self.matrix)

    # ------------------------------------------------------------------------------------------------------------------
    def _formatAndVersionInformation(self,):
        """
        :return:
        """

        # FORMAT INFORMATION:
        self.format_string = FORMAT_STRINGS[(self.er_cor_level, self.mask)]

        # TODO: How to not Hardcode this?
        self.matrix[8][0] = self.format_string[ 0]
        self.matrix[8][1] = self.format_string[ 1]
        self.matrix[8][2] = self.format_string[ 2]
        self.matrix[8][3] = self.format_string[ 3]
        self.matrix[8][4] = self.format_string[ 4]
        self.matrix[8][5] = self.format_string[ 5]
        self.matrix[8][7] = self.format_string[ 6]
        self.matrix[8][8] = self.format_string[ 7]
        self.matrix[7][8] = self.format_string[ 8]
        self.matrix[5][8] = self.format_string[ 9]
        self.matrix[4][8] = self.format_string[10]
        self.matrix[3][8] = self.format_string[11]
        self.matrix[2][8] = self.format_string[12]
        self.matrix[1][8] = self.format_string[13]
        self.matrix[0][8] = self.format_string[14]

        # TODO: How to not Hardcode this?
        self.matrix[self.size - 1][8] = self.format_string[ 0]
        self.matrix[self.size - 2][8] = self.format_string[ 1]
        self.matrix[self.size - 3][8] = self.format_string[ 2]
        self.matrix[self.size - 4][8] = self.format_string[ 3]
        self.matrix[self.size - 5][8] = self.format_string[ 4]
        self.matrix[self.size - 6][8] = self.format_string[ 5]
        self.matrix[self.size - 7][8] = self.format_string[ 6]
        self.matrix[8][self.size - 8] = self.format_string[ 7]
        self.matrix[8][self.size - 7] = self.format_string[ 8]
        self.matrix[8][self.size - 6] = self.format_string[ 9]
        self.matrix[8][self.size - 5] = self.format_string[10]
        self.matrix[8][self.size - 4] = self.format_string[11]
        self.matrix[8][self.size - 3] = self.format_string[12]
        self.matrix[8][self.size - 2] = self.format_string[13]
        self.matrix[8][self.size - 1] = self.format_string[14]

        # VERSION INFORMATION:
        if self.version >= 7:
            self.version_string = VERSION_STRINGS[self.version]
            cnt = -1
            for i in range(6):
                for j in range(3):
                    self.matrix[i][self.size - 11 + j] = self.version_string[cnt]   # TOP RIGHT:    0,0 = R --> 0,1 = Q --> 0,2 = P ... 6,3 = A
                    self.matrix[self.size - 11 + j][i] = self.version_string[cnt]   # BOTTOM LEFT:  0,0 = R --> 1,0 = Q --> 2,0 = P ... 3,6 = A
                    cnt -= 1

# ======================================================================================================================
if __name__ == "__main__":
    import argparse
    import time

    parser = argparse.ArgumentParser(description="Generate your own QR Code")
    parser.add_argument('-i'     , required=True,  help='Input: Your Text'                   , action='store'       , type=str  )
    parser.add_argument('-o'     , required=False, help='Output: Name of your QR Code Image' , action='store'       , type=str  )
    parser.add_argument('-s'     , required=False, help='Display QR Code'                    , action='store_true'  ,   )
    parser.add_argument('-p'     , required=False, help='Print QR Code on Terminal'          , action='store_true'  ,   )
    parser.add_argument('--info' , required=False, help='Show all info about QR Code'        , action='store_true'  ,   )
    parser.add_argument('--debug', required=False, help='Print every step'                   , action='store_true'  ,   )
    arguments = parser.parse_args()

    try:
        # QR Code:
        qr = QrCode(arguments.i, print_steps=arguments.debug)

        # BMP Output:
        if arguments.o is not None:
            qr.bmp(arguments.o)
        else:
            maxlen = 20
            if len(arguments.i) > maxlen:
                name = arguments.i[0:maxlen-3] + '__'
            else:
                name = arguments.i

            qr.bmp( f"./{name}-{ int(round(time.time() * 1000)) }" )

        # Show using Matplotlib:
        if arguments.s:
            qr.show()

        # Show on Terminal:
        if arguments.p:
            qr.print(cnvToHashtag=True)

        # Show QR Code Info:
        if arguments.info:
            print(f'Input: |{qr.string_input}|')
            print(f'Input\'s Length: {qr.msg_len}')
            print(f'Mode: {qr.mode}')
            print(f'Version: {qr.version}')
            print(f'Error Correction Level: {qr.er_cor_level}')
            print(f'Size (QuitZone Included): {qr.size}x{qr.size}')
            print(f'Mask: {qr.mask}')

    except Exception as e:
        print("ERROR WHILE GENERATING QR CODE:", e, e.args)
        raise e

# ======================================================================================================================

"""
# Generating Multiples QR Codes for Test (Maximum Characters of Byte Encoding):

from random import randint

Upper_Limits_Byte   = [17, 14, 11, 7, 32, 26, 20, 14, 53, 42, 32, 24, 78, 62, 46, 34, 106, 84, 60, 44, 134, 106, 74, 58, 154, 122, 86, 64, 192, 152, 108, 84, 230,180, 130, 98, 271, 213, 151, 119, 321, 251, 177, 137, 367, 287, 203, 155, 425, 331, 241, 177, 458, 362, 258, 194, 520, 412, 292, 220, 586,450, 322, 250, 644, 504, 364, 280, 718, 560, 394, 310, 792, 624, 442, 338, 858, 666, 482, 382, 929, 711, 509, 403, 1003, 779, 565, 439, 1091,857, 611, 461, 1171, 911, 661, 511, 1273, 997, 715, 535, 1367, 1059, 751, 593, 1465, 1125, 805, 625, 1528, 1190, 868, 658, 1628, 1264, 908,698, 1732, 1370, 982, 742, 1840, 1452, 1030, 790, 1952, 1538, 1112, 842, 2068, 1628, 1168, 898, 2188, 1722, 1228, 958, 2303, 1809, 1283, 983,2431, 1911, 1351, 1051, 2563, 1989, 1423, 1093, 2699, 2099, 1499, 1139, 2809, 2213, 1579, 1219, 2953, 2331, 1663, 1273]
ECLs                = ['L', 'M', 'Q', 'H']
gabarito            = []

for i,up_lim in enumerate(Upper_Limits_Byte):
    string  = ''.join([chr(randint(97, 97 + 25)) for n in range(up_lim)])                   # Generate random string using a-z characters
    qr      = QrCode(string, error_corretion_level=ECLs[i%4])                               # Force the QR Code to use specific Error Correction Level
    gabarito.append( (f'{i};{up_lim};{qr.string_input};{qr.version};{qr.er_cor_level}') )   # Save QR Code information
    qr.bmp(f"images/{i:04}-{qr.version}-{qr.er_cor_level}", scale=10)                       # Write on disk the QR Code

with open('images/gabarito.csv','w') as f:
    f.write( '\n'.join(gabarito) )
"""