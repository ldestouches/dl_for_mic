
// ROI MEASURE LENGTH AND WIDTH OF INDIVIDUAL BACTERIA

// This script selects an image and uses Roi measure to extract the length and width 
// of each ROI and saves them in an csv file.
// will add iteration through folder later

function roimeasuretocsv(im,roizip){
	
	//roiManager("reset");
	open(im);
	imname = getInfo("image.filename");
	roiManager("Open", roizip);
	
	nROI=roiManager("count");
	print(nROI);
	selectWindow(imname);
	
	for (iROI = 0; iROI < nROI; iROI++) {
		roiManager("Select", iROI);
		run("Measure Roi");
	}
	
	saveAs("Results", "C:/Users/ldestouches/Documents/SOFTWARE/Python/roimeasure/roimeasure_results_Ann_Cyclo_190220_stage9_80_blup.csv");
}

im = File.openDialog("Select image");
roizip = File.openDialog("Select ROI");
roimeasuretocsv(im,roizip);
