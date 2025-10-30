#!/usr/bin/env python
# coding: utf-8

defaultVars(
    shot = 141398,
    bdotarray='HN',
    bdotnames = ['\\OPS_PC::BDOT_L1DMIVVHN3_RAW', '\\OPS_PC::BDOT_L1DMIVVHN2_RAW', '\\OPS_PC::BDOT_L1DMIVVHN1_RAW', '\\OPS_PC::BDOT_L1DMIVVHN16_RAW', '\\OPS_PC::BDOT_L1DMIVVHN15_RAW', '\\OPS_PC::BDOT_L1DMIVVHN14_RAW', '\\OPS_PC::BDOT_L1DMIVVHN13_RAW', '\\OPS_PC::BDOT_L1DMIVVHN10_RAW', '\\OPS_PC::BDOT_L1DMIVVHN7_RAW', '\\OPS_PC::BDOT_L1DMIVVHN6_RAW', '\\OPS_PC::BDOT_L1DMIVVHN5_RAW', '\\OPS_PC::BDOT_L1DMIVVHN4_RAW'],
    bdottree = 'OPS_PC',
    device = 'NSTX'
)

server=device #won't work for all devices

shotsholder = root['OUTPUTS']
shotoutputs=shotsholder[shot]=OMFITtree('')
bdotoutputs=shotoutputs['bdot']=OMFITtree('')
arrayoutputs=bdotoutputs[bdotarray]=OMFITtree('')
data=arrayoutputs['data']=OMFITtree('')
for ib,bname in enumerate(bdotnames):
    data[ib] = OMFITmdsValue(server=server, shot=shot, TDI=bname, treename=bdottree)
