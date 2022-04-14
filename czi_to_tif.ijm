
// This program loops through czi files in a folder and exports them as tif files.

function czi_to_tif(input,output,imname){

	run("Close All");
	
	print("processing file ", imname);
	
	open(input + '/' + imname);
	
	run("Duplicate...", "duplicate channels=1");
	
	saveAs("Tiff", output + '/' + imname);
}

input = "P:/proced/5- User Exchange folders/Caro_Louise/ImagesSIM/Images";
output = "C:/Users/ldestouches/Documents/IMAGES/Caro_SIM/im";

imlist = getFileList(input);
for (i = 0; i < imlist.length; i++){
        czi_to_tif(input, output, imlist[i]);
}

run("Close All");
