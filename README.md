# ColorArt Examples

This is an examples repository to supplement [codeart](https://github.com/vsoch/codeart).
The repository was getting large so I decided to move image and data files over here.

## Dockerfiles

The Dockerfiles [dinosaur dataset](https://github.com/vsoch/dockerfiles) has about 100K Dockerfiles, 
and this small example shows creating visualizations for them. The [interactive version](https://vsoch.github.io/codeart-examples/dockerfiles/web/) isnt' very useful here because we only have one file type, and the range of colors
is limited from greens to blues. This project helped to develop the [sorted interactive version](https://vsoch.github.io/codeart-examples/dockerfiles/sorted/) of the colormap.

## Parse Repo

The [parse_repo](parse_repo) folder shows how to parse a repository (spack)
and then generate a color gradient lookup. The first attempt at the color grid
[can be seen here](https://vsoch.github.io/codeart-examples/parse_repo/web/)
and this was updated to better organize, [seen here](https://vsoch.github.io/codeart-examples/parse_repo/sorted/).
For the second, since the Word2Vec model derives similar embeddings represented in color,
this means that similar colors equate to similar terms. You can explore the visualization
with this knowledge.

Finally, to generate a custom codeart image (with text), the library can
also do that, with an [example here](https://vsoch.github.io/codeart-examples/parse_repo/text.html)
and shown below.

![parse_repo/text.png](parse_repo/text.png)


And of course it would be more appropriate to write the name of the software as the
[text instead](https://vsoch.github.io/codeart-examples/parse_repo/spack.html)!

![parse_repo/spack-text.png](parse_repo/spack-text.png)

and of course you have to zoom in to see that the pixels are actually code, colored
based on their context thanks to Word2Vec.


## Parse by Year

Is an example project to use codeart to parse a large Python code base, determine
year of creation using the GitHub api, and then break into groups based on the year.
This small project helped me to develop the interactive colomap example, which
you can view [here](https://vsoch.github.io/codeart-examples/parse_by_year/web) or
the previous version (not sorted) [here](https://vsoch.github.io/codeart-examples/parse_by_year/web-unsorted/)

The example also generates static images, along with a gif (animation) to
show the change in data over time.

![colormap-groups.gif](parse_by_year/colormap-groups.gif)

Of course this was impossible to explore, hence why I made the interactive version.

## Derive Colormap

The [derive_colormap](derive_colormap) folder an example to show working on deriving a colormap from a set of embeddings. 
This means that we start with 3d, project to 2d, and then use Voronoi to
fill border cells. Here is the original 3d map:

![derive_colormap/colormap-3d.png](derive_colormap/colormap-3d.png)

which we then project to 2d

![derive_colormap/colormap-2d.png](derive_colormap/colormap-2d.png)

And then the Voronoi exercise didn't work out as intended (and I pursued other methods
instead)

![derive_colormap/sploosh.png](derive_colormap/sploosh.png)

And ultimately wound up developing an interactive colormap (too large to add to the 
repo here!) that is better sorted by rows and columns (and generates in a reasonable time).
Note that since this is for all of my Python code, the interface is a bit clunky.
Probably something with canvas would work better here for this number of points.
The notebook is useful to get someone started with a similar project.

## Parse Folders

The [parse_folders](parse_folders) is a similar effort to "Parse Repo" above,
but instead we parse folders on our local file system and generate a colors
gradient. This is the color gradient across all extensions for the model:

![parse_folders/colors-gradient.png](parse_folders/colors-gradient.png)

Or instead, you can generate an [interactive version](https://vsoch.github.io/codeart-examples/parse_repo/web/)
that allows for mousing over colors to see terms, and clicking on the list
of extensions to see relevant terms. The opacity corresponds to the relative
count of the term for the extension. For spack, most terms will be derived
from Python files.

### Interactive

The [interactive version](https://vsoch.github.io/codeart-examples/parse_repo/web/) shows the interactive color grid, where groups (in this case extensions) are colored based on salience. Click an extension to see relevant terms in the embeddings model.

### Abstract
The abstract versions, including those for [no extension](https://vsoch.github.io/codeart-examples/parse_repo/spack/codeart.html), [python](https://vsoch.github.io/codeart-examples/parse_repo/spack/codeart.py.html) and [patch](https://vsoch.github.io/codeart-examples/parse_repo/spack/codeart.patch.html) files are graphics generated with pictures of the code themself.
