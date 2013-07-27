all:
	python phone_holder.py

render:
	/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD --render output/phone_holder_2d.scad -o output/phone_holder.dxf
