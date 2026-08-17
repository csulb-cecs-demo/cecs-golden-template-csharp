# CECS Golden Template — C# Project with xUnit Tests

A small .NET console program reads ten integers and prints their mean and
median. The repository is organized as a reusable class library, a console
application, and one xUnit test library.

> [!NOTE]
> Files in this repo carry 'FACULTY:' comments explaining why each piece is the
> way it is. They are written for whoever adapts this next. Students can ignore
> them, and you can strip them once your own version settles.

## Layout

| Path | What goes here |
|---|---|
| src/Library/ | Statistics.Mean and Statistics.Median. |
| src/ConsoleApplication/ | The console application that reads and reports ten integers. |
| tests/StatisticsTests/ | The xUnit test suite for the library. |
| docs/ | Assignment and faculty guidance. |
| VERIFICATION-LOG.md | Required record of verification and AI assistance. |
| .github/workflows/ci.yml | Builds the solution and runs the tests on every push. |

## Start here

Install the [.NET 8 SDK](https://dotnet.microsoft.com/download/dotnet/8.0),
then run these commands from the repository root:

~~~text
dotnet restore
dotnet build --configuration Release --no-restore
dotnet test --configuration Release --no-build
~~~

Run the demonstration with:

~~~text
dotnet run --project src/ConsoleApplication --configuration Release
~~~

Example:

~~~text
Enter 10 integers:
1 2 3 4 5 6 7 8 9 10
Mean: 5.5
Median: 5.5
~~~

## For students

Implement or adapt the functions in src/Library/Statistics.cs, keep the
public API used by the tests, and run dotnet test before pushing. Fill in
VERIFICATION-LOG.md before submitting.

## For instructors

The xUnit suite is intentionally small and visible. Replace the sample
assignment and tests with course-specific work while keeping the same
solution shape. Before handing an assignment to students, submit one
deliberately wrong solution and confirm that the test workflow turns red.

The repository also includes the language-neutral
[getting-started](docs/getting-started.md), [testing](docs/writing-tests.md),
[troubleshooting](docs/troubleshooting.md), and
[governance](docs/governance.md) guides.

## License

[MIT](LICENSE)
