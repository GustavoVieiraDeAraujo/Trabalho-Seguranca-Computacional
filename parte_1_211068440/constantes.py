S_BOX = {
    "0": "63", "1": "7c", "2": "77", "3": "7b", "4": "f2", "5": "6b", "6": "6f", "7": "c5",
    "8": "30", "9": "1", "a": "67", "b": "2b", "c": "fe", "d": "d7", "e": "ab", "f": "76",
    "10": "ca", "11": "82", "12": "c9", "13": "7d", "14": "fa", "15": "59", "16": "47", "17": "f0",
    "18": "ad", "19": "d4", "1a": "a2", "1b": "af", "1c": "9c", "1d": "a4", "1e": "72", "1f": "c0",
    "20": "b7", "21": "fd", "22": "93", "23": "26", "24": "36", "25": "3f", "26": "f7", "27": "cc",
    "28": "34", "29": "a5", "2a": "e5", "2b": "f1", "2c": "71", "2d": "d8", "2e": "31", "2f": "15",
    "30": "4", "31": "c7", "32": "23", "33": "c3", "34": "18", "35": "96", "36": "5", "37": "9a",
    "38": "7", "39": "12", "3a": "80", "3b": "e2", "3c": "eb", "3d": "27", "3e": "b2", "3f": "75",
    "40": "9", "41": "83", "42": "2c", "43": "1a", "44": "1b", "45": "6e", "46": "5a", "47": "a0",
    "48": "52", "49": "3b", "4a": "d6", "4b": "b3", "4c": "29", "4d": "e3", "4e": "2f", "4f": "84",
    "50": "53", "51": "d1", "52": "0", "53": "ed", "54": "20", "55": "fc", "56": "b1", "57": "5b",
    "58": "6a", "59": "cb", "5a": "be", "5b": "39", "5c": "4a", "5d": "4c", "5e": "58", "5f": "cf",
    "60": "d0", "61": "ef", "62": "aa", "63": "fb", "64": "43", "65": "4d", "66": "33", "67": "85",
    "68": "45", "69": "f9", "6a": "2", "6b": "7f", "6c": "50", "6d": "3c", "6e": "9f", "6f": "a8",
    "70": "51", "71": "a3", "72": "40", "73": "8f", "74": "92", "75": "9d", "76": "38", "77": "f5",
    "78": "bc", "79": "b6", "7a": "da", "7b": "21", "7c": "10", "7d": "ff", "7e": "f3", "7f": "d2",
    "80": "cd", "81": "c", "82": "13", "83": "ec", "84": "5f", "85": "97", "86": "44", "87": "17",
    "88": "c4", "89": "a7", "8a": "7e", "8b": "3d", "8c": "64", "8d": "5d", "8e": "19", "8f": "73",
    "90": "60", "91": "81", "92": "4f", "93": "dc", "94": "22", "95": "2a", "96": "90", "97": "88",
    "98": "46", "99": "ee", "9a": "b8", "9b": "14", "9c": "de", "9d": "5e", "9e": "b", "9f": "db",
    "a0": "e0", "a1": "32", "a2": "3a", "a3": "a", "a4": "49", "a5": "6", "a6": "24", "a7": "5c",
    "a8": "c2", "a9": "d3", "aa": "ac", "ab": "62", "ac": "91", "ad": "95", "ae": "e4", "af": "79",
    "b0": "e7", "b1": "c8", "b2": "37", "b3": "6d", "b4": "8d", "b5": "d5", "b6": "4e", "b7": "a9",
    "b8": "6c", "b9": "56", "ba": "f4", "bb": "ea", "bc": "65", "bd": "7a", "be": "ae", "bf": "8",
    "c0": "ba", "c1": "78", "c2": "25", "c3": "2e", "c4": "1c", "c5": "a6", "c6": "b4", "c7": "c6",
    "c8": "e8", "c9": "dd", "ca": "74", "cb": "1f", "cc": "4b", "cd": "bd", "ce": "8b", "cf": "8a",
    "d0": "70", "d1": "3e", "d2": "b5", "d3": "66", "d4": "48", "d5": "3", "d6": "f6", "d7": "e",
    "d8": "61", "d9": "35", "da": "57", "db": "b9", "dc": "86", "dd": "c1", "de": "1d", "df": "9e",
    "e0": "e1", "e1": "f8", "e2": "98", "e3": "11", "e4": "69", "e5": "d9", "e6": "8e", "e7": "94",
    "e8": "9b", "e9": "1e", "ea": "87", "eb": "e9", "ec": "ce", "ed": "55", "ee": "28", "ef": "df",
    "f0": "8c", "f1": "a1", "f2": "89", "f3": "d", "f4": "bf", "f5": "e6", "f6": "42", "f7": "68",
    "f8": "41", "f9": "99", "fa": "2d", "fb": "f", "fc": "b0", "fd": "54", "fe": "bb", "ff": "16"
}

INVERTED_S_BOX = {value: key for key, value in S_BOX.items()}

RCON = [0x00000000, 0x01000000, 0x02000000, 0x04000000, 0x08000000, 0x10000000, 0x20000000, 0x40000000, 0x80000000, 0x1b000000, 0x36000000]