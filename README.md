# Numerical Input
A Maya script for manual numeric input of translation tools

# How to Use
With the Move/Scale/Rotate tool select the handle you want to manipulate and press the hotkey (Shift+Alt+Q) and type in the value you want to apply to it

Features:
- Supports Custom Pivots
- Pivot Pinning
- Multiple Axis input support ( Simultaneously change X Y and Z by typing in all 3 numbers seperated by space)

# Installation
Copy the directory to your scripts folder make sure to remove  "-main" from the directory name
ie \Users\<username>\Documents\Maya\scripts\NumericalInput



![Step_0](https://github.com/Shinobubu/NumericalInput/assets/14949931/32a17b57-688e-4510-b998-a28ad37b25ff)


![Step_1](https://github.com/Shinobubu/NumericalInput/assets/14949931/76a3fd64-d7b6-4224-90d7-ea09997b6586)

# Creating Hotkeys
Importing the shortcut file will **override** your existing custom hotkey binds! 
If you don't want this to happen you can create your own custom script keybind 
- Create a new Runtime Command Editor
- Name: _MoveNumerical_
- Category: _Custonm Scripts_
- Sub-Category: _Transform_
- Language: _Python_

Paste the following code
```  
from importlib import reload
from NumericalInput import NumericalInput
reload(NumericalInput)
NumericalInput.NumericalInput.openPrompt()
```
![Create_Hotkey](https://github.com/Shinobubu/NumericalInput/assets/14949931/9ad6f3c8-c37b-44c5-ad5f-15e55b70d8b0)
![Create_Hotkey_2](https://github.com/Shinobubu/NumericalInput/assets/14949931/cf5a59ae-a3ab-43bb-9e3b-e541bec539f1)

If you are not concerned with overwritting your existing hotkeys proceed to the steps below

# Importing Hotkeys
![Step_2](https://github.com/Shinobubu/NumericalInput/assets/14949931/2b045f8a-0bb5-4fb5-a85d-f3655b02e9d9)

![Step_3](https://github.com/Shinobubu/NumericalInput/assets/14949931/5c15ccbf-4f39-4880-ab13-0fd7250211b4)

![Step_4](https://github.com/Shinobubu/NumericalInput/assets/14949931/fc644ece-031b-4f7b-99b2-6bf6eb8a4b4f)

![Step_5](https://github.com/Shinobubu/NumericalInput/assets/14949931/d4a6270c-d179-41f4-858e-782d78f20717)

![Step_6](https://github.com/Shinobubu/NumericalInput/assets/14949931/034be218-8f68-4951-8f10-330a9c2a3a26)

# Demonstration Video
Coming Soon
