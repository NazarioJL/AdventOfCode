open System
open System.Collections.Generic
open System.Numerics
open System.IO

let manhattan (c: Complex) = (abs c.Real) + (abs c.Imaginary)

let dirToComplex (dir: string) =
    let t = dir[0]
    let a = dir.Substring(1) |> Int32.Parse

    match t with
    | 'R' -> Complex(0, -1), Complex(a, 0)
    | 'L' -> Complex(0, 1), Complex(a, 0)
    | _ -> invalidArg (nameof dir) "Unexpected turn value, expected R, or L"

let startingLocation, startingDirection = Complex(0, 0), Complex(0, 1)

let input = File.ReadAllText("./input.txt")

let locations, (_, finalLocation) =
    input.Split ", "
    |> Seq.map dirToComplex
    |> Seq.mapFold
        (fun (d, acc) (r, a) ->
            let newD = d * r
            let newLocation = acc + (newD * a)
            (newLocation, (newD, newLocation)))
        (startingDirection, startingLocation)

printfn "Part 1: %A" (int (manhattan finalLocation))

let getPointsInBetween a b =
    let s = int (sign (b - a))

    Seq.unfold (fun x -> Some(x, x + s)) a
    |> Seq.takeWhile (fun x -> x <> b)


let getPointsInBetweenLine (a: Complex, b: Complex) =
    if a = b then
        Seq.empty
    elif a.Imaginary = b.Imaginary && a.Real <> b.Real then
        (getPointsInBetween (int a.Real) (int b.Real))
        |> Seq.map (fun x -> Complex(x, a.Imaginary))
    elif a.Imaginary <> b.Imaginary && a.Real = b.Real then
        (getPointsInBetween (int a.Imaginary) (int b.Imaginary))
        |> Seq.map (fun x -> Complex(a.Real, x))
    else
        invalidOp "Diagonal lines not supported"


let allLocations =
    seq {
        yield startingLocation
        yield! locations
    }


let allPoints =
    allLocations
    |> Seq.pairwise
    |> Seq.map getPointsInBetweenLine
    |> Seq.concat


// Need to use System.Collections.Generic.HashSet as it is mutable
let setVisited = HashSet()

let firstVisitedTwice =
    Seq.find (fun x -> (setVisited.Add x) = false)
    <| seq {yield! allPoints; yield finalLocation}

printfn "Part 2: %A" (int (manhattan firstVisitedTwice))
