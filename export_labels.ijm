run("Duplicate...", "title="+getTitle()+"-labels.tif");
run("Multiply...", "value=0.000");
print(roiManager("count"))
for (i = 0; i < roiManager("count"); i++){
  roiManager("Select", i);
  lab = i+1;
  run("Multiply...", "value=0.000");
  run("Add...","value="+lab);
}

run("16 colors");
run("Enhance Contrast", "saturated=0.0");