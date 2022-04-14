
function mask(input,output,filename){
	
	run("Close All");
	roiManager("reset");

	print("this is file", filename);
	print(input+filename);
	open(input + '/' + filename);
	filenameRaw=getInfo("image.filename"); //not sure how to modify this
	filenameMask=replace(filenameRaw, ".tif", "_mask.tif");
	
	print("2");
	run("Duplicate...", "title="+filenameMask);
	run("Multiply...", "value=0");

	print("3");
	roipath= File.openDialog("Select ROI");
	roiname= File.getName(roipath);
	roiManager("Open", roipath);

	print("4");
	nROI=roiManager("count");
	selectWindow(filenameMask);
	for (iROI = 0; iROI < nROI; iROI++) {
		roiManager("Select", iROI);
		run("Multiply...", "value=0");
		run("Add...", "value=1");
		run("Add...", "value="+iROI);
	}
	
	run("Select None");
	resetMinAndMax();
	run("Set Label Map", "colormap=[Mixed Colors] background=Black shuffle");

	print("5");
	print(output + '/' + filenameMask);
	saveAs("tiff", output + '/' + filenameMask);

	print("6");
}


input = "C:/Users/ldestouches/Documents/SOFTWARE/Fiji/fiji_directory/input";
print(input);
output = "C:/Users/ldestouches/Documents/SOFTWARE/Fiji/fiji_directory/output";
//roipath = "C:/Users/ldestouches/Documents/SOFTWARE/Fiji/fiji_directory/roi";

list = getFileList(input);
for (i = 0; i < list.length; i++){
        mask(input, output, list[i]);
}

run("Close All");
