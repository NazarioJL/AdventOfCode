open System
open System.IO

type Direction =
    | Up = 'U'
    | Left = 'L'
    | Down = 'D'
    | Right = 'R'

let CharToDirection =
    Map [ ('U', Direction.Up)
          ('L', Direction.Left)
          ('D', Direction.Down)
          ('R', Direction.Right) ]

let KeyMapPart1 =
    Map [ (1,
           Map [ (Direction.Up, 1)
                 (Direction.Left, 1)
                 (Direction.Down, 4)
                 (Direction.Right, 2) ])
          (2,
           Map [ (Direction.Up, 2)
                 (Direction.Left, 1)
                 (Direction.Down, 5)
                 (Direction.Right, 3) ])
          (3,
           Map [ (Direction.Up, 3)
                 (Direction.Left, 2)
                 (Direction.Down, 6)
                 (Direction.Right, 3) ])
          (4,
           Map [ (Direction.Up, 1)
                 (Direction.Left, 4)
                 (Direction.Down, 7)
                 (Direction.Right, 5) ])
          (5,
           Map [ (Direction.Up, 2)
                 (Direction.Left, 4)
                 (Direction.Down, 8)
                 (Direction.Right, 6) ])
          (6,
           Map [ (Direction.Up, 3)
                 (Direction.Left, 5)
                 (Direction.Down, 9)
                 (Direction.Right, 6) ])
          (7,
           Map [ (Direction.Up, 4)
                 (Direction.Left, 7)
                 (Direction.Down, 7)
                 (Direction.Right, 8) ])
          (8,
           Map [ (Direction.Up, 5)
                 (Direction.Left, 7)
                 (Direction.Down, 8)
                 (Direction.Right, 9) ])
          (9,
           Map [ (Direction.Up, 6)
                 (Direction.Left, 8)
                 (Direction.Down, 9)
                 (Direction.Right, 9) ]) ]


let KeyMapPart2 =
    Map [ (1,
           Map [ (Direction.Up, 1)
                 (Direction.Left, 1)
                 (Direction.Down, 3)
                 (Direction.Right, 1) ])
          (2,
           Map [ (Direction.Up, 2)
                 (Direction.Left, 2)
                 (Direction.Down, 6)
                 (Direction.Right, 3) ])
          (3,
           Map [ (Direction.Up, 1)
                 (Direction.Left, 2)
                 (Direction.Down, 7)
                 (Direction.Right, 4) ])
          (4,
           Map [ (Direction.Up, 4)
                 (Direction.Left, 3)
                 (Direction.Down, 8)
                 (Direction.Right, 4) ])
          (5,
           Map [ (Direction.Up, 5)
                 (Direction.Left, 5)
                 (Direction.Down, 5)
                 (Direction.Right, 6) ])
          (6,
           Map [ (Direction.Up, 2)
                 (Direction.Left, 5)
                 (Direction.Down, 0xA)
                 (Direction.Right, 7) ])
          (7,
           Map [ (Direction.Up, 3)
                 (Direction.Left, 6)
                 (Direction.Down, 0xB)
                 (Direction.Right, 8) ])
          (8,
           Map [ (Direction.Up, 4)
                 (Direction.Left, 7)
                 (Direction.Down, 0xC)
                 (Direction.Right, 9) ])
          (9,
           Map [ (Direction.Up, 9)
                 (Direction.Left, 8)
                 (Direction.Down, 9)
                 (Direction.Right, 9) ])
          (0xA,
           Map [ (Direction.Up, 6)
                 (Direction.Left, 0xA)
                 (Direction.Down, 0xA)
                 (Direction.Right, 0xB) ])
          (0xB,
           Map [ (Direction.Up, 7)
                 (Direction.Left, 0xA)
                 (Direction.Down, 0xD)
                 (Direction.Right, 0xC) ])
                 
          (0xC,
           Map [ (Direction.Up, 8)
                 (Direction.Left, 0xB)
                 (Direction.Down, 0xC)
                 (Direction.Right, 0xC) ])
          (0xD,
           Map [ (Direction.Up, 0xB)
                 (Direction.Left, 0xD)
                 (Direction.Down, 0xD)
                 (Direction.Right, 0xD) ]) ]

let input = File.ReadAllText("./input.txt")

let parseInput (s: string) =
    s.Split("\n")
    |> Seq.filter (fun x -> x.Length > 0)

let makeGetKeyFun (keyMap: Map<int, Map<Direction,int>>) =
    fun (s: string) (k: int) -> 
        s.ToCharArray()
        |> Seq.map (fun c -> CharToDirection.[c])
        |> Seq.fold (fun a e -> keyMap.[a].[e]) k


let getCode (inputStr: string) (keyMap: Map<int, Map<Direction,int>>): string =
    let getKeyFun = makeGetKeyFun keyMap
    input
    |> parseInput
    |> Seq.fold
        (fun acc e ->
            seq {
                yield! acc
                yield (getKeyFun e (Seq.last acc))
            })
        (Seq.singleton 5)
    |> Seq.skip 1
    |> Seq.map (fun x -> x.ToString("X"))
    |> String.concat ""


printfn "Part 1: %A" (getCode input KeyMapPart1)
printfn "Part 2: %A" (getCode input KeyMapPart2)
