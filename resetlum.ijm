
function resetlum(input,output,imname){
	
	open(input + '/' + imname);
	imnameRaw=getInfo("image.filename");
	imnameReset= replace(imnameRaw, ".tif", "_reset.tif");
	
	run("Brightness/Contrast...");
	resetMinAndMax();
	run("Apply LUT");
	saveAs("tiff", output + '/' + imnameReset);
	
	run("Close All");
}

input = "C:/Users/ldestouches/Documents/Luminosité/TLex_unstacked";
output = "C:/Users/ldestouches/Documents/Luminosité/unstacked_reset";

imlist = getFileList(input);

for (i = 0; i < imlist.length; i++){
        resetlum(input, output, imlist[i]);
}
