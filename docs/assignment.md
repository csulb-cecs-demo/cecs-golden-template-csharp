# Sample Assignment — Descriptive Statistics

*Instructors: replace this file with your own assignment instructions.*

## What to do

Implement the two methods in src/Library/Statistics.cs.

| Method | Returns | Input |
|---|---|---|
| Statistics.Mean(values) | arithmetic mean | a non-empty collection of integers |
| Statistics.Median(values) | middle value, or the mean of the middle two | a non-empty collection of integers |

Do not change the public method names or signatures; the xUnit tests call them
directly. Median must not modify the supplied collection.

## How you are graded

The autograder runs the same suite you can run locally:

~~~text
dotnet test --configuration Release
~~~

There are no hidden tests in this sample. What you see is what is scored.

## Before you push

Fill in VERIFICATION-LOG.md. If you used an AI tool at any point, say so and
say how you checked its output. If you did not, say that instead. An empty log
is not the same as “I did not use one.”
