cardWidth = 2.1215
cardHeight = 3.3675
cardThickness = 0.0335

numRows = 3
numCols = 30.0/numRows

rowSpacing = 0.3
colSpacing = 0.25

width = (numCols * cardWidth) + ((numCols + 1) * colSpacing)
height = (numRows * cardHeight) + ((numRows + 1) * rowSpacing)

print width
print height
