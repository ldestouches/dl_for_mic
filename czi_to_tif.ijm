
// This program loops through czi files in a folder and exports them as tif files.

function czi_to_tif(input,output,imname){

	run("Close All");
	
	print("processing file ", imname);
	
	open(input + '/' + imname);
	
	run("Duplicate...", "duplicate channels=1");
	
	saveAs("Tiff", output + '/' + imname);
}

input = "P:/proced/5- User Exchange folders/Caro_Louise/ImagesSIM/Experiment02_220504/Images";
output = "C:/Users/ldestouches/Documents/IMAGES & TIMELAPSES/SIM/SIM_tif";

imlist = getFileList(input);
for (i = 0; i < imlist.length; i++){
        czi_to_tif(input, output, imlist[i]);
}

run("Close All");
