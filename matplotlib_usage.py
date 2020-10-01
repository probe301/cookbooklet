

=======================
# easy plot settings
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline
plt.rcParams['figure.figsize'] = (10.0, 8.0) # set default size of plots
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'


====================
# matplotlib common
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline
plt.rcParams['figure.figsize'] = (10.0, 8.0) # set default size of plots
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

# multiple plot
ax = plt.subplot(2, 1, 2)
plt.plot(hist.history['acc'], '-o')
plt.plot(hist.history['val_acc'], '-o')
plt.legend(['train', 'val'], loc='upper left')
plt.xlabel('epoch')
plt.ylabel('accuracy')
ax.set_ylim([0, 1])  # this is ax not plt

# multiple plot in grid m*n
f, plots = plt.subplots(21, 10, sharex='all', sharey='all', figsize=(10, 21))
for i in range(203):
    plots[i // 10, i % 10].axis('off')
    plots[i // 10, i % 10].imshow(pat[i], cmap=plt.cm.bone)


# span plot 而且 index 从 0 计数的, 更符合直觉
ax4 = plt.subplot2grid((2,3), (1,0), colspan=2)
