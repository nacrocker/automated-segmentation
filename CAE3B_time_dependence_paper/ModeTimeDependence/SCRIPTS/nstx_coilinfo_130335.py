import numpy as np
def _():
    # Coil information for 130335.

    # HF Array (u/eric/nstx/mm/126a_hf.txt)
    names_HF = ['\\OPS_PC::bdot_l1dmivvhf1_raw','\\OPS_PC::bdot_l1dmivvhf2_raw','\\OPS_PC::bdot_l1dmivvhf4_raw','\\OPS_PC::bdot_l1dmivvhf5_raw','\\OPS_PC::bdot_l1dmivvhf9_raw','\\OPS_PC::bdot_l1dmivvhf11_raw']
    rel_areas_HF = np.array([1.0, -1.0, 1.0, 1.0, -1.0, -1.0])
    coil_pos_HF = np.array([330.0, 338.7, 351.5, 355.8, 158.7, 171.5])*np.pi/180 # (radias)

    # HN Array (u/eric/nstx/mm/2009a_hn.mm)
    names_HN = ['\\OPS_PC::bdot_l1dmivvhn3_raw','\\OPS_PC::bdot_l1dmivvhn2_raw', ' \\OPS_PC::bdot_l1dmivvhn1_raw','\\OPS_PC::bdot_l1dmivvhn16_raw','\\OPS_PC::bdot_l1dmivvhn15_raw',
                '\\OPS_PC::bdot_l1dmivvhn14_raw','\\OPS_PC::bdot_l1dmivvhn10_raw','\\OPS_PC::bdot_l1dmivvhn7_raw','\\OPS_PC::bdot_l1dmivvhn6_raw','\\OPS_PC::bdot_l1dmivvhn5_raw','\\OPS_PC::bdot_l1dmivvhn4_raw']
    rel_areas_HN = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])

    # Alternate (old?) coil angles from /u/eric/nstx/shark_2012.pro.
    coil_pos_HN_old = np.array([30, 50, 60, 155, 170, 180, 291, 300, 330, 350, 360])*np.pi/180
    # New coil angles
    coil_pos_HN_new = np.array([29.8, 49.9, 59.9, 160.0, 165.0, 170.0, 292.5, 302.8, 339.5, 344.8, 349.9])*np.pi/180

    # use the old coil positions (for now) because they give much lower chi-squared values.
    coil_pos_HN = coil_pos_HN_old
    return vars()
coilinfo_130335=_()
