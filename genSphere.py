import bpy
import random

print("- - "*20)
random.seed(27051996)

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

        (0,0,-1)
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

def createMeshFromData(name, origin, scale, verts, faces):
    # Create mesh and object
    me = bpy.data.meshes.new(name+'Mesh')
    ob = bpy.data.objects.new(name, me)
    ob.location = origin
    ob.scale = scale

    # Link object to scene and make active
    scn = bpy.context.scene
    scn.objects.link(ob)
    scn.objects.active = ob
    # ob.select = False

    # Create mesh from given verts, faces.
    me.from_pydata(verts, [], faces)

    # Update mesh with new data
    me.update()


def subdivide(verts, faces, iteration):
    newFaces = []
    dividedEdges = {}

    def vecLen(vec):
        return sum([c**2 for c in vec])**.5

    def scaleVecToLen(vec, desiredLength):
        vecLen_now = vecLen(vec)
        return (
            vec[0] * desiredLength / vecLen_now,
            vec[1] * desiredLength / vecLen_now,
            vec[2] * desiredLength / vecLen_now
        )

    def getCenterPoint(p1, p2):
        vecLen_p1 = vecLen(verts[p1])
        vecLen_p2 = vecLen(verts[p2])
        vecLen_new = (vecLen_p1 + vecLen_p2)*.5
        heightDelta = random.gauss(0,.01*(.6**iteration))

        return scaleVecToLen ((
            (verts[p1][0] + verts[p2][0]) * .5,
            (verts[p1][1] + verts[p2][1]) * .5,
            (verts[p1][2] + verts[p2][2]) * .5
        ), vecLen_new + heightDelta)

    def divideEdge(edge):
        try:
            normalizedEdge = list(edge)
            normalizedEdge.sort()
            normalizedEdge = tuple(normalizedEdge)
            return dividedEdges[tuple(normalizedEdge)]
        except Exception as e:
            newVert  = getCenterPoint(*edge)
            newIndex = len(verts)
            normalizedEdge = list(edge)
            normalizedEdge.sort()
            normalizedEdge = tuple(normalizedEdge)
            dividedEdges[normalizedEdge] = newIndex
            verts.append(newVert)
            return newIndex

    for face in faces:
        edge1 = (face[0], face[1])
        edge2 = (face[1], face[2])
        edge3 = (face[2], face[0])

        newFaces.append((
            face[0],
            divideEdge(edge1),
            divideEdge(edge3)
        ))

        newFaces.append((
            face[1],
            divideEdge(edge2),
            divideEdge(edge1)
        ))

        newFaces.append((
            face[2],
            divideEdge(edge3),
            divideEdge(edge2)
        ))

        newFaces.append((
            divideEdge(edge1),
            divideEdge(edge2),
            divideEdge(edge3)
        ))


    return verts, newFaces


verts, faces = generateIcoSphere()
for i in range(10):
    verts, faces = subdivide(verts, faces, i+1)


createMeshFromData('ProcGenSphere', (0,0,0), (8,8,8), verts, faces)
