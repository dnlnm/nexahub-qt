"""QMK Keycode name lookup table.

Maps keycode hex values to human-readable QMK names.
Updated with complete keycodes from vial-code/keycodes_v6.py
"""

# Basic keycodes (0x0000 - 0x00FF)
BASIC_KEYCODES = {
    0x0000: "KC_NO",
    0x0001: "KC_TRNS",
    0x0004: "KC_A",
    0x0005: "KC_B",
    0x0006: "KC_C",
    0x0007: "KC_D",
    0x0008: "KC_E",
    0x0009: "KC_F",
    0x000A: "KC_G",
    0x000B: "KC_H",
    0x000C: "KC_I",
    0x000D: "KC_J",
    0x000E: "KC_K",
    0x000F: "KC_L",
    0x0010: "KC_M",
    0x0011: "KC_N",
    0x0012: "KC_O",
    0x0013: "KC_P",
    0x0014: "KC_Q",
    0x0015: "KC_R",
    0x0016: "KC_S",
    0x0017: "KC_T",
    0x0018: "KC_U",
    0x0019: "KC_V",
    0x001A: "KC_W",
    0x001B: "KC_X",
    0x001C: "KC_Y",
    0x001D: "KC_Z",
    0x001E: "KC_1",
    0x001F: "KC_2",
    0x0020: "KC_3",
    0x0021: "KC_4",
    0x0022: "KC_5",
    0x0023: "KC_6",
    0x0024: "KC_7",
    0x0025: "KC_8",
    0x0026: "KC_9",
    0x0027: "KC_0",
    0x0028: "KC_ENTER",
    0x0029: "KC_ESCAPE",
    0x002A: "KC_BSPACE",
    0x002B: "KC_TAB",
    0x002C: "KC_SPACE",
    0x002D: "KC_MINUS",
    0x002E: "KC_EQUAL",
    0x002F: "KC_LBRACKET",
    0x0030: "KC_RBRACKET",
    0x0031: "KC_BSLASH",
    0x0032: "KC_NONUS_HASH",
    0x0033: "KC_SCOLON",
    0x0034: "KC_QUOTE",
    0x0035: "KC_GRAVE",
    0x0036: "KC_COMMA",
    0x0037: "KC_DOT",
    0x0038: "KC_SLASH",
    0x0039: "KC_CAPSLOCK",
    0x003A: "KC_F1",
    0x003B: "KC_F2",
    0x003C: "KC_F3",
    0x003D: "KC_F4",
    0x003E: "KC_F5",
    0x003F: "KC_F6",
    0x0040: "KC_F7",
    0x0041: "KC_F8",
    0x0042: "KC_F9",
    0x0043: "KC_F10",
    0x0044: "KC_F11",
    0x0045: "KC_F12",
    0x0046: "KC_PSCREEN",
    0x0047: "KC_SCROLLLOCK",
    0x0048: "KC_PAUSE",
    0x0049: "KC_INSERT",
    0x004A: "KC_HOME",
    0x004B: "KC_PGUP",
    0x004C: "KC_DELETE",
    0x004D: "KC_END",
    0x004E: "KC_PGDOWN",
    0x004F: "KC_RIGHT",
    0x0050: "KC_LEFT",
    0x0051: "KC_DOWN",
    0x0052: "KC_UP",
    0x0053: "KC_NUMLOCK",
    0x0054: "KC_KP_SLASH",
    0x0055: "KC_KP_ASTERISK",
    0x0056: "KC_KP_MINUS",
    0x0057: "KC_KP_PLUS",
    0x0058: "KC_KP_ENTER",
    0x0059: "KC_KP_1",
    0x005A: "KC_KP_2",
    0x005B: "KC_KP_3",
    0x005C: "KC_KP_4",
    0x005D: "KC_KP_5",
    0x005E: "KC_KP_6",
    0x005F: "KC_KP_7",
    0x0060: "KC_KP_8",
    0x0061: "KC_KP_9",
    0x0062: "KC_KP_0",
    0x0063: "KC_KP_DOT",
    0x0064: "KC_NONUS_BSLASH",
    0x0065: "KC_APPLICATION",
    0x0067: "KC_KP_EQUAL",
    0x0068: "KC_F13",
    0x0069: "KC_F14",
    0x006A: "KC_F15",
    0x006B: "KC_F16",
    0x006C: "KC_F17",
    0x006D: "KC_F18",
    0x006E: "KC_F19",
    0x006F: "KC_F20",
    0x0070: "KC_F21",
    0x0071: "KC_F22",
    0x0072: "KC_F23",
    0x0073: "KC_F24",
    0x0074: "KC_EXEC",
    0x0075: "KC_HELP",
    0x0077: "KC_SLCT",
    0x0078: "KC_STOP",
    0x0079: "KC_AGIN",
    0x007A: "KC_UNDO",
    0x007B: "KC_CUT",
    0x007C: "KC_COPY",
    0x007D: "KC_PSTE",
    0x007E: "KC_FIND",
    0x0080: "KC__VOLUP",
    0x0081: "KC__VOLDOWN",
    0x0082: "KC_LCAP",
    0x0083: "KC_LNUM",
    0x0084: "KC_LSCR",
    0x0085: "KC_KP_COMMA",
    0x0087: "KC_RO",
    0x0088: "KC_KANA",
    0x0089: "KC_JYEN",
    0x008A: "KC_HENK",
    0x008B: "KC_MHEN",
    0x0090: "KC_LANG1",
    0x0091: "KC_LANG2",
    0x00A5: "KC_LCTRL",
    0x00A6: "KC_LSHIFT",
    0x00A7: "KC_LALT",
    0x00A8: "KC_LGUI",
    0x00A9: "KC_RCTRL",
    0x00AA: "KC_RSHIFT",
    0x00AB: "KC_RALT",
    0x00AC: "KC_RGUI",
    0x00CD: "KC_MS_U",
    0x00CE: "KC_MS_D",
    0x00CF: "KC_MS_L",
    0x00D0: "KC_MS_R",
    0x00D1: "KC_BTN1",
    0x00D2: "KC_BTN2",
    0x00D3: "KC_BTN3",
    0x00D4: "KC_BTN4",
    0x00D5: "KC_BTN5",
    0x00D9: "KC_WH_U",
    0x00DA: "KC_WH_D",
    0x00DB: "KC_WH_L",
    0x00DC: "KC_WH_R",
    0x00DD: "KC_ACL0",
    0x00DE: "KC_ACL1",
    0x00DF: "KC_ACL2",
}

# Shifted keycodes (modifiers applied)
SHIFTED_KEYCODES = {
    0x0235: "KC_TILD",
    0x021E: "KC_EXLM",
    0x021F: "KC_AT",
    0x0220: "KC_HASH",
    0x0221: "KC_DLR",
    0x0222: "KC_PERC",
    0x0223: "KC_CIRC",
    0x0224: "KC_AMPR",
    0x0225: "KC_ASTR",
    0x0226: "KC_LPRN",
    0x0227: "KC_RPRN",
    0x022D: "KC_UNDS",
    0x022E: "KC_PLUS",
    0x022F: "KC_LCBR",
    0x0230: "KC_RCBR",
    0x0236: "KC_LT",
    0x0237: "KC_GT",
    0x0233: "KC_COLN",
    0x0231: "KC_PIPE",
    0x0238: "KC_QUES",
    0x0234: "KC_DQUO",
}

# Mod-Tap keycodes (0x2000 - 0x3FFF)
MOD_TAP_KEYCODES = {
    0x2F00: "ALL_T(kc)",
    0x2300: "C_S_T(kc)",
    0x2400: "LALT_T(kc)",
    0x2500: "LCA_T(kc)",
    0x2C00: "LAG_T(kc)",
    0x2D00: "LCAG_T(kc)",
    0x2900: "LCG_T(kc)",
    0x2100: "LCTL_T(kc)",
    0x2800: "LGUI_T(kc)",
    0x2600: "LSA_T(kc)",
    0x2200: "LSFT_T(kc)",
    0x2700: "MEH_T(kc)",
    0x3400: "RALT_T(kc)",
    0x3D00: "RCAG_T(kc)",
    0x3900: "RCG_T(kc)",
    0x3100: "RCTL_T(kc)",
    0x3800: "RGUI_T(kc)",
    0x3200: "RSFT_T(kc)",
    0x2A00: "SGUI_T(kc)",
}

# Layer-Tap base keycodes (0x4000 - 0x4FFF)
LAYER_TAP_BASE = 0x4000

# Layer-Mod base (0x5000 - 0x51FF)
LAYER_MOD_BASE = 0x5000

# One Shot Mod keycodes (0x52A0 - 0x52BF)
ONE_SHOT_MOD_KEYCODES = {
    0x52A1: "OSM(MOD_LCTL)",
    0x52A2: "OSM(MOD_LSFT)",
    0x52A3: "OSM(MOD_LCTL|MOD_LSFT)",
    0x52A4: "OSM(MOD_LALT)",
    0x52A5: "OSM(MOD_LCTL|MOD_LALT)",
    0x52A6: "OSM(MOD_LSFT|MOD_LALT)",
    0x52A7: "OSM(MOD_MEH)",
    0x52A8: "OSM(MOD_LGUI)",
    0x52A9: "OSM(MOD_LCTL|MOD_LGUI)",
    0x52AA: "OSM(MOD_LSFT|MOD_LGUI)",
    0x52AB: "OSM(MOD_LCTL|MOD_LSFT|MOD_LGUI)",
    0x52AC: "OSM(MOD_LALT|MOD_LGUI)",
    0x52AD: "OSM(MOD_LCTL|MOD_LALT|MOD_LGUI)",
    0x52AE: "OSM(MOD_LSFT|MOD_LALT|MOD_LGUI)",
    0x52AF: "OSM(MOD_HYPR)",
    0x52B1: "OSM(MOD_RCTL)",
    0x52B2: "OSM(MOD_RSFT)",
    0x52B3: "OSM(MOD_RCTL|MOD_RSFT)",
    0x52B4: "OSM(MOD_RALT)",
    0x52B5: "OSM(MOD_RCTL|MOD_RALT)",
    0x52B6: "OSM(MOD_RSFT|MOD_RALT)",
    0x52B7: "OSM(MOD_RCTL|MOD_RSFT|MOD_RALT)",
    0x52B8: "OSM(MOD_RGUI)",
    0x52B9: "OSM(MOD_RCTL|MOD_RGUI)",
    0x52BA: "OSM(MOD_RSFT|MOD_RGUI)",
    0x52BB: "OSM(MOD_RCTL|MOD_RSFT|MOD_RGUI)",
    0x52BC: "OSM(MOD_RALT|MOD_RGUI)",
    0x52BD: "OSM(MOD_RCTL|MOD_RALT|MOD_RGUI)",
    0x52BE: "OSM(MOD_RSFT|MOD_RALT|MOD_RGUI)",
    0x52BF: "OSM(MOD_RCTL|MOD_RSFT|MOD_RALT|MOD_RGUI)",
}

# Tap Dance base (0x5700 - 0x57FF)
TAP_DANCE_BASE = 0x5700

# Macro base (0x7700 - 0x777F)
MACRO_BASE = 0x7700

# RGB keycodes (0x7800 - 0x78FF)
RGB_KEYCODES = {
    0x7820: "RGB_TOG",
    0x7821: "RGB_MOD",
    0x7822: "RGB_RMOD",
    0x7823: "RGB_HUI",
    0x7824: "RGB_HUD",
    0x7825: "RGB_SAI",
    0x7826: "RGB_SAD",
    0x7827: "RGB_VAI",
    0x7828: "RGB_VAD",
    0x7829: "RGB_SPI",
    0x782A: "RGB_SPD",
    0x782B: "RGB_M_P",
    0x782C: "RGB_M_B",
    0x782D: "RGB_M_R",
    0x782E: "RGB_M_SW",
    0x782F: "RGB_M_SN",
    0x7830: "RGB_M_K",
    0x7831: "RGB_M_X",
    0x7832: "RGB_M_G",
    0x7833: "RGB_M_T",
}

# Backlight keycodes (0x7800 - 0x7806)
BACKLIGHT_KEYCODES = {
    0x7800: "BL_ON",
    0x7801: "BL_OFF",
    0x7802: "BL_TOGG",
    0x7803: "BL_DEC",
    0x7804: "BL_INC",
    0x7805: "BL_STEP",
    0x7806: "BL_BRTG",
}

# Audio keycodes (0x7480 - 0x7493)
AUDIO_KEYCODES = {
    0x7480: "AU_ON",
    0x7481: "AU_OFF",
    0x7482: "AU_TOG",
    0x748A: "CLICKY_TOGGLE",
    0x748D: "CLICKY_UP",
    0x748E: "CLICKY_DOWN",
    0x748F: "CLICKY_RESET",
    0x7490: "MU_ON",
    0x7491: "MU_OFF",
    0x7492: "MU_TOG",
    0x7493: "MU_MOD",
}

# Haptic keycodes (0x7C40 - 0x7C4C)
HAPTIC_KEYCODES = {
    0x7C40: "HPT_ON",
    0x7C41: "HPT_OFF",
    0x7C42: "HPT_TOG",
    0x7C43: "HPT_RST",
    0x7C44: "HPT_FBK",
    0x7C45: "HPT_BUZ",
    0x7C46: "HPT_MODI",
    0x7C47: "HPT_MODD",
    0x7C48: "HPT_CONT",
    0x7C49: "HPT_CONI",
    0x7C4A: "HPT_COND",
    0x7C4B: "HPT_DWLI",
    0x7C4C: "HPT_DWLD",
}

# Auto Shift keycodes (0x7C10 - 0x7C15)
AUTO_SHIFT_KEYCODES = {
    0x7C10: "KC_ASDN",
    0x7C11: "KC_ASUP",
    0x7C12: "KC_ASRP",
    0x7C13: "KC_ASON",
    0x7C14: "KC_ASOFF",
    0x7C15: "KC_ASTG",
}

# Combo keycodes (0x7C50 - 0x7C52)
COMBO_KEYCODES = {
    0x7C50: "CMB_ON",
    0x7C51: "CMB_OFF",
    0x7C52: "CMB_TOG",
}

# Dynamic Macro keycodes (0x7C53 - 0x7C57)
DYNAMIC_MACRO_KEYCODES = {
    0x7C53: "DYN_REC_START1",
    0x7C54: "DYN_REC_START2",
    0x7C55: "DYN_REC_STOP",
    0x7C56: "DYN_MACRO_PLAY1",
    0x7C57: "DYN_MACRO_PLAY2",
}

# MIDI keycodes (0x7103 - 0x718F)
MIDI_KEYCODES = {
    0x7103: "MI_C",
    0x7104: "MI_Cs",
    0x7105: "MI_D",
    0x7106: "MI_Ds",
    0x7107: "MI_E",
    0x7108: "MI_F",
    0x7109: "MI_Fs",
    0x710A: "MI_G",
    0x710B: "MI_Gs",
    0x710C: "MI_A",
    0x710D: "MI_As",
    0x710E: "MI_B",
    0x710F: "MI_C_1",
    0x7110: "MI_Cs_1",
    0x7111: "MI_D_1",
    0x7112: "MI_Ds_1",
    0x7113: "MI_E_1",
    0x7114: "MI_F_1",
    0x7115: "MI_Fs_1",
    0x7116: "MI_G_1",
    0x7117: "MI_Gs_1",
    0x7118: "MI_A_1",
    0x7119: "MI_As_1",
    0x711A: "MI_B_1",
    0x711B: "MI_C_2",
    0x711C: "MI_Cs_2",
    0x711D: "MI_D_2",
    0x711E: "MI_Ds_2",
    0x711F: "MI_E_2",
    0x7120: "MI_F_2",
    0x7121: "MI_Fs_2",
    0x7122: "MI_G_2",
    0x7123: "MI_Gs_2",
    0x7124: "MI_A_2",
    0x7125: "MI_As_2",
    0x7126: "MI_B_2",
    0x7127: "MI_C_3",
    0x7128: "MI_Cs_3",
    0x7129: "MI_D_3",
    0x712A: "MI_Ds_3",
    0x712B: "MI_E_3",
    0x712C: "MI_F_3",
    0x712D: "MI_Fs_3",
    0x712E: "MI_G_3",
    0x712F: "MI_Gs_3",
    0x7130: "MI_A_3",
    0x7131: "MI_As_3",
    0x7132: "MI_B_3",
    0x7133: "MI_C_4",
    0x7134: "MI_Cs_4",
    0x7135: "MI_D_4",
    0x7136: "MI_Ds_4",
    0x7137: "MI_E_4",
    0x7138: "MI_F_4",
    0x7139: "MI_Fs_4",
    0x713A: "MI_G_4",
    0x713B: "MI_Gs_4",
    0x713C: "MI_A_4",
    0x713D: "MI_As_4",
    0x713E: "MI_B_4",
    0x713F: "MI_C_5",
    0x7140: "MI_Cs_5",
    0x7141: "MI_D_5",
    0x7142: "MI_Ds_5",
    0x7143: "MI_E_5",
    0x7144: "MI_F_5",
    0x7145: "MI_Fs_5",
    0x7146: "MI_G_5",
    0x7147: "MI_Gs_5",
    0x7148: "MI_A_5",
    0x7149: "MI_As_5",
    0x714A: "MI_B_5",
    0x714B: "MI_OCT_N2",
    0x714C: "MI_OCT_N1",
    0x714D: "MI_OCT_0",
    0x714E: "MI_OCT_1",
    0x714F: "MI_OCT_2",
    0x7150: "MI_OCT_3",
    0x7151: "MI_OCT_4",
    0x7152: "MI_OCT_5",
    0x7153: "MI_OCT_6",
    0x7154: "MI_OCT_7",
    0x7155: "MI_OCTD",
    0x7156: "MI_OCTU",
    0x7157: "MI_TRNS_N6",
    0x7158: "MI_TRNS_N5",
    0x7159: "MI_TRNS_N4",
    0x715A: "MI_TRNS_N3",
    0x715B: "MI_TRNS_N2",
    0x715C: "MI_TRNS_N1",
    0x715D: "MI_TRNS_0",
    0x715E: "MI_TRNS_1",
    0x715F: "MI_TRNS_2",
    0x7160: "MI_TRNS_3",
    0x7161: "MI_TRNS_4",
    0x7162: "MI_TRNS_5",
    0x7163: "MI_TRNS_6",
    0x7164: "MI_TRNSD",
    0x7165: "MI_TRNSU",
    0x7167: "MI_VEL_1",
    0x7168: "MI_VEL_2",
    0x7169: "MI_VEL_3",
    0x716A: "MI_VEL_4",
    0x716B: "MI_VEL_5",
    0x716C: "MI_VEL_6",
    0x716D: "MI_VEL_7",
    0x716E: "MI_VEL_8",
    0x716F: "MI_VEL_9",
    0x7170: "MI_VEL_10",
    0x7171: "MI_VELD",
    0x7172: "MI_VELU",
    0x7173: "MI_CH1",
    0x7174: "MI_CH2",
    0x7175: "MI_CH3",
    0x7176: "MI_CH4",
    0x7177: "MI_CH5",
    0x7178: "MI_CH6",
    0x7179: "MI_CH7",
    0x717A: "MI_CH8",
    0x717B: "MI_CH9",
    0x717C: "MI_CH10",
    0x717D: "MI_CH11",
    0x717E: "MI_CH12",
    0x717F: "MI_CH13",
    0x7180: "MI_CH14",
    0x7181: "MI_CH15",
    0x7182: "MI_CH16",
    0x7183: "MI_CHD",
    0x7184: "MI_CHU",
    0x7185: "MI_ALLOFF",
    0x7186: "MI_SUS",
    0x7187: "MI_PORT",
    0x7188: "MI_SOST",
    0x7189: "MI_SOFT",
    0x718A: "MI_LEG",
    0x718B: "MI_MOD",
    0x718C: "MI_MODSD",
    0x718D: "MI_MODSU",
    0x718E: "MI_BENDD",
    0x718F: "MI_BENDU",
}

# Magic keycodes (0x7000 - 0x701F)
MAGIC_KEYCODES = {
    0x7000: "MAGIC_SWAP_CONTROL_CAPSLOCK",
    0x7001: "MAGIC_UNSWAP_CONTROL_CAPSLOCK",
    0x7003: "MAGIC_UNCAPSLOCK_TO_CONTROL",
    0x7004: "MAGIC_CAPSLOCK_TO_CONTROL",
    0x7005: "MAGIC_SWAP_LALT_LGUI",
    0x7006: "MAGIC_UNSWAP_LALT_LGUI",
    0x7007: "MAGIC_SWAP_RALT_RGUI",
    0x7008: "MAGIC_UNSWAP_RALT_RGUI",
    0x7009: "MAGIC_UNNO_GUI",
    0x700A: "MAGIC_NO_GUI",
    0x700B: "MAGIC_TOGGLE_GUI",
    0x700C: "MAGIC_SWAP_GRAVE_ESC",
    0x700D: "MAGIC_UNSWAP_GRAVE_ESC",
    0x700E: "MAGIC_SWAP_BACKSLASH_BACKSPACE",
    0x700F: "MAGIC_UNSWAP_BACKSLASH_BACKSPACE",
    0x7011: "MAGIC_HOST_NKRO",
    0x7012: "MAGIC_UNHOST_NKRO",
    0x7013: "MAGIC_TOGGLE_NKRO",
    0x7014: "MAGIC_SWAP_ALT_GUI",
    0x7015: "MAGIC_UNSWAP_ALT_GUI",
    0x7016: "MAGIC_TOGGLE_ALT_GUI",
    0x7017: "MAGIC_SWAP_LCTL_LGUI",
    0x7018: "MAGIC_UNSWAP_LCTL_LGUI",
    0x7019: "MAGIC_SWAP_RCTL_RGUI",
    0x701A: "MAGIC_UNSWAP_RCTL_RGUI",
    0x701B: "MAGIC_SWAP_CTL_GUI",
    0x701C: "MAGIC_UNSWAP_CTL_GUI",
    0x701D: "MAGIC_TOGGLE_CTL_GUI",
    0x701E: "MAGIC_EE_HANDS_LEFT",
    0x701F: "MAGIC_EE_HANDS_RIGHT",
}

# Special keycodes (0x7C00 - 0x7C7B)
SPECIAL_KEYCODES = {
    0x7C00: "QK_BOOT",
    0x7C01: "QK_REBOOT",
    0x7C03: "QK_CLEAR_EEPROM",
    0x7C16: "KC_GESC",
    0x7C18: "KC_LCPO",
    0x7C19: "KC_RCPC",
    0x7C1A: "KC_LSPO",
    0x7C1B: "KC_RSPC",
    0x7C1C: "KC_LAPO",
    0x7C1D: "KC_RAPC",
    0x7C1E: "KC_SFTENT",
    0x7C73: "QK_CAPS_WORD_TOGGLE",
    0x7C77: "FN_MO13",
    0x7C78: "FN_MO23",
    0x7C79: "QK_REPEAT_KEY",
    0x7C7A: "QK_ALT_REPEAT_KEY",
    0x7C7B: "QK_LAYER_LOCK",
}

# Media keycodes
MEDIA_KEYCODES = {
    0x00A8: "KC_PWR",
    0x00A9: "KC_SLEP",
    0x00AA: "KC_WAKE",
    0x00AC: "KC_MUTE",
    0x00AD: "KC_VOLU",
    0x00AE: "KC_VOLD",
    0x00B3: "KC_MNXT",
    0x00B4: "KC_MPRV",
    0x00B5: "KC_MSTP",
    0x00B6: "KC_MPLY",
    0x00B7: "KC_MSEL",
    0x00B8: "KC_EJCT",
    0x00BC: "KC_MRWD",
    0x00BD: "KC_MFFD",
    0x00B1: "KC_CALC",
    0x00B0: "KC_MAIL",
    0x00B4: "KC_MYCM",
    0x00B5: "KC_WSCH",
    0x00B6: "KC_WHOM",
    0x00B7: "KC_WBAK",
    0x00B8: "KC_WFWD",
    0x00B9: "KC_WSTP",
    0x00BA: "KC_WREF",
    0x00BB: "KC_WFAV",
    0x00BE: "KC_BRIU",
    0x00BF: "KC_BRID",
}

# RGB Matrix keycodes (0x7840 - 0x784C)
RGB_MATRIX_KEYCODES = {
    0x7840: "RM_ON",
    0x7841: "RM_OFF",
    0x7842: "RM_TOGG",
    0x7843: "RM_NEXT",
    0x7844: "RM_PREV",
    0x7845: "RM_HUEU",
    0x7846: "RM_HUED",
    0x7847: "RM_SATU",
    0x7848: "RM_SATD",
    0x7849: "RM_VALU",
    0x784A: "RM_VALD",
    0x784B: "RM_SPDU",
    0x784C: "RM_SPDD",
}

# User keycodes base (0x7E00 - 0x7E3F)
USER_KEYCODE_BASE = 0x7E00

# Make all keycode dictionaries into one lookup
ALL_KEYCODE_DICTS = [
    BASIC_KEYCODES,
    SHIFTED_KEYCODES,
    MOD_TAP_KEYCODES,
    ONE_SHOT_MOD_KEYCODES,
    RGB_KEYCODES,
    BACKLIGHT_KEYCODES,
    AUDIO_KEYCODES,
    HAPTIC_KEYCODES,
    AUTO_SHIFT_KEYCODES,
    COMBO_KEYCODES,
    DYNAMIC_MACRO_KEYCODES,
    MIDI_KEYCODES,
    MAGIC_KEYCODES,
    SPECIAL_KEYCODES,
    MEDIA_KEYCODES,
    RGB_MATRIX_KEYCODES,
]


def get_mods_keycode(keycode: int) -> str:
    """Generate MOD keycode name."""
    mods = (keycode >> 8) & 0x0F
    kc = keycode & 0xFF

    mod_names = []
    if mods & 0x01:
        mod_names.append("LCTL")
    if mods & 0x02:
        mod_names.append("LSFT")
    if mods & 0x04:
        mod_names.append("LALT")
    if mods & 0x08:
        mod_names.append("LGUI")
    if mods & 0x11:
        mod_names.append("RCTL")
    if mods & 0x12:
        mod_names.append("RSFT")
    if mods & 0x14:
        mod_names.append("RALT")
    if mods & 0x18:
        mod_names.append("RGUI")

    base_name = BASIC_KEYCODES.get(kc, f"0x{kc:02X}")
    if mod_names:
        return f"{'+'.join(mod_names)}({base_name})"
    return base_name


def get_mod_tap_keycode(keycode: int) -> str:
    """Generate MT keycode name."""
    mods = (keycode >> 8) & 0x0F
    kc = keycode & 0xFF

    mod_names = []
    if mods & 0x01:
        mod_names.append("CTL")
    if mods & 0x02:
        mod_names.append("SFT")
    if mods & 0x04:
        mod_names.append("ALT")
    if mods & 0x08:
        mod_names.append("GUI")

    base_name = BASIC_KEYCODES.get(kc, f"0x{kc:02X}")
    if mod_names:
        return f"MT({'|'.join(mod_names)},{base_name})"
    return f"MT({base_name})"


def get_layer_tap_keycode(keycode: int) -> str:
    """Generate LT keycode name."""
    layer = (keycode >> 8) & 0x0F
    kc = keycode & 0xFF
    base_name = BASIC_KEYCODES.get(kc, f"0x{kc:02X}")
    return f"LT({layer},{base_name})"


def get_layer_mod_keycode(keycode: int) -> str:
    """Generate LM keycode name."""
    layer = (keycode >> 4) & 0x0F
    mods = keycode & 0x0F

    mod_names = []
    if mods & 0x01:
        mod_names.append("CTL")
    if mods & 0x02:
        mod_names.append("SFT")
    if mods & 0x04:
        mod_names.append("ALT")
    if mods & 0x08:
        mod_names.append("GUI")

    if mod_names:
        return f"LM({layer},{'+'.join(mod_names)})"
    return f"LM({layer})"


def get_to_keycode(keycode: int) -> str:
    """Generate TO keycode name."""
    layer = keycode & 0x1F
    return f"TO({layer})"


def get_mo_keycode(keycode: int) -> str:
    """Generate MO keycode name."""
    layer = keycode & 0x1F
    return f"MO({layer})"


def get_df_keycode(keycode: int) -> str:
    """Generate DF keycode name."""
    layer = keycode & 0x1F
    return f"DF({layer})"


def get_tg_keycode(keycode: int) -> str:
    """Generate TG keycode name."""
    layer = keycode & 0x1F
    return f"TG({layer})"


def get_osl_keycode(keycode: int) -> str:
    """Generate OSL keycode name."""
    layer = keycode & 0x1F
    return f"OSL({layer})"


def get_osm_keycode(keycode: int) -> str:
    """Generate OSM keycode name."""
    mods = keycode & 0x0F

    mod_names = []
    if mods & 0x01:
        mod_names.append("CTL")
    if mods & 0x02:
        mod_names.append("SFT")
    if mods & 0x04:
        mod_names.append("ALT")
    if mods & 0x08:
        mod_names.append("GUI")

    if mod_names:
        return f"OSM({'|'.join(mod_names)})"
    return "OSM()"


def get_tt_keycode(keycode: int) -> str:
    """Generate TT keycode name."""
    layer = keycode & 0x1F
    return f"TT({layer})"


def get_pdf_keycode(keycode: int) -> str:
    """Generate PDF keycode name."""
    layer = keycode & 0x1F
    return f"PDF({layer})"


def get_swap_hands_keycode(keycode: int) -> str:
    """Generate SH keycode name."""
    kc = keycode & 0xFF
    if kc in BASIC_KEYCODES:
        return f"SH_{BASIC_KEYCODES[kc]}"
    return f"SH(0x{kc:02X})"


def get_tap_dance_keycode(keycode: int) -> str:
    """Generate TD keycode name."""
    idx = keycode & 0xFF
    return f"TD({idx})"


def get_macro_keycode(keycode: int) -> str:
    """Generate M keycode name."""
    idx = keycode & 0x7F
    return f"M({idx})"


def get_user_keycode(keycode: int) -> str:
    """Generate USER keycode name."""
    idx = keycode & 0x3F
    return f"USER{idx:02d}"


def get_keycode_name(keycode: int) -> str:
    """Convert a keycode value to its QMK name.

    Args:
        keycode: 16-bit keycode value

    Returns:
        QMK keycode name string
    """
    if keycode == 0x0000:
        return "KC_NO"
    if keycode == 0x0001:
        return "KC_TRNS"

    # Check basic and special keycode dictionaries
    for kd in ALL_KEYCODE_DICTS:
        if keycode in kd:
            return kd[keycode]

    # Check range-based keycodes
    # Mods: 0x0100 - 0x1FFF
    if 0x0100 <= keycode <= 0x1FFF:
        return get_mods_keycode(keycode)

    # Mod-Tap: 0x2000 - 0x3FFF
    if 0x2000 <= keycode <= 0x3FFF:
        return get_mod_tap_keycode(keycode)

    # Layer-Tap: 0x4000 - 0x4FFF
    if 0x4000 <= keycode <= 0x4FFF:
        return get_layer_tap_keycode(keycode)

    # Layer-Mod: 0x5000 - 0x51FF
    if 0x5000 <= keycode <= 0x51FF:
        return get_layer_mod_keycode(keycode)

    # TO: 0x5200 - 0x521F
    if 0x5200 <= keycode <= 0x521F:
        return get_to_keycode(keycode)

    # MO: 0x5220 - 0x523F
    if 0x5220 <= keycode <= 0x523F:
        return get_mo_keycode(keycode)

    # DF: 0x5240 - 0x525F
    if 0x5240 <= keycode <= 0x525F:
        return get_df_keycode(keycode)

    # TG: 0x5260 - 0x527F
    if 0x5260 <= keycode <= 0x527F:
        return get_tg_keycode(keycode)

    # OSL: 0x5280 - 0x529F
    if 0x5280 <= keycode <= 0x529F:
        return get_osl_keycode(keycode)

    # OSM: 0x52A0 - 0x52BF
    if 0x52A0 <= keycode <= 0x52BF:
        return get_osm_keycode(keycode)

    # TT: 0x52C0 - 0x52DF
    if 0x52C0 <= keycode <= 0x52DF:
        return get_tt_keycode(keycode)

    # PDF: 0x52E0 - 0x52FF
    if 0x52E0 <= keycode <= 0x52FF:
        return get_pdf_keycode(keycode)

    # Swap Hands: 0x5600 - 0x56FF
    if 0x5600 <= keycode <= 0x56FF:
        return get_swap_hands_keycode(keycode)

    # Tap Dance: 0x5700 - 0x57FF
    if 0x5700 <= keycode <= 0x57FF:
        return get_tap_dance_keycode(keycode)

    # Macro: 0x7700 - 0x777F
    if 0x7700 <= keycode <= 0x777F:
        return get_macro_keycode(keycode)

    # User: 0x7E00 - 0x7E3F
    if 0x7E00 <= keycode <= 0x7E3F:
        return get_user_keycode(keycode)

    # Unknown - return hex
    return f"0x{keycode:04X}"


def shorten_keycode_name(name: str, max_len: int = 8) -> str:
    """Shorten a keycode name for display.

    Args:
        name: Full keycode name
        max_len: Maximum length

    Returns:
        Shortened name
    """
    if len(name) <= max_len:
        return name

    # Common abbreviations
    abbreviations = {
        "KC_": "",
        "LEFT_": "L",
        "RIGHT_": "R",
        "BACKSPACE": "BSPC",
        "DELETE": "DEL",
        "ESCAPE": "ESC",
        "ENTER": "ENT",
        "SPACE": "SPC",
        "SHIFT": "SFT",
        "CONTROL": "CTL",
        "GUI": "WIN",
        "ALT": "ALT",
        "BRACKET": "BRC",
        "SEMICOLON": "SCLN",
        "QUOTE": "QUOT",
        "GRAVE": "GRV",
        "COMMA": "COMM",
        "SLASH": "SLSH",
        "BACKSLASH": "BSLS",
        "NONUS": "NU",
        "CAPS_LOCK": "CAPS",
        "SCROLL_LOCK": "SLCK",
        "PRINT_SCREEN": "PSCR",
        "PAGE_UP": "PGUP",
        "PAGE_DOWN": "PGDN",
        "INSERT": "INS",
        "APPLICATION": "APP",
        "TRANSPARENT": "TRNS",
        "VOLUME_UP": "VOLU",
        "VOLUME_DOWN": "VOLD",
        "MUTE": "MUTE",
    }

    result = name
    for full, short in abbreviations.items():
        result = result.replace(full, short)

    if len(result) <= max_len:
        return result

    # Still too long - truncate
    return result[: max_len - 1] + "…"
