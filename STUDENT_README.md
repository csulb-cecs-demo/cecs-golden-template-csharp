# Student Build Guide

This project reads ten integers and prints their mean and median. It uses:

- .NET 8
- A class library in src/Library
- A console application in src/ConsoleApplication
- xUnit tests in tests/StatisticsTests

Install the [.NET 8 SDK](https://dotnet.microsoft.com/download/dotnet/8.0).
The SDK includes the dotnet command used below. These commands work in
PowerShell, Windows Command Prompt, macOS Terminal, and Linux shells.

## Build and test

From the repository root, run:

~~~text
dotnet restore
dotnet build --configuration Release --no-restore
dotnet test --configuration Release --no-build
~~~

The first restore may need an internet connection to download the xUnit
packages.

## Run the project

Run the console application with:

~~~text
dotnet run --project src/ConsoleApplication --configuration Release
~~~

Enter ten integers separated by spaces or newlines. For example:

~~~text
Enter 10 integers:
1 2 3 4 5 6 7 8 9 10
Mean: 5.5
Median: 5.5
~~~

## Run the tests

dotnet test discovers and runs all five xUnit cases in
tests/StatisticsTests.

You can run only the test project when iterating:

~~~text
dotnet test tests/StatisticsTests/StatisticsTests.csproj
~~~

If you change the project structure, update the project references in the
solution and in the affected .csproj files. Fill in VERIFICATION-LOG.md
before your final push.
