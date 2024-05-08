# Numerical Input
# Author : Shinobu
# Description: using shortcut keys to numerically transform a selection based on selected tools, Inputting  unit values like -0.2mm to move a point 
# Import an example shortcut key set using the HotKey Editor.
'''
from NumericalInput import NumericalInput
nInput = NumericalInput.NumericalInput()
NumericalInput.openPrompt()
'''
#include <QtCore/QCoreApplication>
from maya import cmds
import maya.api.OpenMaya as oMaya
import math



class NumericalInput():

	@staticmethod
	def isValidContext():
		ctx = cmds.currentCtx()
		contx = cmds.contextInfo(ctx, c=True)
		if contx == "manipMove" or contx  == "manipRotate" or contx == "manipScale":
			return True
		return False


	@staticmethod
	def rotateQuat(axis,angles):
		quat = oMaya.MQuaternion()
		quat.setToXAxis(angles[0])
		quat.setToYAxis(angles[1])
		quat.setToZAxis(angles[2])
		return quat

	@staticmethod
	def coordinateSpace(kspace):
		wspace = False
		ospace = False
		lspace = False
		cspace = False	
		rspace = False			
		if kspace == 0:
			ospace = True
		if kspace == 1:
			lspace = True
		if kspace == 2:
			wspace = True
		if kspace == 3:
			rspace = True
		if kspace == 6:
			cspace = True
		return wspace , ospace , lspace , cspace ,rspace

	@staticmethod	
	def enteredvalue(*args):		
		# query the current context (current tool)		
		# derived from https://gist.github.com/yamahigashi/85d9743553cd41c4cb40
		if NumericalInput.isValidContext():
			values = args[0]	
			# remove white spaces
			values = values.strip()
			values = values.split(" ")					
			x,y,z = (0 , 0 , 0)
			v = values[0] # for single only entries
			if len(values) > 1:		
				x = values[0]					
				y = values[1]
				if len(values) > 2:
					z = values[2]			
			# more reliable for getting pivot rotations than manipContext
			orientation = cmds.manipPivot( q=True, o=True)
			orientation = orientation[0]			
			euler = oMaya.MEulerRotation(math.radians(orientation[0]) ,math.radians(orientation[1]),math.radians(orientation[2]))	
			
			
			if NumericalInput.contextname == "manipMove":
				axisindex = cmds.manipMoveContext( "Move", q=True, currentActiveHandle=True)	
				pinPivot = cmds.manipMoveContext( "Move", q=True, pin=True)
				wspace, ospace, lspace, cspace, rspace = NumericalInput.coordinateSpace(cmds.manipMoveContext( "Move", q=True, mode=True))								
				pivot = cmds.manipMoveContext( "Move", q=True, position=True)					
				if len(pivot) == 0:
					print("This tool doesn't work with the pivot gizmo press INSERT to exit Pivot Edit")
					return
				internalunit = cmds.currentUnit(q=True,fullName=True)				
				x = float(cmds.convertUnit(x,toUnit=internalunit))
				y = float(cmds.convertUnit(y,toUnit=internalunit))
				z = float(cmds.convertUnit(z,toUnit=internalunit))		
				v = float(cmds.convertUnit(v,toUnit=internalunit))		
				direction = oMaya.MVector( x,y,z )
				
				if len(values) == 1:
					# when there is only single value 
					direction = oMaya.MVector()
					if axisindex == 0: # X					
						direction.x = v										
					if axisindex == 1: # Y
						direction.y = v					
					if axisindex == 2: # Z
						direction.z = v				
				rotdirection = direction.rotateBy(euler)												
				if wspace == True or ospace == True or cspace == True or lspace == True: 
					if cspace == True:
						ws = True
						ls = True						
					cmds.move( rotdirection.x , rotdirection.y , rotdirection.z, r=True , ws=wspace, os=ospace )					
					
					if pinPivot == False:		
						pVector = oMaya.MVector(  float(pivot[0]),float(pivot[1]),float(pivot[2]))						
						if euler.x + euler.y + euler.z == 0:					
							# no change in pivot rotation don't try 
							pass							
						else:									
							newPin = pVector + rotdirection
							cmds.manipPivot( p=newPin)						
				else:
					print("Unsupported coordinate space. only World, Local and Object space is supported for this tool.")
				
			if NumericalInput.contextname == "manipRotate":
				axisindex = cmds.manipRotateContext( "Rotate", q=True, currentActiveHandle=True)									
				wspace, ospace, lspace, cspace , rspace = NumericalInput.coordinateSpace(cmds.manipRotateContext( "Rotate", q=True, mode=True))
				pivot = cmds.manipRotateContext( "Rotate", q=True, position=True)		
				if len(pivot) == 0:
					print("This tool doesn't work with the pivot gizmo press INSERT to exit Pivot Edit")
					return
				# get pivot manipulator
				
				x = float(x)
				y = float(y)
				z = float(z)	
				v = float(v)
				direction = oMaya.MVector( x,y,z )						
				orientation = [str(euler.x)+"rad",str(euler.y)+"rad",str(euler.z)+"rad"]							

				if len(values) == 1:					
					direction = oMaya.MVector()
					if axisindex == 0: # X					
						direction.x = v										
					if axisindex == 1: # Y
						direction.y = v					
					if axisindex == 2: # Z
						direction.z = v

				if wspace == True or ospace == True or rspace == True or lspace == True: 
					if rspace == True:
						#custom pivot detected
						ws = True
						ls = True
					if euler.x == euler.y == euler.z == 0:	
						# fixes a bug where no if the pivot isn't customized it would twist 
						cmds.rotate( direction.x, direction.y , direction.z , r=True,  p=pivot , ws=wspace, os=ospace )					
					else:
						cmds.rotate( direction.x, direction.y , direction.z , r=True,  p=pivot , ws=wspace, os=ospace , oa=orientation)										
				else:
					print("Unsupported coordinate space. only World, Local and Object space is supported for this tool.")

			if NumericalInput.contextname == "manipScale":
				axisindex = cmds.manipScaleContext( "Scale", q=True, currentActiveHandle=True)					
				# get pivot manipulator
				pivot = cmds.manipScaleContext( "Scale", q=True, position=True)				
				if len(pivot) == 0:
					print("This tool doesn't work with the pivot gizmo press INSERT to exit Pivot Edit")
					return
				
				orientation = [str(euler.x)+"rad",str(euler.y)+"rad",str(euler.z)+"rad"]
				x,y,z = (1 , 1 , 1) # default to 1 ( no scale)
				if len(values) > 1:		
					x = values[0]					
					y = values[1]
					if len(values) > 2:
						z = values[2]
				x = float(x)
				y = float(y)
				z = float(z)
				v = float(v)
				direction = oMaya.MVector(x,y,z)	
				if len(values) > 1:					
					cmds.scale( x,y,z,  p=pivot , oa=orientation)
				else:	
					direction = oMaya.MVector(1,1,1)								
					if axisindex == 0: # X
						direction.x = v
					if axisindex == 1: # Y
						direction.y = v						
					if axisindex == 2: # Z
						direction.z = v
					if axisindex == 3 : #ALL
						direction = oMaya.MVector(v,v,v)
					if axisindex == 4: #X&Y
						direction.x = v
						direction.y = v					
					if axisindex == 5: #Y&Z
						direction.y = v
						direction.z = v						
					if axisindex == 6: #X&Z
						direction.x = v 
						direction.z = v						

				if euler.x == euler.y == euler.z == 0:
					cmds.scale( direction.x,direction.y,direction.z,  p=pivot )
				else:
					cmds.scale( direction.x,direction.y,direction.z,  p=pivot , oa=orientation)
		else:
			print("Only works if Move, Rotate or Scale tool is active")
		cmds.deleteUI("InputPrompt")

	@staticmethod
	def openPrompt(axis="x"):
		#if NumericalInput.isValidContext():
		ctx = cmds.currentCtx()
		contextname = cmds.contextInfo(ctx, c=True)
		NumericalInput.contextname = contextname

		
		NumericalInput.axis = axis
		if(cmds.window("InputPrompt",q=1,ex=1)):cmds.deleteUI("InputPrompt")
		cmds.window("InputPrompt",t='ifield',s=0,tb=0,mb=1)
		cmds.columnLayout('column')
		cmds.textField("numfield",  ec=NumericalInput.enteredvalue ,alwaysInvokeEnterCommandOnReturn=True, w=120,bgc=[0.0, 0.0, 0.0] )
		cmds.showWindow("InputPrompt")		
		cmds.setFocus("numfield")
		


