#!/usr/bin/env python

# This example will show how to build a model for a repository. Specifically,
# we choose a Python repository (a large one!) and then build a model for
# all file extensions with > 100 files. We will show generating raw images
# (data for your use) along with a web gallery for each extension (using
# the same model)

from codeart.main import CodeBase
from glob import glob
import os

code = CodeBase()
code.add_repo("https://github.com/spack/spack")

# Look at extractors, one added per extension
# code.codefiles


###
## Example 1: Generate Raw Data
###

# You likely want to chose those above a certain threshold.
# Here we look at extensions with >= 100 files. If you get an error during
# training, it's because the size of the vocabularity isn't big enough due
# to too few files, so choose your extension threshold generously.

code.threshold_files(thresh=20)
#{'.yaml': [codeart-files:47],
# '.py': [codeart-files:4225],
# '.rst': [codeart-files:42],
# '.txt': [codeart-files:24],
# '.sh': [codeart-files:38],
# '.patch': [codeart-files:530]}

# Let's train a word2vec model, size 3 for RGB space, for each of those extensions
code.train(groups=[".py", ".patch"])

# We can also train a single model for some set of extensions
code.train_all(groups=[".py", ".patch", ".txt"])

# Or just train for all extensions
code.train_all()

# We now have a model for each extension (and all)
code.models
code.models["all"]

# First let's just generate vectors (RGB values across words in each model) for each language
# This is a pandas data frame you can easily save to csv, pickle, etc.
vectors = code.get_vectors(".py")

###
## Example 2: Generate a Plot
###

# Here is an simple visualization example using Matplotlib.
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(
    vectors[0].tolist(),
    vectors[1].tolist(),
    vectors[2].tolist(),
    c=vectors.to_numpy() / 255,
)

# If you want to add text
# for row in vectors.iterrows():
#    ax.text(row[1][0], row[1][1], row[1][2], row[0])

plt.savefig("spack-python.png")


###
## Example 3.A: Generate Code Art Tree
###

vectors = code.get_vectors('all')
code.make_tree(group="all", vectors=vectors, outdir=os.getcwd(), outfile="tree.html")

# outputs tree.html and data.json, and images folder

###
## Example 3.B: Generate Code Images
###

# The same images as above, but without the data.json and tree.html
# (intended for your own development)

# Generate images for all files
if not os.path.exists("images"):
    os.mkdir("images")

# Create folder of code images (if you want to work with them directly)
code.make_art(group=".py", outdir="images", vectors=vectors)


###
## Example 4: Generate A Gallery
###


# The gallery example here will plot each language, using the same model

images = glob("images/*png")
groups = list(code.threshold_files(20).keys())
make_gallery(groups=groups, images=images, outdir=os.getcwd())

###
## Example 5: Generate Interactive Web Interface
###

from codeart.graphics import generate_interactive_colormap

# let's only choose top extensions (moreso than last time)
groups = list(code.threshold_files(10).keys())
vectors = code.get_vectors('all')
counts = code.get_color_percentages(groups=groups, vectors=vectors)

vectors.to_csv("spack-colormap-vectors.csv")
counts.to_csv("spack-color-percentages.csv")

# !mkdir -p web
from codeart.graphics import generate_interactive_colormap
generate_interactive_colormap(vectors=vectors, counts=counts, outdir="web")

# Output files are in web

###
## Example 6: Use images to generate a true "code art"
###

from codeart.colors import generate_color_lookup
images = glob("images/*")
color_lookup = generate_color_lookup(images)

# Write to index.html, images are relative to this folder
# This function will only work well with codefiles of uniform colors
from codeart.graphics import generate_codeart
generate_codeart('sunset.jpg', color_lookup, sample=10, top=100, outfile="index.html")

# Generate an image with text (dinosaur!)
from codeart.graphics import generate_codeart_text
generate_codeart_text('dinosaur', color_lookup, outfile="text.html")
generate_codeart_text('spack', color_lookup, outfile="spack.html", font_size=100, width=1200)
