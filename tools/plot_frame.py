import matplotlib.pyplot as plt

def plot_frame(data, *args, **kwargs):
    # aspect = kwargs.get('aspect', 'auto')
    # cmap = kwargs.get('cmap', 'seismic')
    kwargs.setdefault('cmap', 'seismic')
    kwargs.setdefault('aspect', 'auto')
    plt.imshow(
        data, 
        # cmap=cmap,
        # aspect=aspect,
        **kwargs,
    )