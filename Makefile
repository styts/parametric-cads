all: phone_holder lid_rack

phone_holder:
	python phone_holder.py

lid_rack:
	python lid_rack.py

render:
	/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD --render output/phone_holder_2d.scad -o output/phone_holder.dxf
	/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD --render output/lid_rack_2d.scad -o output/lid_rack.dxf
