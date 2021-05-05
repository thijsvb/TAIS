#imports:

#Numpy
import numpy as  np
#STL image creator
from stl import mesh

def data_to_stl(filename, input_data, model_size, base_off=1):
    ncols, nrows = input_data.shape
    x_len, y_len, z_len = model_size
    z_max = z_len - base_off
    #shift data to start from z=0
    input_data -= input_data.min()
    data_max = input_data.max()
    #determine voxel x and y length
    voxel_x_len = x_len / ncols
    voxel_y_len = y_len / nrows

    scaled_data=np.zeros((nrows,ncols,3))
    for i in range(0, ncols):
        for j in range(0, nrows):
            z = input_data[i][j]/data_max*z_max + base_off
            x = i/ncols*x_len + voxel_x_len/2
            y = j/nrows*y_len + voxel_y_len/2
            scaled_data[i][j]=(x, y, z)

    meshes = []
    for i in range(ncols):
        for j in range(nrows):
            x, y, z = scaled_data[i][j]
            v_mesh = voxel_mesh(x, y, voxel_x_len, voxel_y_len, z)
            meshes.append(v_mesh)
    # combine the meshes
    combined = mesh.Mesh(np.concatenate([m.data for m in meshes]))

    # Write the mesh to a file so we can print it
    combined.save(filename)

    return

#function that creates the mesh of a bar voxel
def voxel_mesh(center_x, center_y, voxel_x_len, voxel_y_len, height):
    vertice1 = [center_x - voxel_x_len/2, center_y - voxel_y_len/2, 0]
    vertice2 = [center_x + voxel_x_len/2, center_y - voxel_y_len/2, 0]
    vertice3 = [center_x - voxel_x_len/2, center_y + voxel_y_len/2, 0]
    vertice4 = [center_x + voxel_x_len/2, center_y + voxel_y_len/2, 0]
    vertice5 = [center_x - voxel_x_len/2, center_y - voxel_y_len/2, height]
    vertice6 = [center_x + voxel_x_len/2, center_y - voxel_y_len/2, height]
    vertice7 = [center_x - voxel_x_len/2, center_y + voxel_y_len/2, height]
    vertice8 = [center_x + voxel_x_len/2, center_y + voxel_y_len/2, height]

    faces = [[vertice1, vertice3, vertice4], [vertice1, vertice4, vertice2],
             [vertice1, vertice2, vertice6], [vertice1, vertice6, vertice5],
             [vertice1, vertice5, vertice3], [vertice5, vertice7, vertice3],
             [vertice2, vertice4, vertice6], [vertice4, vertice8, vertice6],
             [vertice3, vertice7, vertice8], [vertice3, vertice8, vertice4],
             [vertice5, vertice6, vertice8], [vertice5, vertice8, vertice7]]

    surface = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))
    for i in range(len(faces)):
        for j in range(3):
            surface.vectors[i][j] = faces[i][j]

    return surface
