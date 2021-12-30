# fsharp

This folder contains any solutions developed in the [`fsharp`](https://fsharp.org/) language.

## How to run

Currently these solutions use fsharp interactive files that run from the command line using `.NET Core`. To run a file simple execute:

```sh
dotnet fsi solution.fsx
```

Currently the structure is organized like so:

```text
├── 2016
│   ├── day01
│   │   ├── input.txt
│   │   └── solution.fsx
│   ├── day02
│   │   ├── input.txt
│   │   └── solution.fsx
...
│   └── day[n]
│       ├── input.txt
│       └── solution.fsx
└── README.md
```

I may move to something more idiomatic for gathering benchmarking, integrating testing and any other useful features. The end goal is to templatize structures per programming language and a way to run a solution by:

- mode _e.g._ `fsharp`, `python`, `Java`, `custom1`, etc...
- year
- part
- variant

You can imagine running any solution like so:

```sh
./run.sh python 2021 24  # defaults first (or only) variant
./run.sh 2021 24  # defaults to a language
```
