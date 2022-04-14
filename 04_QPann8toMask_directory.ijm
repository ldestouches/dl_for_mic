
function mask(input,output,filename,roipath,roi){
	
	run("Close All");
	roiManager("reset");

	open(input+filename);
	filenameRaw=getInfo("image.filename"); //not sure how to modify this
	filenameMask=replace(filenameRaw, ".tif", "_mask.tif");

	run("Duplicate...", "title="+filenameMask);
	run("Multiply...", "value=0");

	//roipath= File.openDialog("Select ROI");
	roiManager("Open", roipath+roi);

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
	
	pathMask=folderRaw+filenameMask;
	
	saveAs("tiff", output + filenameMask);
}


input = "C:/Users/ldestouches/Documents/SOFTWARE/Fiji/fiji_directory";
output = "C:/Users/ldestouches/Documents/SOFTWARE/Fiji/fiji_directory";
roipath = "C:/Users/ldestouches/Documents/SOFTWARE/Fiji/fiji_directory/roi";

list = getFileList(input);
for (i = 0; i < list.length; i++){
        mask(input, output, list[i], roipath, list[i]); // I should add AND for roi list[i]
}
SetBatchMode(false); // not sure what this does