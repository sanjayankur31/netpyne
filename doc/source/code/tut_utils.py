import numpy as np
import os, sys, traceback
import sim
from neuron import h

# apply method for distributing channels
def applyMethod(methodType, segment, mech, parameter= '', endValue= 0):
    ''' Input: methodtype- linear, exp, uniform, sigmoid
        Output:None
        Function: distribute channels as per methodType
    '''
    try:

        seg = sim.net.cells[0].secs[segment]['hObj']
        paramValues = seg.psection()['density_mechs']['hh'][mech]
        if methodType == "linear":
            seg.psection()['density_mechs']['hh'][mech] = [k - k/float(len(x)) * (i+1) for i, k in enumerate(paramValues) ]
        # elif methodType == "uniform":
        # elif methodType == "exp":
        # elif methodType == "sigmoid":

    except:
        traceback.print_exc(file=sys.stdout)
    return

joe  3:45 PM
So for example, instead of  gna: 0.5 , I want to be able to do gna: '0.5 - pathDistFromSoma / 150'

sidmitra  3:45 PM
ok will work on that

joe  3:46 PM
For variables pathDistFromSoma , realDistFromSoma , pathDistFromBranchStart , pathDistFromTrunk

# -----------------------------------------------------------------------------
# Convert connection param string to function
# -----------------------------------------------------------------------------
def _connStrToFunc(self, preCellsTags, postCellsTags, connParam):
    # list of params that have a function passed in as a string
    paramsStrFunc = [param for param in self.connStringFuncParams+['probability', 'convergence', 'divergence'] if param in connParam and isinstance(connParam[param], basestring)]

    # dict to store correspondence between string and actual variable
    dictVars = {}
    dictVars['pre_x']       = lambda preConds,postConds: preConds['x']
    dictVars['pre_y']       = lambda preConds,postConds: preConds['y']
    dictVars['pre_z']       = lambda preConds,postConds: preConds['z']
    dictVars['pre_xnorm']   = lambda preConds,postConds: preConds['xnorm']
    dictVars['pre_ynorm']   = lambda preConds,postConds: preConds['ynorm']
    dictVars['pre_znorm']   = lambda preConds,postConds: preConds['znorm']
    dictVars['post_x']      = lambda preConds,postConds: postConds['x']
    dictVars['post_y']      = lambda preConds,postConds: postConds['y']
    dictVars['post_z']      = lambda preConds,postConds: postConds['z']
    dictVars['post_xnorm']  = lambda preConds,postConds: postConds['xnorm']
    dictVars['post_ynorm']  = lambda preConds,postConds: postConds['ynorm']
    dictVars['post_znorm']  = lambda preConds,postConds: postConds['znorm']
    dictVars['dist_x']      = lambda preConds,postConds: abs(preConds['x'] - postConds['x'])
    dictVars['dist_y']      = lambda preConds,postConds: abs(preConds['y'] - postConds['y'])
    dictVars['dist_z']      = lambda preConds,postConds: abs(preConds['z'] - postConds['z'])
    dictVars['dist_3D']    = lambda preConds,postConds: np.sqrt((preConds['x'] - postConds['x'])**2 +
                            (preConds['y'] - postConds['y'])**2 +
                            (preConds['z'] - postConds['z'])**2)
    dictVars['dist_3D_border'] = lambda preConds,postConds: np.sqrt((abs(preConds['x'] - postConds['x']) - postConds['borderCorrect'][0])**2 +
                            (abs(preConds['y'] - postConds['y']) - postConds['borderCorrect'][1])**2 +
                            (abs(preConds['z'] - postConds['z']) - postConds['borderCorrect'][2])**2)
    dictVars['dist_2D']     = lambda preConds,postConds: np.sqrt((preConds['x'] - postConds['x'])**2 +
                            (preConds['z'] - postConds['z'])**2)
    dictVars['dist_xnorm']  = lambda preConds,postConds: abs(preConds['xnorm'] - postConds['xnorm'])
    dictVars['dist_ynorm']  = lambda preConds,postConds: abs(preConds['ynorm'] - postConds['ynorm'])
    dictVars['dist_znorm']  = lambda preConds,postConds: abs(preConds['znorm'] - postConds['znorm'])
    dictVars['dist_norm3D'] = lambda preConds,postConds: np.sqrt((preConds['xnorm'] - postConds['xnorm'])**2 +
                            np.sqrt(preConds['ynorm'] - postConds['ynorm']) +
                            np.sqrt(preConds['znorm'] - postConds['znorm']))
    dictVars['dist_norm2D'] = lambda preConds,postConds: np.sqrt((preConds['xnorm'] - postConds['xnorm'])**2 +
                            np.sqrt(preConds['znorm'] - postConds['znorm']))
    dictVars['rand'] = lambda unused1,unused2: self.rand

    # add netParams variables
    for k,v in self.params.__dict__.items():
        if isinstance(v, Number):
            dictVars[k] = v

    # for each parameter containing a function, calculate lambda function and arguments
    for paramStrFunc in paramsStrFunc:
        strFunc = connParam[paramStrFunc]  # string containing function
        for randmeth in self.stringFuncRandMethods: strFunc = strFunc.replace(randmeth, 'rand.'+randmeth) # append rand. to h.Random() methods
        strVars = [var for var in list(dictVars.keys()) if var in strFunc and var+'norm' not in strFunc]  # get list of variables used (eg. post_ynorm or dist_xyz)
        lambdaStr = 'lambda ' + ','.join(strVars) +': ' + strFunc # convert to lambda function
        lambdaFunc = eval(lambdaStr)

        if paramStrFunc in ['probability']:
            # replace function with dict of values derived from function (one per pre+post cell)
            connParam[paramStrFunc+'Func'] = {(preGid,postGid): lambdaFunc(
                **{strVar: dictVars[strVar] if isinstance(dictVars[strVar], Number) else dictVars[strVar](preCellTags, postCellTags) for strVar in strVars})
                for preGid,preCellTags in preCellsTags.items() for postGid,postCellTags in postCellsTags.items()}

        elif paramStrFunc in ['convergence']:
            # replace function with dict of values derived from function (one per post cell)
            connParam[paramStrFunc+'Func'] = {postGid: lambdaFunc(
                **{strVar: dictVars[strVar] if isinstance(dictVars[strVar], Number) else dictVars[strVar](None, postCellTags) for strVar in strVars})
                for postGid,postCellTags in postCellsTags.items()}

        elif paramStrFunc in ['divergence']:
            # replace function with dict of values derived from function (one per post cell)
            connParam[paramStrFunc+'Func'] = {preGid: lambdaFunc(
                **{strVar: dictVars[strVar] if isinstance(dictVars[strVar], Number) else dictVars[strVar](preCellTags, None) for strVar in strVars})
                for preGid, preCellTags in preCellsTags.items()}

        else:
            # store lambda function and func vars in connParam (for weight, delay and synsPerConn since only calculated for certain conns)
            connParam[paramStrFunc+'Func'] = lambdaFunc
            connParam[paramStrFunc+'FuncVars'] = {strVar: dictVars[strVar] for strVar in strVars}
