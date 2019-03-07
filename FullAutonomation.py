# This code seeks to create a file structure for the user. After, the user will
# be promted to enter the location for their photos, which will relocate them
# into the newly created directory. After, a full processing script will begin,
# running through the set parameters, and then saving and exporting the file to
# a before-mentioned location.
# Created by Jacob Rayl <jrayl@sycamores.indstate.edu>
# Draft #2. Updated on Feb. 1, 2019 @12:00pm

# Beginning the folder set-up phase

##def folderset():
##    print ("Creating folder set-up")
##    import os
##    
##    folderpath = input("Specify the location for your project: ") #input the correct pathway including the "\\"
##    foldername = input("Specify the name of your project: ") #input the correct name for your new folder
##    
##    os.chdir(folderpath)
##    os.mkdir(foldername)
##    os.chdir(folderpath + "\\" + foldername)
##    os.mkdir("export")
##    os.mkdir("photos")
##    os.mkdir("output")
##    #os.chdir(folderpath + "\\" + foldername + "\\" + "photos") #Not needed as rig folder errors if within the photo folder for processing script (see below)
##    os.mkdir("rig")
##    print ("Folders done!")
##    return 1
##    Metashape.app.update()
##
##folderset()
##
##
##
### Beginning transfer of photos to new directory.
##
##def relocate():
##    print ("Let's relocate your photos")
##    import shutil
##    import os
##
##    source = input("Please enter path to photos: ")
##    dest1 = input("Please enter the path for relocation: ")
##
##    files = os.listdir(source)
##
##    for f in files:
##        shutil.move(source+f, dest1)
##    return 1
##
##relocate()



#Beginning the processing phase

def autostart():
    import os
    import Metashape
    doc = Metashape.app.document
    
    print("Beginning start-up sequence")
    
    path_photos = Metashape.app.getExistingDirectory("Tell me where to find your photos:")
    path_photos += "//"
	
    print ("Checking save filename")
    project_path = Metashape.app.getSaveFileName("Specify file name and location for saving:")
    if not project_path:
	    print("Booting Down")
	    return 0
	
    if project_path[-4:].lower() != ".psz":
	    project_path += ".psz"

    #creating new chunk
    doc.addChunk()
    chunk = doc.chunks[-1]	    
	
    print ("Adding photos")
    image_list =[
		os.path.join(path_photos, path)
		for path in os.listdir(path_photos)
		if path.lower().endswith(("jpg", "jpeg", "tif", "png","JPG","JPEG","TIF",""))
		]
    chunk.addPhotos(image_list)

##    doc.save("D://Fall2018//ENVI472GeospatialTopics//test//export//Lab4.psx") #Change this path to your saved location
##    print ("File Saved")
    
##    os.listdir(path_photos)
##    for photo in image_list:
##	    if ("jpg" or "jpeg" or "tif" or "png" or "JPG" or "JPEG" or "TIF" or "PNG"): #in photo.lower():
##                chunk.photos.add(path_photos + photo)
##    Metashape.app.update()
	
    print ("Time to align photos")
    chunk.detectMarkers() #use only if you are using a marker pallet of sorts
    chunk.matchPhotos(accuracy = Metashape.HighAccuracy, preselection = Metashape.NoPreselection)

    chunk.alignCameras()

    chunk.buildDepthMaps()

    #build dense cloud
    print ("Building you a dense cloud")
    chunk.buildDenseCloud()
	
    #build mesh
    print ("Making you a mesh, now")
    chunk.buildModel(face_count = Metashape.HighFaceCount, surface = Metashape.Arbitrary, source = Metashape.PointCloudData)

    chunk.buildUV()
    
    #build texture
    print ("Generating your textures now")
    chunk.buildTexture()
    
    #save
    doc.save(path = project_path)
    Metashape.app.update()

    #export
    chunk.exportModel(path = project_path + ".obj", texture_format = Metashape.ImageFormatPNG, format = Metashape.ModelFormatOBJ)

    print("Processing complete; please check directory.")
    return 1

autostart()
