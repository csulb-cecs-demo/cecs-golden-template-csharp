namespace Library;

/// <summary>
/// Descriptive statistics functions used by the console demonstration.
/// </summary>
public static class Statistics
{
    /// <summary>
    /// Calculates the arithmetic mean of the supplied values.
    /// </summary>
    public static double Mean(IReadOnlyList<int> data)
    {
        ArgumentNullException.ThrowIfNull(data);

        if (data.Count == 0)
        {
            throw new ArgumentException("At least one value is required.", nameof(data));
        }

        double sum = 0.0;
        foreach (int value in data)
        {
            sum += value;
        }

        return sum / data.Count;
    }

    /// <summary>
    /// Calculates the median without changing the input collection.
    /// </summary>
    public static double Median(IReadOnlyList<int> data)
    {
        ArgumentNullException.ThrowIfNull(data);

        if (data.Count == 0)
        {
            throw new ArgumentException("At least one value is required.", nameof(data));
        }

        int[] sortedData = data.ToArray();
        Array.Sort(sortedData);

        int middle = sortedData.Length / 2;
        if (sortedData.Length % 2 == 1)
        {
            return sortedData[middle];
        }

        return (sortedData[middle - 1] + (double)sortedData[middle]) / 2.0;
    }
}
