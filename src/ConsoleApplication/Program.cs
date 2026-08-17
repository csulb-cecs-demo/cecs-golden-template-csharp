using System.Globalization;
using Library;

internal static class Program
{
    private const int NumberOfValues = 10;

    public static int Main()
    {
        Console.WriteLine("Enter 10 integers:");

        List<int> data = new(NumberOfValues);

        while (data.Count < NumberOfValues && Console.ReadLine() is { } line)
        {
            string[] tokens = line.Split(
                (char[]?)null,
                StringSplitOptions.RemoveEmptyEntries);

            foreach (string token in tokens)
            {
                if (!int.TryParse(
                        token,
                        NumberStyles.Integer,
                        CultureInfo.InvariantCulture,
                        out int value))
                {
                    Console.Error.WriteLine("Invalid input. Please enter 10 integers.");
                    return 1;
                }

                data.Add(value);
                if (data.Count == NumberOfValues)
                {
                    break;
                }
            }
        }

        if (data.Count != NumberOfValues)
        {
            Console.Error.WriteLine("Invalid input. Please enter 10 integers.");
            return 1;
        }

        Console.WriteLine(
            $"Mean: {Statistics.Mean(data).ToString(CultureInfo.InvariantCulture)}");
        Console.WriteLine(
            $"Median: {Statistics.Median(data).ToString(CultureInfo.InvariantCulture)}");

        return 0;
    }
}
