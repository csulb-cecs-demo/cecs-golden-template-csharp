using Library;

namespace StatisticsTests;

public class StatisticsTests
{
    [Fact]
    public void MeanFindsMeanOfConsecutiveValues()
    {
        int[] data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

        Assert.Equal(5.5, Statistics.Mean(data));
    }

    [Fact]
    public void MeanFindsMeanWithNegativeValues()
    {
        int[] data = [-10, -8, -6, -4, -2, 2, 4, 6, 8, 10];

        Assert.Equal(0.0, Statistics.Mean(data));
    }

    [Fact]
    public void MedianFindsMedianOfUnsortedValues()
    {
        int[] data = [10, 2, 8, 4, 6, 1, 9, 3, 7, 5];

        Assert.Equal(5.5, Statistics.Median(data));
    }

    [Fact]
    public void MedianFindsMedianWithRepeatedValues()
    {
        int[] data = [8, 3, 3, 1, 8, 3, 5, 3, 9, 3];

        Assert.Equal(3.0, Statistics.Median(data));
    }

    [Fact]
    public void MedianDoesNotChangeTheInputArray()
    {
        int[] data = [10, 2, 8, 4, 6, 1, 9, 3, 7, 5];
        int[] originalData = (int[])data.Clone();

        _ = Statistics.Median(data);

        Assert.Equal(originalData, data);
    }
}
