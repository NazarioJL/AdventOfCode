open System
open System.IO


let isTriangle (a: int, b: int, c: int) : bool =
    let sorted =
        seq {
            a
            b
            c
        }
        |> Seq.sort
        |> Seq.toList

    sorted.[0] + sorted.[1] > sorted.[2]

let input =
    File.ReadAllText("../../../inputs/2016/day03.txt")

let parseInput (inputStr: string) =
    inputStr.Split("\n")
    |> Seq.filter (fun x -> not (x |> String.IsNullOrEmpty))
    |> Seq.map (fun x ->
        let parts =
            x.Split(
                " ",
                StringSplitOptions.RemoveEmptyEntries
                ||| StringSplitOptions.TrimEntries
            )

        parts
        |> Seq.map Int32.Parse
        |> Seq.toArray
        |> fun arr -> arr.[0], arr.[1], arr.[2])

let part1 =
    input
    |> parseInput
    |> Seq.filter isTriangle
    |> Seq.length

printfn "Solution part 1: %A" part1

let transpose3 (triple: (int * int * int) []) =
    let a, b, c = triple.[0]
    let d, e, f = triple.[1]
    let g, h, i = triple.[2]

    seq {
        (a, d, g)
        (b, e, h)
        (c, f, i)
    }

let transformInput (triples: seq<int * int * int>) =
    triples
    |> Seq.chunkBySize 3
    |> Seq.map transpose3
    |> Seq.concat

let part2 =
    input
    |> parseInput
    |> transformInput
    |> Seq.filter isTriangle
    |> Seq.length

printfn "Solution part 2: %A" part2
