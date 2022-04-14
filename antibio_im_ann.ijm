
function antibio_im_for_ann(path,tl,outpath){
	
	run("Close All");
	open(path + '/' + tl);	
	
	selectWindow(tl);
	tlname = getInfo("image.filename");
	st= replace(tlname, ".tif", "_");
	run("Duplicate...", "title=Fosfo duplicate channels=2 frames=1");
	imname= getInfo("image.filename");
	imname_st= replace(imname, "Position", "Fosfo_241120_"+st+"01_");
	saveAs("Tiff", outpath+"/"+imname_st);
	
	selectWindow(tl);
	run("Duplicate...", "title=Fosfo duplicate channels=2 frames=20");
	imname= getInfo("image.filename");
	imname_st= replace(imname, "Position", "Fosfo_241120_"+st+"20_");
	saveAs("Tiff", outpath+"/"+imname_st);
	
	selectWindow(tl);
	run("Duplicate...", "title=Fosfo duplicate channels=2 frames=40");
	imname= getInfo("image.filename");
	imname_st= replace(imname, "Position", "Fosfo_241120_"+st+"40_");
	saveAs("Tiff", outpath+"/"+imname_st);
		
	selectWindow(tl);
	run("Duplicate...", "title=Fosfo duplicate channels=2 frames=60");
	imname= getInfo("image.filename");
	imname_st= replace(imname, "Position", "Fosfo_241120_"+st+"60_");
	saveAs("Tiff", outpath+"/"+imname_st);
		
	selectWindow(tl);
	run("Duplicate...", "title=Fosfo duplicate channels=2 frames=80");
	imname= getInfo("image.filename");
	imname_st= replace(imname, "Position", "Fosfo_241120_"+st+"80_");
	saveAs("Tiff", outpath+"/"+imname_st);
}

path = "C:/Users/ldestouches/Documents/IMAGES & TIMELAPSES/ANTIBIO/Fosfomycin/untreated/24-11-20";
outpath = "C:/Users/ldestouches/Documents/IMAGES & TIMELAPSES/ANTIBIO/Images for Annotations"

tllist = getFileList(path);
for (i = 0; i < tllist.length; i++){
        antibio_im_for_ann(path, tllist[i], outpath);
}

run("Close All");