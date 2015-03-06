SLOTS = xrange(32)

# [Configurable] Specific machines to track, with their slot number
_MILL_1 = 5
_MILL_2 = 4
_MILL_3 = 3
_LATHE_1 = 2
_LATHE_2 = 1
_LATHE_3 = 31
_LATHE_4 = 30
# _WOOD_LATHE_1 = 8
# _WOOD_LATHE_2 = 9
# _WOOD_LATHE_3 = 10
# _CNC_LATHE = 11
_SPECIFIC_MACHINE_TO_SLOT_MAP = { 'Mill 1': _MILL_1,
                        'Mill 2': _MILL_2,
                        'Mill 3': _MILL_3,
                        'Lathe 1': _LATHE_1,
                        'Lathe 2': _LATHE_2,
                        'Lathe 3': _LATHE_3,
                        'Lathe 4': _LATHE_4}
                        # 'Wood Lathe 1': _WOOD_LATHE_1,
                        # 'Wood Lathe 2': _WOOD_LATHE_2,
                        # 'Wood Lathe 3': _WOOD_LATHE_3,
                        # 'CNC Lathe': _CNC_LATHE
                        # }

# [Configurable] Lists of slots for each shop
_MAIN_SHOP_SLOTS = [1, 2, 3, 4, 5, 27, 28, 29, 30, 31]
_WOOD_SHOP_SLOTS = [6, 7, 8, 9, 10, 22, 23, 24, 25, 26]
_SHEET_METAL_SHOP_SLOTS = [11, 12, 13, 14, 15, 17, 18, 19, 20, 21]

# Mapping from slot to machine - constructed based on previous data
_SLOT_TO_MACHINE_MAP = {}
# Add the specific machines to the map
for m in _SPECIFIC_MACHINE_TO_SLOT_MAP:
    _SLOT_TO_MACHINE_MAP[_SPECIFIC_MACHINE_TO_SLOT_MAP[m]] = m

# Fill in the default Machines
_MAIN = 1
_WOOD = 1
_SHEET = 1
for i in SLOTS:
    if i not in _SLOT_TO_MACHINE_MAP:
        if i in _MAIN_SHOP_SLOTS:
            _SLOT_TO_MACHINE_MAP[i] = 'Main %d' % _MAIN
            _MAIN += 1
        elif i in _WOOD_SHOP_SLOTS:
            _SLOT_TO_MACHINE_MAP[i] = 'Wood %d' % _WOOD
            _WOOD += 1
        elif i in _SHEET_METAL_SHOP_SLOTS:
            _SLOT_TO_MACHINE_MAP[i] = 'Sheet %d' % _SHEET
            _SHEET += 1
        else:
            _SLOT_TO_MACHINE_MAP[i] = 'N/A'

def get_machine_name(slot):
    return _SLOT_TO_MACHINE_MAP[slot]


def is_in_wood_shop(slot):
    return slot in _WOOD_SHOP_SLOTS


def is_in_sheet_metal_shop(slot):
    return slot in _SHEET_METAL_SHOP_SLOTS


def is_in_main_shop(slot):
    return slot in _MAIN_SHOP_SLOTS


def which_sub_shop(slot):
    if is_in_main_shop(slot):
        return 'main'
    elif is_in_sheet_metal_shop(slot):
        return 'sheet'
    elif is_in_wood_shop(slot):
        return 'wood'
    else:
        return None

def is_specific_machine(slot):
    return slot in _SPECIFIC_MACHINE_TO_SLOT_MAP.viewvalues()

