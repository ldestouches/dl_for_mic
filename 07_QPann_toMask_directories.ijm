

// here I should change filenameMask to just filename to remove _mask - decided its ok like this
// try to loop through the ROI too

function mask(input,output,imname,roipath,roiname){
	
	run("Close All");
	roiManager("reset");

	print("processing file ", imname);
	
	open(input + '/' + imname);
	imnameRaw=getInfo("image.filename");
	imnameMask= replace(imnameRaw, ".tif", "_mask.tif");
	
	run("Duplicate...", "title="+imnameMask);
	run("Multiply...", "value=0");

	//open(roipath + '/' + roiname);
	
	//roipath= File.openDialog("Select ROI");
	//roiname= File.getName(roipath);
	roiManager("Open", roipath + "/" + roiname);

	nROI=roiManager("count");
	selectWindow(imnameMask);
	for (iROI = 0; iROI < nROI; iROI++) {
		roiManager("Select", iROI);
		run("Multiply...", "value=0");
		run("Add...", "value=1");
		run("Add...", "value="+iROI);
	}
	
	run("Select None");
	resetMinAndMax();
	run("Set Label Map", "colormap=[Mixed Colors] background=Black shuffle");

	saveAs("tiff", output + '/' + imnameMask);
}


input = "C:/Users/ldestouches/Documents/IMAGES & TIMELAPSES/SIM/SIM_tif";
output = "C:/Users/ldestouches/Documents/IMAGES & TIMELAPSES/SIM/SIM_mask";
roipath = "C:/Users/ldestouches/Documents/IMAGES & TIMELAPSES/SIM/ROI_SIM";

imlist = getFileList(input);
roilist = getFileList(roipath);
for (i = 0; i < imlist.length; i++){
        mask(input, output, imlist[i],roipath,roilist[i]);
}

run("Close All");
