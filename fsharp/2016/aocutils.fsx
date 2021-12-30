module aocutils

open System.IO

let getString (year: int) (day: int) =
    $"./../../inputs/{year}/day{day:D2}.txt"

let getInput (year: int) (day: int) =
    File.ReadAllText($"./../../../inputs/{year}/day{day:D2}.txt")
