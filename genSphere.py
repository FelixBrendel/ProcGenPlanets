import bpy

print("- - "*20)

def generateIcoSphere():

    verts = [
        (0,0,1),

        (0.89442,  0,       0.44721),
        (0.27639,  0.85064, 0.44721),
        (-0.7236,  0.52572, 0.44721),
        (-0.7236, -0.52572, 0.44721),
        (0.27639, -0.85064, 0.44721),

        (  0.7236,  0.52572, -0.44721),
        (-0.27639,  0.85064, -0.44721),
        (-0.89442,  0,       -0.44721),
        (-0.27639, -0.85064, -0.44721),
        (  0.7236, -0.52572, -0.44721),

        (0,0,-1),
    ]

    faces = (
        (0,1,2),
        (0,2,3),
        (0,3,4),
        (0,4,5),
        (0,5,1),

        (1,6,2),
        (2,7,3),
        (3,8,4),
        (4,9,5),
        (5,10,1),

        (10,6,1),
        (6,7,2),
        (7,8,3),
        (8,9,4),
        (9,10,5),

        (10,11,6),
        (6,11,7),
        (7,11,8),
        (8,11,9),
        (9,11,10)
    )
    return (verts, faces)

def createMeshFromData(name, origin, verts, faces):
    # Create mesh and object
    me = bpy.data.meshes.new(name+'Mesh')
    ob = bpy.data.objects.new(name, me)
    ob.location = origin

    # Link object to scene and make active
    scn = bpy.context.scene
    scn.objects.link(ob)
    scn.objects.active = ob
    ob.select = True

    # Create mesh from given verts, faces.
    me.from_pydata(verts, [], faces)
    # Update mesh with new data
    me.update()


def subdivide(verts, faces):
    newFaces = []
    dividedEdges = {}

    def normalize(point):
        vecLen = sum([c**2 for c in point])**.5
        return tuple(c/vecLen for c in point)

    def getCenterPoint(p1, p2):
        return normalize ((
            (verts[p1][0]+verts[p2][0])*.5,
            (verts[p1][1]+verts[p2][1])*.5,
            (verts[p1][2]+verts[p2][2])*.5
        ))

    def divideEdge(edge):
        try:
            return dividedEdges[edge]
        except Exception as e:
            newVert  = getCenterPoint(*edge)
            newIndex = len(verts)
            dividedEdges[edge] = newIndex
            verts.append(newVert)
            return newIndex

    for face in faces:
        edge1 = (face[0], face[1])
        edge2 = (face[1], face[2])
        edge3 = (face[2], face[0])

        divideEdge(edge1)
        divideEdge(edge2)
        divideEdge(edge3)

        newFaces.append((
            face[0],
            dividedEdges[edge1],
            dividedEdges[edge3]
        ))

        newFaces.append((
            face[1],
            dividedEdges[edge2],
            dividedEdges[edge1]
        ))

        newFaces.append((
            face[2],
            dividedEdges[edge3],
            dividedEdges[edge2]
        ))

        newFaces.append((
            dividedEdges[edge1],
            dividedEdges[edge2],
            dividedEdges[edge3]
        ))


    return verts, newFaces


verts, faces = generateIcoSphere()
verts, faces = subdivide(verts, faces)
verts, faces = subdivide(verts, faces)
verts, faces = subdivide(verts, faces)
verts, faces = subdivide(verts, faces)
verts, faces = subdivide(verts, faces)

createMeshFromData('Icosphere', (0,0,0), verts, faces)
