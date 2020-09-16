from netpyne import specs, sim
from neuron import h
# Network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters


## Cell types
PYRcell = {'secs': {}}

PYRcell['secs']['soma'] = {'geom': {}, 'mechs': {}}
PYRcell['secs']['soma']['geom'] = {'diam': 18.8, 'L': 18.8, 'Ra': 123.0}
PYRcell['secs']['soma']['mechs']['hh'] = {'gnabar': 0.12, 'gkbar': 0.036, 'gl': 0.003, 'el': -70}

PYRcell['secs']['dend'] = {'geom': {}, 'topol': {}, 'mechs': {}}
PYRcell['secs']['dend']['geom'] = {'diam': 5.0, 'L': 150.0, 'Ra': 150.0, 'cm': 1}
PYRcell['secs']['dend']['topol'] = {'parentSec': 'soma', 'parentX': 1.0, 'childX': 0}
PYRcell['secs']['dend']['mechs']['pas'] = {'g': 0.0000357, 'e': -70}
PYRcell['secs']['dend']['mechs']['hh'] = {'gnabar': 0.12,'gkbar': 0.036, 'gl': 0.003, 'el': -70}      # soma hh mechanisms

# pass function as string for setting mechanisms. For example, distribute channels along a dendriteself.
# example functtostr : {"gnabar":"05.-distanceToSoma*0.9"}
# def _getDistanceString(distanceString, seg):
#     '''
#         Function: Determines neuron version of distance string specified for mech distribution
#         Input: seg -
#         function as tring for distribution of channels
#         Output: none
#     '''
#
#     # parentSec =
#     if distanceString == 'pathDistanceFromSoma'):
#         h.distance()
#         strFunc.replace('pathDistanceFromSoma', _getDistanceString('pathDistanceFromSoma', seg) )
#
#     elif strFunc.find('euclideanDistanceFromSoma') != -1:
#         strFunc.replace('euclideanDistanceFromSoma', _getDistanceString('euclideanDistanceFromSoma', seg) )
#
#     elif strFunc.find('pathDistanceFromBranchStart') != -1:
#         strFunc.replace('pathDistanceFromBranchStart', _getDistanceString('pathDistanceFromBranchStart', seg) )
#
#     elif strFunc.find('euclideanDistanceFromBranchStart') != -1:
#         strFunc.replace('euclideanDistanceFromBranchStart', _getDistanceString('euclideanDistanceFromBranchStart', seg) )
#
# # pass function as string for setting mechanisms. For example, distribute channels along a dendriteself.
# # example functtostr : {"gnabar":"05.-distanceToSoma*0.9"}
# def _mechStrToFunc(seg, mech, nseg, strVars, strFunc):
#     '''
#         Function: Distribute channels in section as per string function
#         Input: seg -
#         function as tring for distribution of channels
#         Output: none
#     '''
#     # pathDistFromSoma , realDistFromSoma , pathDistFromBranchStart , pathDistFromTrunk
#     # dend = sim.net.cells[0].secs['dend']['hObj']
#     # soma = sim.net.cells[0].secs['soma']['hObj']
#     mech = 'gnabar'
#     sec = 'dend'
#     nseg = 3
#
#     sec = sim.net.cells[0].secs[secLabel]['hObj']
#     seg.nseg = nseg
#
#     soma = sim.net.cells[0].secs['soma']['hObj']
#
#     parentSec = h.SectionRef(sec=seg).parent
#     mechDistribution = seg.psection()['density_mechs']['hh'][mech]
#
#     segDistances = [ h.distance(seg) for seg in dend]

dend.nseg = 3
mechDistribution = dend.psection()['density_mechs']['hh'][mech]
# distance from trunk
h.distance()
#0.0
h.distance([seg for seg in parentSec][0])
# 9.4
print( " segments in dendrite " + str([seg for seg in dend]) )
#[compartCell0.dend(0.166667), compartCell0.dend(0.5), compartCell0.dend(0.833333)]
print( " distances for segments in dendrite " + str([h.distance(seg) for seg in dend]))
#[43.8, 93.8, 143.8]
# exponential distribution
strFunc = 'a+b*np.exp(-dist/100)'
strVars = ['a','b','dist']
lambdaStr = 'lambda ' + ','.join(strVars) +': ' + strFunc
lambdaFunc = eval(lambdaStr)
print( " applying exponential lambda function " + str([lambdaFunc(3,4, h.distance(seg)) for seg in dend]) )
#[5.581303131429179, 4.565639491224026, 3.94960835348426]
# linear distribution
strFunc = 'a-b*dist'
lambdaStr = 'lambda ' + ','.join(strVars) +': ' + strFunc
lambdaFunc = eval(lambdaStr)
print( " applying linear lambda function " + str([lambdaFunc(3,4, h.distance(seg)) for seg in dend]) )
#[-172.2, -372.2, -572.2]
# distance from soma
h.distance([seg for seg in soma][0])
#9.4


    # strFunc = 'a + b*(np.exp(-distanceFromSoma))'
    # strFunc = 'a + b*(np.exp(-2*h.distance()))'

    if strFunc.find('pathDistanceFromSoma') != -1:
        strFunc.replace('pathDistanceFromSoma', _getDistanceString('pathDistanceFromSoma', seg) )

    elif strFunc.find('euclideanDistanceFromSoma') != -1:
        strFunc.replace('euclideanDistanceFromSoma', _getDistanceString('euclideanDistanceFromSoma', seg) )

    elif strFunc.find('pathDistanceFromBranchStart') != -1:
        strFunc.replace('pathDistanceFromBranchStart', _getDistanceString('pathDistanceFromBranchStart', seg) )

    elif strFunc.find('euclideanDistanceFromBranchStart') != -1:
        strFunc.replace('euclideanDistanceFromBranchStart', _getDistanceString('euclideanDistanceFromBranchStart', seg) )

    lambdaStr = 'lambda ' + ','.join(strVars) +': ' + strFunc # convert to lambda function
    lambdaFunc = eval(lambdaStr)

    evaluatedMech = lambdaFunc(strVars)

netParams.cellParams['PYR'] = PYRcell

## Population parameters
netParams.popParams['S'] = {'cellType': 'PYR', 'numCells': 1}
# netParams.popParams['M'] = {'cellType': 'PYR', 'numCells': 1}


## Synaptic mechanism parameters
netParams.synMechParams['exc'] = {'mod': 'Exp2Syn', 'tau1': 1.0, 'tau2': 5.0, 'e': 0}  # excitatory synaptic mechanism

# Stimulation parameters
netParams.stimSourceParams['bkg'] = {'type': 'NetStim', 'rate': 10, 'noise': 0.5}
netParams.stimTargetParams['bkg->PYR'] = {'source': 'bkg', 'conds': {'cellType': 'PYR'}, 'weight': 0.01, 'delay': 5, 'synMech': 'exc'}

#
# ## Cell connectivity rules
# netParams.connParams['S->M'] = {'preConds': {'pop': 'S'}, 'postConds': {'pop': 'M'},  #  S -> M
#     'probability': 0.5,         # probability of connection
#     'weight': 0.01,             # synaptic weight
#     'delay': 5,                 # transmission delay (ms)
#     'sec': 'dend',              # section to connect to
#     'loc': 1.0,                 # location of synapse
#     'synMech': 'exc'}           # target synaptic mechanism


# Simulation options
simConfig = specs.SimConfig()       # object of class SimConfig to store simulation configuration

simConfig.duration = 1*1e3          # Duration of the simulation, in ms
simConfig.dt = 0.025                # Internal integration timestep to use
simConfig.verbose = False           # Show detailed messages
simConfig.recordTraces = {'V_soma':{'sec':'soma','loc':0.5,'var':'v'}}  # Dict with traces to record
simConfig.recordStep = 1            # Step size in ms to save data (eg. V traces, LFP, etc)
simConfig.filename = 'tut3'         # Set file output name
simConfig.savePickle = False        # Save params, network and sim output to pickle file

simConfig.analysis['plotRaster'] = {'saveFig': True}                  # Plot a raster
simConfig.analysis['plotTraces'] = {'include': [1], 'saveFig': True}  # Plot recorded traces for this list of cells
simConfig.analysis['plot2Dnet'] = {'saveFig': True}                   # plot 2D cell positions and connections


# Create network and run simulation
sim.createSimulateAnalyze(netParams = netParams, simConfig = simConfig)

dend = sim.net.cells[0].secs.dend.hObj
dend.psection()
dend.nseg = 3
dend.psection()

# import pylab; pylab.show()  # this line is only necessary in certain systems where figures appear empty

# check model output
# sim.checkOutput('tut3')
import numpy as np

dend = sim.net.cells[0].secs['dend']['hObj']
soma = sim.net.cells[0].secs['soma']['hObj']

parentSec = h.SectionRef(sec=dend).parent # soma
dend.nseg = 3
mech = 'gnabar'
mechDistribution = dend.psection()['density_mechs']['hh'][mech]
# distance from trunk
h.distance()
#0.0
h.distance([seg for seg in parentSec][0])
# 9.4
print( " segments in dendrite " + str([seg for seg in dend]) )
#[compartCell0.dend(0.166667), compartCell0.dend(0.5), compartCell0.dend(0.833333)]
print( " distances for segments in dendrite " + str([h.distance(seg) for seg in dend]))
#[43.8, 93.8, 143.8]
# exponential distribution
strFunc = 'a+b*np.exp(-dist/100)'
strVars = ['a','b','dist']
lambdaStr = 'lambda ' + ','.join(strVars) +': ' + strFunc
lambdaFunc = eval(lambdaStr)
print( " applying exponential lambda function " + str([lambdaFunc(3,4, h.distance(seg)) for seg in dend]) )
#[5.581303131429179, 4.565639491224026, 3.94960835348426]
# linear distribution
strFunc = 'a-b*dist'
lambdaStr = 'lambda ' + ','.join(strVars) +': ' + strFunc
lambdaFunc = eval(lambdaStr)
print( " applying linear lambda function " + str([lambdaFunc(3,4, h.distance(seg)) for seg in dend]) )
#[-172.2, -372.2, -572.2]
# distance from soma
h.distance([seg for seg in soma][0])
#9.4
