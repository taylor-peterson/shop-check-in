import shop
import sample_users
import slots

TEST_SHOP = shop.Shop()
TEST_SHOP.open_(sample_users.USER_POD)
TEST_SHOP.add_user_s_to_slot([sample_users.USER_CERTIFIED], slots._MILL_1)
TEST_SHOP.add_user_s_to_slot([sample_users.USER_CERTIFIED, sample_users.USER_CERTIFIED], slots._CNC_LATHE)
TEST_SHOP.add_user_s_to_slot([sample_users.USER_PROCTOR], slots._WOOD_LATHE_2)
TEST_SHOP.add_user_s_to_slot([sample_users.USER_PROCTOR], 30)
TEST_SHOP.change_pod(sample_users.USER_PROCTOR)

TEST_DICT = {'open': True,
        'pods': 'Alex Ozdemir, Jonpaul Littelton',
        'main':
            {'machines':
                 {'Mill 1': {'in_use': True,
                             'users': 'Veronica Rivera',
                             'start_time': 'Test Time'},
                  'Mill 2': {'in_use': True,
                             'users': 'Paul, Celeste',
                             'start_time': 'Test Time'},
                  'Mill 3': {'in_use': False,
                             'users': '',
                             'start_time': ''}
                 },
             'limbo':
                 ['Adam', 'Betsy', 'Cain']
            },
        'wood':
            {'machines':
                 {'Wood Lathe 1': {'in_use': False,
                                   'users': '',
                                   'start_time':''}
                 },
             'limbo':
                 ['David','Edward']
            },
        'sheet':
            {'machines':
                 {'CNC Lathe': {'in_use': False}},
             'limbo':
                 ['Faith','Gruver']}
}