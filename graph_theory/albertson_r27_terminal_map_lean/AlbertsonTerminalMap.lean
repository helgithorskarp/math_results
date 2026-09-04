import Std

/-!
Kernel-checked finite layer of the terminal-triangulation argument used at
the Albertson r = 27 frontier.  This file intentionally does not formalize
Jordan separation, the face-tracing translation from a good drawing, or the
sealed-region provenance lemma.  It records a constructive disk shelling but
does not formalize the elementary topological triangle-gluing lemma.
-/

namespace AlbertsonTerminalMap

inductive Edge where
  | uz | zt | tr | rw | uw
  | zw | zx | wx | tx | rx
  | ur | ut | zr | wt | ux
  deriving DecidableEq, Repr

open Edge

inductive OriginalVertex where
  | u | z | t | r | w
  deriving DecidableEq, Repr

open OriginalVertex

def originalVertices : List OriginalVertex := [u, z, t, r, w]

def unorderedPairs : List OriginalVertex → List (OriginalVertex × OriginalVertex)
  | [] => []
  | first :: rest => rest.map (fun second => (first, second)) ++ unorderedPairs rest

def allEdges : List Edge :=
  [uz, zt, tr, rw, uw, zw, zx, wx, tx, rx, ur, ut, zr, wt, ux]

def outerBoundary : List Edge := [uz, zt, tr, rw, uw]

def diskInternal : List Edge := [zw, zx, wx, tx, rx]

def crossingEdges : List Edge := [zw, ur, ut, zr, wt]

def completeK5 : List Edge := outerBoundary ++ crossingEdges

def originalEndpoints : Edge → Option (OriginalVertex × OriginalVertex)
  | uz => some (u, z)
  | zt => some (z, t)
  | tr => some (t, r)
  | rw => some (r, w)
  | uw => some (u, w)
  | zw => some (z, w)
  | ur => some (u, r)
  | ut => some (u, t)
  | zr => some (z, r)
  | wt => some (t, w)
  | zx | wx | tx | rx | ux => none

def originalEdgesInPairOrder : List Edge :=
  [uz, ut, ur, uw, zt, zr, zw, tr, wt, rw]

def sameEdgeSet (left right : List Edge) : Bool :=
  left.all (fun e => right.contains e) && right.all (fun e => left.contains e)

def diskFaces : List (List Edge) :=
  [ [uz, zw, uw],
    [zw, wx, zx],
    [zt, tx, zx],
    [tr, rx, tx],
    [rw, wx, rx] ]

def diskOccurrences : List Edge := diskFaces.flatten

def multiplicity (e : Edge) : Nat :=
  (diskOccurrences.filter fun candidate => candidate == e).length

def boundaryEdges : List Edge :=
  allEdges.filter fun e => multiplicity e == 1

def internalEdges : List Edge :=
  allEdges.filter fun e => multiplicity e == 2

def absentEdges : List Edge :=
  allEdges.filter fun e => multiplicity e == 0

def crossingPairs : List (Edge × Edge) :=
  [(zw, ur), (zw, ut), (ut, zr), (zr, wt), (wt, ur)]

def crossingDegree (e : Edge) : Nat :=
  (crossingPairs.filter fun pair => pair.1 == e || pair.2 == e).length

def crossingDegrees : List Nat := crossingEdges.map crossingDegree

def listDisjoint (left right : List Edge) : Bool :=
  left.all fun e => !(right.contains e)

inductive PlanarVertex where
  | U | Z | T | R | W | X
  deriving DecidableEq, Repr

open PlanarVertex

structure OrientedFace where
  first : PlanarVertex
  second : PlanarVertex
  third : PlanarVertex
  deriving DecidableEq, Repr

abbrev Dart := PlanarVertex × PlanarVertex

def faceDarts (face : OrientedFace) : List Dart :=
  [(face.first, face.second),
   (face.second, face.third),
   (face.third, face.first)]

def shellFace0 : OrientedFace := ⟨U, Z, W⟩
def shellFace1 : OrientedFace := ⟨W, Z, X⟩
def shellFace2 : OrientedFace := ⟨Z, T, X⟩
def shellFace3 : OrientedFace := ⟨T, R, X⟩
def shellFace4 : OrientedFace := ⟨R, W, X⟩

def orientedFaces : List OrientedFace :=
  [shellFace0, shellFace1, shellFace2, shellFace3, shellFace4]

def orientedOccurrences : List Dart := orientedFaces.flatMap faceDarts

def reverseDart (dart : Dart) : Dart := (dart.2, dart.1)

def dartMultiplicity (dart : Dart) : Nat :=
  (orientedOccurrences.filter fun candidate => candidate == dart).length

def outerDarts : List Dart := [(U, Z), (Z, T), (T, R), (R, W), (W, U)]

def internalDarts : List Dart := [(Z, W), (Z, X), (W, X), (T, X), (R, X)]

def outerDartsOnce : Bool :=
  outerDarts.all fun dart =>
    dartMultiplicity dart == 1 && dartMultiplicity (reverseDart dart) == 0

def internalDartsCancel : Bool :=
  internalDarts.all fun dart =>
    dartMultiplicity dart == 1 && dartMultiplicity (reverseDart dart) == 1

def allPlanarVertices : List PlanarVertex := [U, Z, T, R, W, X]

def planarRank : PlanarVertex → Nat
  | U => 0
  | Z => 1
  | T => 2
  | R => 3
  | W => 4
  | X => 5

def planarEdge (left right : PlanarVertex) : Dart :=
  if planarRank left < planarRank right then (left, right) else (right, left)

def faceLinkEdge (vertex : PlanarVertex) (face : OrientedFace) : Option Dart :=
  if vertex == face.first then
    some (planarEdge face.second face.third)
  else if vertex == face.second then
    some (planarEdge face.first face.third)
  else if vertex == face.third then
    some (planarEdge face.first face.second)
  else
    none

def linkEdges (vertex : PlanarVertex) : List Dart :=
  orientedFaces.filterMap (faceLinkEdge vertex)

def linkDegree (vertex neighbor : PlanarVertex) : Nat :=
  ((linkEdges vertex).filter fun side => side.1 == neighbor || side.2 == neighbor).length

def activeLinkDegrees (vertex : PlanarVertex) : List Nat :=
  (allPlanarVertices.map (linkDegree vertex)).filter fun degree => degree > 0

inductive FaceId where
  | F0 | F1 | F2 | F3 | F4
  deriving DecidableEq, Repr

open FaceId

def allFaceIds : List FaceId := [F0, F1, F2, F3, F4]

def faceEdges : FaceId → List Edge
  | F0 => [uz, zw, uw]
  | F1 => [zw, wx, zx]
  | F2 => [zt, tx, zx]
  | F3 => [tr, rx, tx]
  | F4 => [rw, wx, rx]

def sharesEdge (left right : FaceId) : Bool :=
  (faceEdges left).any fun side => (faceEdges right).contains side

def allFacePairs : List (FaceId × FaceId) :=
  [(F0, F1), (F0, F2), (F0, F3), (F0, F4),
   (F1, F2), (F1, F3), (F1, F4),
   (F2, F3), (F2, F4), (F3, F4)]

def adjacentFacePairs : List (FaceId × FaceId) :=
  allFacePairs.filter fun pair => sharesEdge pair.1 pair.2

def dualSpanningPath : List (FaceId × FaceId) :=
  [(F0, F1), (F1, F2), (F2, F3), (F3, F4)]

def dualSpanningPathValid : Bool :=
  dualSpanningPath.all fun pair => adjacentFacePairs.contains pair

def dualSpanningPathCoversFaces : Bool :=
  let incidentFaces := dualSpanningPath.flatMap fun pair => [pair.1, pair.2]
  allFaceIds.all fun face => incidentFaces.contains face

def isDartPath : List Dart → Bool
  | [] => true
  | [_] => true
  | first :: second :: rest =>
      first.2 == second.1 && isDartPath (second :: rest)

def isClosedDartCycle : List Dart → Bool
  | [] => false
  | first :: rest =>
      isDartPath (first :: rest) &&
        match (first :: rest).getLast? with
        | some last => last.2 == first.1
        | none => false

def orientedOccurrencesFor (faces : List OrientedFace) : List Dart :=
  faces.flatMap faceDarts

def dartMultiplicityIn (faces : List OrientedFace) (dart : Dart) : Nat :=
  ((orientedOccurrencesFor faces).filter fun candidate => candidate == dart).length

def allDarts : List Dart :=
  allPlanarVertices.flatMap fun left =>
    allPlanarVertices.filterMap fun right =>
      if left == right then none else some (left, right)

def allPlanarEdges : List Dart :=
  allDarts.filter fun dart => planarRank dart.1 < planarRank dart.2

def boundaryDartsOf (faces : List OrientedFace) : List Dart :=
  allDarts.filter fun dart =>
    dartMultiplicityIn faces dart == 1 &&
      dartMultiplicityIn faces (reverseDart dart) == 0

def sameDartSet (left right : List Dart) : Bool :=
  left.all (fun dart => right.contains dart) &&
    right.all (fun dart => left.contains dart)

def faceVertices (face : OrientedFace) : List PlanarVertex :=
  [face.first, face.second, face.third]

def verticesInFaces (faces : List OrientedFace) : List PlanarVertex :=
  faces.flatMap faceVertices

def verticesOfDarts (darts : List Dart) : List PlanarVertex :=
  darts.flatMap fun dart => [dart.1, dart.2]

def sameVertexSet (left right : List PlanarVertex) : Bool :=
  left.all (fun vertex => right.contains vertex) &&
    right.all (fun vertex => left.contains vertex)

def faceUndirectedEdges (face : OrientedFace) : List Dart :=
  (faceDarts face).map fun dart => planarEdge dart.1 dart.2

def complexEdges (faces : List OrientedFace) : List Dart :=
  allPlanarEdges.filter fun edge =>
    (orientedOccurrencesFor faces).contains edge ||
      (orientedOccurrencesFor faces).contains (reverseDart edge)

def sharedEdges (faces : List OrientedFace) (next : OrientedFace) : List Dart :=
  (faceUndirectedEdges next).filter fun edge => (complexEdges faces).contains edge

def sharedVertices (faces : List OrientedFace) (next : OrientedFace) :
    List PlanarVertex :=
  (faceVertices next).filter fun vertex => (verticesInFaces faces).contains vertex

def arcEdges (arc : List Dart) : List Dart :=
  arc.map fun dart => planarEdge dart.1 dart.2

def newVertices (faces : List OrientedFace) (next : OrientedFace) :
    List PlanarVertex :=
  (faceVertices next).filter fun vertex => !(verticesInFaces faces).contains vertex

/-- `next` meets the preceding triangle complex in exactly the displayed
connected proper boundary arc, with the opposite orientation on every glued
edge.  Exact shared-edge and shared-vertex tests exclude hidden pinches. -/
def ExactBoundaryAttachment (faces : List OrientedFace) (next : OrientedFace)
    (arc : List Dart) : Prop :=
  0 < arc.length ∧
  arc.length < (faceDarts next).length ∧
  arc.length < (boundaryDartsOf faces).length ∧
  (faceVertices next).Nodup ∧
  arc.Nodup ∧
  (arcEdges arc).Nodup ∧
  isDartPath arc = true ∧
  arc.all (fun dart => (boundaryDartsOf faces).contains dart) = true ∧
  arc.all (fun dart => (faceDarts next).contains (reverseDart dart)) = true ∧
  sameDartSet (sharedEdges faces next) (arcEdges arc) = true ∧
  sameVertexSet (sharedVertices faces next) (verticesOfDarts arc) = true

def shellStage1 : List OrientedFace := [shellFace0]
def shellStage2 : List OrientedFace := shellStage1 ++ [shellFace1]
def shellStage3 : List OrientedFace := shellStage2 ++ [shellFace2]
def shellStage4 : List OrientedFace := shellStage3 ++ [shellFace3]
def shellStage5 : List OrientedFace := shellStage4 ++ [shellFace4]

def shellArc1 : List Dart := [(Z, W)]
def shellArc2 : List Dart := [(Z, X)]
def shellArc3 : List Dart := [(T, X)]
def shellArc4 : List Dart := [(R, X), (X, W)]

def shellBoundary1 : List Dart := [(U, Z), (Z, W), (W, U)]
def shellBoundary2 : List Dart := [(U, Z), (Z, X), (X, W), (W, U)]
def shellBoundary3 : List Dart := [(U, Z), (Z, T), (T, X), (X, W), (W, U)]
def shellBoundary4 : List Dart :=
  [(U, Z), (Z, T), (T, R), (R, X), (X, W), (W, U)]
def shellBoundary5 : List Dart := outerDarts

/-- A constructive shelling of the five triangles.  Starting from one
triangle, the next three triangles attach along one boundary edge and the
last attaches along the boundary path R-X-W.  Every simplex intersection and
every intermediate boundary is computed from the face list. -/
theorem disk_shelling_certificate :
    orientedFaces = shellStage5 ∧
    (faceVertices shellFace0).Nodup ∧
    (faceVertices shellFace1).Nodup ∧
    (faceVertices shellFace2).Nodup ∧
    (faceVertices shellFace3).Nodup ∧
    (faceVertices shellFace4).Nodup ∧
    sameDartSet (boundaryDartsOf shellStage1) shellBoundary1 = true ∧
    sameDartSet (boundaryDartsOf shellStage2) shellBoundary2 = true ∧
    sameDartSet (boundaryDartsOf shellStage3) shellBoundary3 = true ∧
    sameDartSet (boundaryDartsOf shellStage4) shellBoundary4 = true ∧
    sameDartSet (boundaryDartsOf shellStage5) shellBoundary5 = true ∧
    isClosedDartCycle shellBoundary1 = true ∧
    isClosedDartCycle shellBoundary2 = true ∧
    isClosedDartCycle shellBoundary3 = true ∧
    isClosedDartCycle shellBoundary4 = true ∧
    isClosedDartCycle shellBoundary5 = true ∧
    (boundaryDartsOf shellStage1).length = 3 ∧
    (boundaryDartsOf shellStage2).length = 4 ∧
    (boundaryDartsOf shellStage3).length = 5 ∧
    (boundaryDartsOf shellStage4).length = 6 ∧
    (boundaryDartsOf shellStage5).length = 5 ∧
    ExactBoundaryAttachment shellStage1 shellFace1 shellArc1 ∧
    ExactBoundaryAttachment shellStage2 shellFace2 shellArc2 ∧
    ExactBoundaryAttachment shellStage3 shellFace3 shellArc3 ∧
    ExactBoundaryAttachment shellStage4 shellFace4 shellArc4 ∧
    newVertices shellStage1 shellFace1 = [X] ∧
    newVertices shellStage2 shellFace2 = [T] ∧
    newVertices shellStage3 shellFace3 = [R] ∧
    newVertices shellStage4 shellFace4 = [] := by
  unfold ExactBoundaryAttachment
  repeat' apply And.intro
  all_goals decide

/-- The five listed triangles have the claimed disk incidence data, Euler
count, pentagonal boundary, and complementary five-edge crossing cycle. -/
theorem finite_terminal_map_certificate :
    boundaryEdges = outerBoundary ∧
    internalEdges = diskInternal ∧
    absentEdges = [ur, ut, zr, wt, ux] ∧
    diskFaces.length = 5 ∧
    diskOccurrences.length = 15 ∧
    outerBoundary.length = 5 ∧
    diskInternal.length = 5 ∧
    (6 : Nat) + diskFaces.length =
      (outerBoundary.length + diskInternal.length) + 1 ∧
    completeK5.length = 10 ∧
    completeK5.Nodup ∧
    originalVertices.length = 5 ∧
    originalVertices.Nodup ∧
    sameEdgeSet completeK5 originalEdgesInPairOrder = true ∧
    originalEdgesInPairOrder.filterMap originalEndpoints =
      unorderedPairs originalVertices ∧
    listDisjoint outerBoundary crossingEdges = true ∧
    crossingPairs.length = 5 ∧
    crossingPairs.Nodup ∧
    crossingDegrees = [2, 2, 2, 2, 2] ∧
    orientedFaces.length = 5 ∧
    orientedOccurrences.length = 15 ∧
    outerDartsOnce = true ∧
    internalDartsCancel = true := by
  decide

/-- The five original vertices have interval links and the crossing vertex
has the circular link Z-W-R-T-Z.  The displayed edge orders also give an
explicit connected traversal of every link. -/
theorem vertex_link_certificate :
    linkEdges U = [(Z, W)] ∧
    linkEdges Z = [(U, W), (W, X), (T, X)] ∧
    linkEdges T = [(Z, X), (R, X)] ∧
    linkEdges R = [(T, X), (W, X)] ∧
    linkEdges W = [(U, Z), (Z, X), (R, X)] ∧
    linkEdges X = [(Z, W), (Z, T), (T, R), (R, W)] ∧
    activeLinkDegrees U = [1, 1] ∧
    activeLinkDegrees Z = [1, 1, 2, 2] ∧
    activeLinkDegrees T = [1, 1, 2] ∧
    activeLinkDegrees R = [1, 1, 2] ∧
    activeLinkDegrees W = [1, 2, 1, 2] ∧
    activeLinkDegrees X = [2, 2, 2, 2] := by
  decide

/-- The face dual is connected via F0-F1-F2-F3-F4, and all boundary darts
form the single oriented cycle U-Z-T-R-W-U. -/
theorem face_boundary_connectivity_certificate :
    adjacentFacePairs =
      [(F0, F1), (F1, F2), (F1, F4), (F2, F3), (F3, F4)] ∧
    dualSpanningPathValid = true ∧
    dualSpanningPathCoversFaces = true ∧
    dualSpanningPath.length = 4 ∧
    dualSpanningPath.Nodup ∧
    outerDarts = [(U, Z), (Z, T), (T, R), (R, W), (W, U)] ∧
    outerDarts.length = 5 ∧
    outerDarts.Nodup ∧
    isClosedDartCycle outerDarts = true := by
  decide

structure Profile where
  edges : Nat
  crossings : Nat
  fullPentagons : Nat
  deriving DecidableEq, Repr

def profileA : Profile := ⟨103, 57, 9⟩
def profileB : Profile := ⟨106, 64, 11⟩

def crossingC5s (p : Profile) : Nat :=
  (2 * p.edges - 8 * (24 - 2)) / 3

def terminalEdges (p : Profile) : Nat :=
  p.edges - 2 * crossingC5s p

def terminalCrossings (p : Profile) : Nat :=
  p.crossings - 4 * crossingC5s p

def planarVertices (p : Profile) : Nat :=
  24 + terminalCrossings p

def planarEdges (p : Profile) : Nat :=
  terminalEdges p + 2 * terminalCrossings p

def planarFaces (p : Profile) : Nat :=
  planarEdges p + 2 - planarVertices p

def ProfileCertificate (p : Profile) : Prop :=
  3 * p.crossings + 25 * (24 - 2) = 7 * p.edges ∧
  crossingC5s p = p.fullPentagons + 1 ∧
  terminalCrossings p + 3 * (24 - 2) = terminalEdges p ∧
  planarEdges p = 3 * planarVertices p - 6 ∧
  planarFaces p = 2 * planarVertices p - 4 ∧
  3 * planarFaces p = 2 * planarEdges p

/-- Exact profile-A computation: ten crossing C5s reduce to the terminal
planarization (V,E,F) = (41,117,78). -/
theorem profileA_certificate :
    ProfileCertificate profileA ∧
    crossingC5s profileA = 10 ∧
    terminalEdges profileA = 83 ∧
    terminalCrossings profileA = 17 ∧
    planarVertices profileA = 41 ∧
    planarEdges profileA = 117 ∧
    planarFaces profileA = 78 := by
  unfold ProfileCertificate
  decide

/-- Exact profile-B computation: twelve crossing C5s reduce to the terminal
planarization (V,E,F) = (40,114,76). -/
theorem profileB_certificate :
    ProfileCertificate profileB ∧
    crossingC5s profileB = 12 ∧
    terminalEdges profileB = 82 ∧
    terminalCrossings profileB = 16 ∧
    planarVertices profileB = 40 ∧
    planarEdges profileB = 114 ∧
    planarFaces profileB = 76 := by
  unfold ProfileCertificate
  decide

/-- The integer remainder in the last deletion average forces 6089, while
the standard drawing number at r = 27 is 6084. -/
theorem final_integer_certificate :
    298314 = 49 * 6088 + 2 ∧
    49 * 6088 < 298314 ∧
    298314 < 49 * 6089 ∧
    (13 * 13 * 12 * 12) / 4 = 6084 ∧
    6084 < 6089 := by
  decide

#print axioms finite_terminal_map_certificate
#print axioms vertex_link_certificate
#print axioms face_boundary_connectivity_certificate
#print axioms disk_shelling_certificate
#print axioms profileA_certificate
#print axioms profileB_certificate
#print axioms final_integer_certificate

end AlbertsonTerminalMap
