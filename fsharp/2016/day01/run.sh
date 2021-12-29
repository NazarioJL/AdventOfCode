if ! [ -x "$(command -v dotnet)" ]; then
    echo "dotnet is required for this to run"
    exit 1
fi

dotnet fsi solution.fsx
