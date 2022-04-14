
function antibio_im_for_ann(path,tl,outpath){
	
	run("Close All");
	open(path + '/' + tl);	
	
	selectWindow(tl);
	tlname = getInfo("image.filename");
	st= replace(tlname, ".tif", "_");
	run("Duplicate...", "title=Cycloserine duplicate channels=2 frames=30");
	imname= getInfo("image.filename");
	imname_st= replace(imname, "Position", "Cyclo_271120_"+st+"30_");
	saveAs("Tiff", outpath+"/"+imname_st);
}

path = "C:/Users/ldestouches/Documents/IMAGES & TIMELAPSES/ANTIBIO/Cycloserine/untreated/27-11-20";
outpath = "C:/Users/ldestouches/Documents/IMAGES & TIMELAPSES/ANTIBIO/Images for Annotations"

tllist = getFileList(path);
for (i = 0; i < tllist.length; i++){
        antibio_im_for_ann(path, tllist[i], outpath);
}

run("Close All");