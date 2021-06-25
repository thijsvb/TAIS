#imports:

#Numpy
import numpy as  np
#STL creator
from stl import mesh
#SKimage
from skimage import transform

def data_to_stl(input_data, model_size, downscale_factor=None, base_off=1):
    ncols, nrows = input_data.shape
    x_len, y_len, z_len = model_size
    z_max = z_len - base_off

    #downscale data
    if downscale_factor is None:
        needed_res = max(x_len, y_len)//0.3 # rough estimation for needed array length based on common nozzle size (0.3) and model size
        downscale_factor = int(min(ncols, nrows)//needed_res)
    if downscale_factor > 1:
        # this downscale function sometimes produces lower values than are in the original image
        # to fix this, chop the image back to the old minimum after downscaling
        floor = input_data.min()
        input_data = transform.downscale_local_mean(input_data, (downscale_factor, downscale_factor))
        mask = input_data < floor
        input_data[mask] = floor
    ncols, nrows = input_data.shape

    #shift data to start from z=0
    input_data -= input_data.min()
    data_max = input_data.max()

    vertices=np.zeros((nrows,ncols,3))
    checkzs = []
    for x in range(0, ncols):
        for y in range(0, nrows):
            z = input_data[x][y]/data_max*z_max + base_off
            checkzs.append(z)
            vertices[y][x]=(x/(ncols-1)*x_len, y/(nrows-1)*y_len, z)

    faces = facemaker(vertices)

    print(f"number of faces: {len(faces)}")
    facesNp = np.array(faces)

    # Create the mesh
    surface = mesh.Mesh(np.zeros(facesNp.shape[0], dtype=mesh.Mesh.dtype))
    for i in range(len(faces)):
        for j in range(3):
            surface.vectors[i][j] = facesNp[i][j]

    # Write the mesh to a file so we can print it
    # surface.save(filename)
    # return mesh to be saved by UI
    return surface

#Function that creates triangles of the model that we want to print from the (x,y,z) positions array that we feed in.
#Can show the scaling radius as well if parameters are provided
def facemaker(vertices):
    ncols, nrows, xyz = vertices.shape
    faces=[]

    #faces for the input array
    for y in range(0, ncols - 1):
        for x in range(0, nrows - 1):
            # create face 1
            vertice1 = vertices[y][x]
            vertice2 = vertices[y+1][x]
            vertice3 = vertices[y+1][x+1]
            face1 = np.array([vertice1,vertice2,vertice3])

            # create face 2
            vertice1 = vertices[y][x]
            vertice2 = vertices[y][x+1]
            vertice3 = vertices[y+1][x+1]

            face2 = np.array([vertice1,vertice3,vertice2])

            faces.append(face1)
            faces.append(face2)


    #faces for edges and bottom
    #I couldn't figure out how to make this one loop and fix the triangle orientation at the same time
    bottomfaces = []
    vertice0 = (0, 0, 0)
    y = 0
    for x in range(0, ncols-1):
        vertice1 = vertices[x][y]
        vertice2 = vertices[x+1][y]
        vertice3 = (vertice1[0], vertice1[1], 0)
        vertice4 = (vertice2[0], vertice2[1], 0)

        face1 = np.array([vertice1, vertice3, vertice4])
        face2 = np.array([vertice1, vertice4, vertice2])
        faces.append(face1)
        faces.append(face2)

        bface = np.array([vertice4, vertice3, vertice0])
        bottomfaces.append(bface)
    y = -1
    for x in range(0, ncols-1):
        vertice1 = vertices[x][y]
        vertice2 = vertices[x+1][y]
        vertice3 = (vertice1[0], vertice1[1], 0)
        vertice4 = (vertice2[0], vertice2[1], 0)

        face1 = np.array([vertice1, vertice4, vertice3])
        face2 = np.array([vertice1, vertice2, vertice4])
        faces.append(face1)
        faces.append(face2)

        bface = np.array([vertice3, vertice4, vertice0])
        bottomfaces.append(bface)
    x = 0
    for y in range(0, nrows-1):
        vertice1 = vertices[x][y]
        vertice2 = vertices[x][y+1]
        vertice3 = (vertice1[0], vertice1[1], 0)
        vertice4 = (vertice2[0], vertice2[1], 0)

        face1 = np.array([vertice1, vertice4, vertice3])
        face2 = np.array([vertice1, vertice2, vertice4])
        faces.append(face1)
        faces.append(face2)

        bface = np.array([vertice3, vertice4, vertice0])
        bottomfaces.append(bface)
    x = -1
    for y in range(0, nrows-1):
        vertice1 = vertices[x][y]
        vertice2 = vertices[x][y+1]
        vertice3 = (vertice1[0], vertice1[1], 0)
        vertice4 = (vertice2[0], vertice2[1], 0)

        face1 = np.array([vertice1, vertice3, vertice4])
        face2 = np.array([vertice1, vertice4, vertice2])
        faces.append(face1)
        faces.append(face2)

        bface = np.array([vertice4, vertice3, vertice0])
        bottomfaces.append(bface)

    for face in bottomfaces:
        faces.append(face)

    return faces
