import matplotlib.pyplot as plt


def plot_frame(data, *args, **kwargs):
    """
    The plot_frame function is a wrapper for the matplotlib.pyplot.imshow function, which plots an image from a 2D array of data (a frame).

    Args:
        data: Pass in the data to be plotted
        *args: Pass a non-keyworded, variable-length argument list to the function
        **kwargs: Pass in keyword arguments to the function

    Returns:
        A matplotlib
    """
    kwargs.setdefault('cmap', 'seismic')
    kwargs.setdefault('aspect', 'auto')
    return plt.imshow(
        data, 
        # cmap=cmap,
        # aspect=aspect,
        **kwargs,
    )
