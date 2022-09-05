import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
import os
import sys

def set_OBJ_global(*args):
    if len(cmds.ls(sl=True, sn=True, r=True)) ==1:
        obj = (cmds.ls(sl=True, sn=True, r=True))[0]
        cmds.optionVar(sv=('obj', obj))

        if len(cmds.ls('*|'+obj+'_vibrating_grp')) ==1:
            vibr_grp = str(cmds.ls('*|'+obj+'_vibrating_grp')[0])
            cmds.optionVar(sv=('vibr_grp', vibr_grp))
            print ("vibrating group set to [ %s ] "%(vibr_grp))
        else:
            print ("Can't find vibrating group!")


        if len(cmds.ls('*|'+obj+'_parent_grp')) ==1:
            parent_grp = str(cmds.ls('*|'+obj+'_parent_grp')[0])
            cmds.optionVar(sv=('parent_grp', parent_grp))
            print ("parent group set to [ %s ] "%(parent_grp))
        else:
            print ("Can't find parent group!")

        print ("OBJ IS NOW SET TO  [ %s ] "%(obj))
        msg = "%s"%(obj)
        cmds.inViewMessage( amg='Now we are working on <hl>'+msg+'</hl>', pos='midCenterTop', fade=True)

    else:
        sys.exit('You must select one object!')



def bake_sim(*args):

    all_values = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
    range_min = pm.playbackOptions(q=True, min=True)
    range_max = pm.playbackOptions(q=True, max=True)

    if len(cmds.ls(selection=True)) > 0:
        selected_objs = cmds.ls(selection=True)
        for obj in selected_objs:

            this_grp = str(cmds.ls('*|'+obj+'_vibrating_grp')[0])

            cmds.deleteAttr( '%s.translate_STRENGTH'%(this_grp) )
            cmds.deleteAttr( '%s.translate_DENSITY'%(this_grp) )
            cmds.deleteAttr( '%s.rotate_STRENGTH'%(this_grp) )
            cmds.deleteAttr( '%s.rotate_DENSITY'%(this_grp) )
            cmds.deleteAttr( '%s.scale_STRENGTH'%(this_grp) )
            cmds.deleteAttr( '%s.scale_DENSITY'%(this_grp) )

            cmds.bakeResults(this_grp, time=(range_min,range_max), sb=1, at=all_values, simulation=True)
            print ("BAKED VALUES OF [ %s ] ON ATTRIBUTES: %s IN RANGE: %s -> %s "%(this_grp, all_values, range_min, range_max))
    else:

        if cmds.optionVar( exists='vibr_grp' ) == 1:
            this_grp = cmds.optionVar( q='vibr_grp' )
        else:
            this_grp = (cmds.ls(sl=True, sn=True, r=True))[0]


        cmds.deleteAttr( '%s.translate_STRENGTH'%(this_grp) )
        cmds.deleteAttr( '%s.translate_DENSITY'%(this_grp) )
        cmds.deleteAttr( '%s.rotate_STRENGTH'%(this_grp) )
        cmds.deleteAttr( '%s.rotate_DENSITY'%(this_grp) )
        cmds.deleteAttr( '%s.scale_STRENGTH'%(this_grp) )
        cmds.deleteAttr( '%s.scale_DENSITY'%(this_grp) )

        cmds.bakeResults(this_grp, time=(range_min,range_max), sb=1, at=all_values, simulation=True)
        print ("BAKED VALUES OF [ %s ] ON ATTRIBUTES: %s IN RANGE: %s -> %s "%(this_grp, all_values, range_min, range_max))
    


def make_grp(*args):

    obj = cmds.optionVar( q='obj' )

    if str(cmds.listRelatives(obj, allParents=True)) == "[u'%s_vibrating_grp']"%(obj):
        cmds.parent(obj, world=True )
        pm.delete(obj+'_parent_grp')    
        
    # parent_grp = cmds.group( em=True, name=obj+'_parent_grp' )
    vibr_grp = pm.group( obj, n=obj+'_vibrating_grp')
    vibr_grp = str(cmds.ls('*|'+obj+'_vibrating_grp')[0])
    parent_grp = cmds.group( vibr_grp, name=obj+'_parent_grp' )
    parent_grp = str(cmds.ls('*|'+obj+'_parent_grp')[0])

    cmds.optionVar(sv=('vibr_grp', vibr_grp))
    cmds.optionVar(sv=('parent_grp', parent_grp))

    # cmds.select(vibr_grp)
    # mel.eval('CenterPivot;')
    # mel.eval('BakeCustomPivot;')
    # cmds.select( clear=True )

    cmds.addAttr(vibr_grp, ln ="translate_STRENGTH", at="float", dv=1, k=True)
    cmds.addAttr(vibr_grp, ln ="translate_DENSITY", at="float", dv=0.1, k=True)
    cmds.addAttr(vibr_grp, ln ="rotate_STRENGTH", at="float", dv=36, k=True)
    cmds.addAttr(vibr_grp, ln ="rotate_DENSITY", at="float", dv=0.1, k=True)
    cmds.addAttr(vibr_grp, ln ="scale_STRENGTH", at="float", dv=1, k=True)
    cmds.addAttr(vibr_grp, ln ="scale_DENSITY", at="float", dv=0.1, k=True)


def usun_expr(*args):
    
    this_obj = (pm.ls(sl=True, sn=True))[0]
    pm.select (this_obj, replace=1)
    pm.delete (expressions=1)



    for attrib in values:
        if cmds.connectionInfo( '%s.%s'%(this_obj,attrib), isDestination=True) == 0:
            pm.setAttr( '%s.%s'%(this_obj, attrib), 0)
            pm.setAttr( '%s.%s'%(this_obj, attrib), 0)
    pm.select (clear=True)
    
def update_variables(*args):
    
    if len(cmds.ls(selection=True)) ==1:
        obj = (cmds.ls(sl=True, sn=True, r=True))[0]

        cmds.optionVar(sv=('obj', obj))

    # # set_OBJ_global()    
    # print "set obj =  %s"%(obj)

    Attrib_list = []
    txCheck = cmds.checkBox('txAxisBox', query=True, value=True)
    tyCheck = cmds.checkBox('tyAxisBox', query=True, value=True)
    tzCheck = cmds.checkBox('tzAxisBox', query=True, value=True)
    rxCheck = cmds.checkBox('rxAxisBox', query=True, value=True)
    ryCheck = cmds.checkBox('ryAxisBox', query=True, value=True)
    rzCheck = cmds.checkBox('rzAxisBox', query=True, value=True)
    sxCheck = cmds.checkBox('sxAxisBox', query=True, value=True)
    syCheck = cmds.checkBox('syAxisBox', query=True, value=True)
    szCheck = cmds.checkBox('szAxisBox', query=True, value=True)
    if txCheck == 1: Attrib_list.append('tx')
    if tyCheck == 1: Attrib_list.append('ty')
    if tzCheck == 1: Attrib_list.append('tz')
    if rxCheck == 1: Attrib_list.append('rx')
    if ryCheck == 1: Attrib_list.append('ry')
    if rzCheck == 1: Attrib_list.append('rz')
    if sxCheck == 1: Attrib_list.append('sx')
    if syCheck == 1: Attrib_list.append('sy')
    if szCheck == 1: Attrib_list.append('sz')
    # print Attrib_list
    global values
    values = Attrib_list
    
    # print values
    # print "koniec update variables"


def motion_trail(*args):
    # print "motion trail function"
    if len(cmds.ls(selection=True)) >0:
        selected_objs = cmds.ls( selection=True)
        for s_obj in selected_objs:
            cmds.optionVar(sv=('obj', s_obj))
            if len(pm.ls(s_obj+"_noise_motion_trailHandle"))==1:
                cmds.delete(s_obj+"_noise_motion_trailHandle")

            elif len(pm.ls(s_obj+"_noise_motion_trailHandle"))==0:
                refresh()
    else:
        obj=cmds.optionVar( q='obj' )

        if len(pm.ls(obj+"_noise_motion_trailHandle"))==1:
            cmds.delete(obj+"_noise_motion_trailHandle")

        elif len(pm.ls(obj+"_noise_motion_trailHandle"))==0:
            refresh()



def refresh(*args):
    # print "refresh function"
    obj=cmds.optionVar( q='obj' )
    vibr_grp = obj+"_vibrating_grp"
    # parent_grp = cmds.optionVar( q='parent_grp' )
 

    if len(pm.ls(obj+"_noise_motion_trailHandle"))==1:
        cmds.select(obj)
        mel.eval('UpdateSnapshot;')
        # print "updated motion trail"
        # cmds.select(vibr_grp)
    else:
        range_min = pm.playbackOptions(q=True, min=True)
        range_max = pm.playbackOptions(q=True, max=True)
        noise_motion_trail=cmds.snapshot(obj, name=obj+"_noise_motion_trail", mt=True, startTime=range_min, endTime=range_max, increment=1 )
        # cmds.parent(obj+"_noise_motion_trailHandle",parent_grp)

    mel.eval('animCurveEditor -edit -resultScreenSamples 0 -resultSamples 1 -resultUpdate delayed -showResults true graphEditor1GraphEd;')

def center_pivots(*args):

    obj=cmds.optionVar( q='obj' )
    vibr_grp = str(cmds.ls('*|'+obj+'_vibrating_grp')[0])
    parent_grp = str(cmds.ls('*|'+obj+'_parent_grp')[0])

    cmds.select(vibr_grp)
    mel.eval('CenterPivot;')
    cmds.select(parent_grp)
    mel.eval('CenterPivot;')
    cmds.select(clear=True)

def move_anim(*args):
    # print "move anim"
    obj=cmds.optionVar( q='obj' )
    vibr_grp = str(cmds.ls('*|'+obj+'_vibrating_grp')[0])
    parent_grp = str(cmds.ls('*|'+obj+'_parent_grp')[0])
    # print obj, vibr_grp, parent_grp

    cmds.select(obj)
    lastKeyframe = cmds.findKeyframe(which='last')
    firstKeyframe = cmds.findKeyframe(which='first')
    # print "cut key zaraz"

    keyframe_count = cmds.keyframe(obj,query=True,kc=True)

    cmds.cutKey(obj, time=(firstKeyframe,lastKeyframe))
    # print "zerowanie"
    for eachAttr in values:### Loop of attributes
        try:
            if eachAttr.startswith('s')==True:
                cmds.setAttr( obj + "." + eachAttr, 1);
            else:
                cmds.setAttr( obj + "." + eachAttr, 0);
        except:
            print ('%s %s is locked')%(obj, eachAttr)
    # print "center pivots zaraz"
    center_pivots()
    # print "paste keys"
    
    if keyframe_count !=0:
        cmds.pasteKey( parent_grp)
        warning_msg = "from %s were transferred to %s_parent_grp"%(obj,obj)
        cmds.inViewMessage( amg='<hl>Animation keys</hl> '+warning_msg, pos='midCenter', fade=True)
    else:
        "no keyframes found!"
    
    



def make_expr(*args):
    if len(pm.ls( selection=True)) > 1:
        question1 = cmds.confirmDialog( title='Just to make sure...',
                                message='You selected more than one object. Do you want to apply noise on all of those objects?',
                                button=['Yeah, perform noise on multiple objects','No, let me select again'],
                                defaultButton='oh, no, let me select again',)
        if question1 == 'Yeah, perform noise on multiple objects':
            multiple_noiser()
        elif question1 == 'oh, no, let me select again':
            sys.exit('remember to select ONE object then')
        else:
            print ("ok")
    elif len(pm.ls( selection=True)) == 0:
        sys.exit('What do you want to apply noise on?')

    obj = cmds.optionVar( q='obj' )

    update_variables()

    make_grp()

    # number_of_keyframes = cmds.keyframe(obj,query=True,kc=True)
    move_anim()

    
    vibr_grp = cmds.optionVar( q='vibr_grp' )
    parent_grp = cmds.optionVar( q='parent_grp' )
    scaleOffset = cmds.optionVar( fv=('scaleOffset', cmds.floatField(so, q=True, value=True)))
    GS_command()
    
    # print values
    

    list_con = cmds.listConnections(vibr_grp, s=True, scn=True) or []
    # print "list con"
    if not list_con:
        pass
    else:
        usun_expr()
    # ------------------------
    
    # STRENGTH_VALUE = cmds.getAttr('%s.translate_STRENGTH'%(vibr_grp))
    # TIME_STRETCH_VALUE = cmds.getAttr('%s.translate_DENSITY'%(vibr_grp))
    # print "robienie expr"
    for attr in values:
        noise_multiply = mel.eval('rand -100 100;')
        offset = 0
        GLOBAL_SCALE = 1
        # print "po GLOBAL SCALE"
        if attr.startswith('r')==True:
            multiplier = 36
            STRENGTH_NODE = vibr_grp+'.rotate_STRENGTH'
            TIME_STRETCH_NODE = vibr_grp+'.rotate_DENSITY'
            # print "startswith r"
            
        elif attr.startswith('t')==True:
            multiplier = 1
            STRENGTH_NODE = vibr_grp+'.translate_STRENGTH'
            TIME_STRETCH_NODE = vibr_grp+'.translate_DENSITY'
            GLOBAL_SCALE = cmds.optionVar( q='GLOBAL_SCALE' )
            # print "startswith t"

        elif attr.startswith('s')==True:
            multiplier = 1
            STRENGTH_NODE = vibr_grp+'.scale_STRENGTH'
            TIME_STRETCH_NODE = vibr_grp+'.scale_DENSITY'
            offset = cmds.optionVar( q='scaleOffset' )
            # print "startswith s"
        else:
            print ("no attributes!")
        


        cmds.select(vibr_grp)
        expression_string = '%s = ((noise((frame+(%s*%s))*%s)*%s)*%s)+%s' % (attr, noise_multiply, STRENGTH_NODE, TIME_STRETCH_NODE, STRENGTH_NODE, GLOBAL_SCALE, offset)
        # print '%s = ((noise((frame+(%s*%s))*%s)*%s)*%s)+%s' % (attr, noise_multiply, STRENGTH_NODE, TIME_STRETCH_NODE, STRENGTH_NODE, GLOBAL_SCALE, offset)
        pm.expression( o=vibr_grp, s=expression_string)
    print ("CREATED NOISE ON THIS OBJECT : [ %s ] FOR THOSE ATTRIBUTES: %s"%(vibr_grp, values))

    mel.eval('animCurveEditor -edit -resultScreenSamples 0 -resultSamples 1 -resultUpdate delayed -showResults true graphEditor1GraphEd;')

def open_micro_tweaker(*args):

    if (cmds.window("micro_tweaker_win", exists=True)):
        cmds.deleteUI("micro_tweaker_win")

    if len(pm.ls(selection=True)) > 1:
        selected_objs = cmds.ls(selection=True)
        cmds.select(clear=True)
        for objs in selected_objs:
            cmds.select(objs+"_vibrating_grp", add=True)
    else:
        GLOBAL_SCALE = cmds.optionVar( q='GLOBAL_SCALE' )
        vibr_grp = cmds.optionVar( q='vibr_grp' )
        try:
            micro_tweaker_win = cmds.window("micro_tweaker_win", title='Micro Tweaker' )
            cmds.columnLayout()

            cmds.attrFieldSliderGrp('ts', label='Translate STRENGTH', minValue=0.0001, maxValue=100000, fieldMinValue=0.0001, fieldMaxValue=GLOBAL_SCALE*5, at='%s.translate_STRENGTH' %(vibr_grp), cc=refresh, bgc=[0.23,0.23,0.2], w=500 )
            cmds.attrFieldSliderGrp('td', label='Translate DENSITY', minValue=0.0001, maxValue=100000, fieldMinValue=0.0001, fieldMaxValue=GLOBAL_SCALE*0.5, at='%s.translate_DENSITY' %(vibr_grp), cc=refresh, bgc=[0.25,0.25,0.21], w=500  )
            cmds.attrFieldSliderGrp('rs', label='Rotate STRENGTH', minValue=0.0001, maxValue=360000, fieldMinValue=0.0001, fieldMaxValue=100, at='%s.rotate_STRENGTH' %(vibr_grp), cc=refresh, bgc=[0.23,0.2,0.2], w=500  )
            cmds.attrFieldSliderGrp('rd', label='Rotate DENSITY', minValue=0.0001, maxValue=100000, fieldMinValue=0.0001, fieldMaxValue=0.5, at='%s.rotate_DENSITY' %(vibr_grp), cc=refresh, bgc=[0.26,0.22,0.22], w=500  )
            cmds.attrFieldSliderGrp('ss', label='Scale STRENGTH', minValue=0.0001, maxValue=100000, fieldMinValue=0.0001, fieldMaxValue=5, at='%s.scale_STRENGTH' %(vibr_grp), cc=refresh, bgc=[0.18,0.2,0.2], w=500  )
            cmds.attrFieldSliderGrp('sd', label='Scale DENSITY', minValue=0.0001, maxValue=10000, fieldMinValue=0.0001, fieldMaxValue=0.5, at='%s.scale_DENSITY' %(vibr_grp), cc=refresh, bgc=[0.18,0.22,0.22], w=500  )
            cmds.showWindow( micro_tweaker_win )
        except RuntimeError:
             pass

def so_command(*args):
    field = cmds.floatField(so, q=True, value=True)
    cmds.optionVar( fv=('scaleOffset', field))

def GS_command(*args):
    field = cmds.floatField(GLOBAL_SCALE, q=True, value=True)
    cmds.optionVar( fv=('GLOBAL_SCALE', field))


def multiple_noiser(*args):
    list_of_selected_objs = cmds.ls( selection=True)
    for s_obj in list_of_selected_objs:
        cmds.select(clear=True)
        cmds.select(s_obj)
        make_expr()
        cmds.select(clear=True)
    print ("applied noise on every of selected objects!")
    # cmds.optionVar(iv=('multiple', 1))



scriptDir = cmds.internalVar(userScriptDir=True)
# print scriptDir
iconDyr = scriptDir+"Noise_Creator/icons/"

if (cmds.window("window_noise", exists=True)):
    cmds.deleteUI(window_noise)
        
window_noise = cmds.window("window_noise", title = "Noise Creator", widthHeight=(247, 174) )
cmds.frameLayout( label='choose attributes to make noise on:', labelAlign='center', cl=False, bgc= [0.22, 0.22, 0.22])
# cmds.rowColumnLayout( numberOfColumns=2)
cmds.rowColumnLayout( numberOfRows=3 )
tx = cmds.checkBox("txAxisBox", l="Translate X", v=True)
ty = cmds.checkBox("tyAxisBox", l="Translate Y", v=True)
tz = cmds.checkBox("tzAxisBox", l="Translate Z", v=True)
rx = cmds.checkBox("rxAxisBox", l="Rotate X", v=True)
ry = cmds.checkBox("ryAxisBox", l="Rotate Y", v=True)
rz = cmds.checkBox("rzAxisBox", l="Rotate Z", v=True)
sx = cmds.checkBox("sxAxisBox", l="Scale X", v=False)
sy = cmds.checkBox("syAxisBox", l="Scale Y", v=False)
sz = cmds.checkBox("szAxisBox", l="Scale Z", v=False)
cmds.text( label='Scale', bgc=[0.24,0.24,0.24])
cmds.text( label='Offset:', bgc=[0.24,0.24,0.24])
so = cmds.floatField("scaleOffset", value=1, ann="Base scale value", w=44, cc=so_command)

cmds.setParent( '..' )
cmds.rowColumnLayout( numberOfRows=1 )
cmds.text( label=' Set global scale of vibrations: ', bgc= [0.23, 0.18, 0.18])
GLOBAL_SCALE = cmds.floatField("GLOBAL_SCALE", value=1, ann="GLOBAL_SCALE", w=90, cc=GS_command, bgc= [0.23, 0.18, 0.18])
cmds.setParent( '..' )
cmds.setParent( '..' )
# cmds.symbolButton(  image=sciezka+"noise_make_icon3.jpg", command=make_expr)
# cmds.setParent( '..' )

cmds.setParent( '..' )
cmds.rowColumnLayout( numberOfColumns=3, cs=[10,10], rs=[4,4])
cmds.symbolButton(  image=iconDyr+"noise_make_icon4.jpg", command=make_expr)
bake_bt = cmds.symbolButton(image= iconDyr+"noise_bake_grp_icon2.jpg", command=bake_sim)
set_OBJ_global = cmds.symbolButton(image= iconDyr+"noise_set_obj_icon2.jpg", command=set_OBJ_global)
motion_trail_bt = cmds.symbolButton(image= iconDyr+"noise_motion_trail_icon.jpg", command=motion_trail)
update_mtrail_bt = cmds.symbolButton(image= iconDyr+"noise_motion_trail_refresh_icon2.jpg", command=refresh)
open_micro_tweaker = cmds.symbolButton(image= iconDyr+"noise_tweaker_icon.jpg", command=open_micro_tweaker)

cmds.showWindow(window_noise)
