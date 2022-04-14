
function mask(input,output,filename,roipath){
	
	run("Close All");
	roiManager("reset");

	open(input);
	filenameRaw=getInfo("image.filename"); //not sure how to modify this
	print(filenameRaw)
	filenameMask=replace(filenameRaw, ".tif", "_mask.tif");

	run("Duplicate...", "title="+filenameMask);
	run("Multiply...", "value=0");

	roiManager("Open", roipath);

	nROI=roiManager("count");
	selectWindow(filenameMask);
	for (iROI = 0; iROI < nROI; iROI++) {
		roiManager("Select", iROI);
		run("Multiply...", "value=0");
		run("Add...", "value=1");
		run("Add...", "value="+iROI);

	run("Select None");
	resetMinAndMax();
	run("Set Label Map", "colormap=[Mixed Colors] background=Black shuffle");
	
	pathMask=folderRaw+filenameMask;
	
	saveAs("tiff", output + filenameMask)
}


input = "C:/Users/ldestouches/Documents/SOFTWARE/Fiji/fiji_directory";
output = "C:/Users/ldestouches/Documents/SOFTWARE/Fiji/fiji_directory";
roipath= File.openDialog("Select ROI");

list = getFileList(input);
for (i = 0; i < list.length; i++){
        mask(input, output, list[i],roipath);
}
SetBatchMode(false) // not sure what this does