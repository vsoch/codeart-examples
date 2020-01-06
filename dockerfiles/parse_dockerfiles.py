#!/usr/bin/env python

from codeart.main import CodeBase
import os

# Sitting where you want root of analysis to be
code = CodeBase()

# Cloned on my computer
# git clone https://github.com/vsoch/dockerfiles

# Let's write a custom function to derive a group name. A return of None/False
# means we will skip adding a file
def is_dockerfile(filename):
    if filename.endswith("Dockerfile"):
        return "dockerfile"

code.add_folder("/home/vanessa/Documents/Dropbox/Code/database/dockerfiles/data", func=is_dockerfile)

# Look at extractors, one added per extension
code.codefiles
# {'dockerfile': [codeart-files:98904]}

# We only have one group, so only need to do one train.
code.train() 

# extract vectors for an extension (pandas dataframe, words in rows)
# normalized to RGB color space
vectors = code.get_vectors("dockerfile")
vectors.shape # (9623, 3)

# Derive counts (should be same as total since we just have one file type)
groups = code.get_groups()
counts = code.get_color_percentages(groups, vectors)

# Save vectors gradients and counts, along with word2vec model
counts.to_csv("color-percentages.csv")
vectors.to_csv("vectors-gradients.csv")
code.save_model(outdir=os.getcwd(), group="dockerfile")

# Generate a vector gradient
from codeart.graphics import save_vectors_gradient_grid
save_vectors_gradient_grid(vectors=vectors, outfile="colors-gradient.png")

# Save interactive colormap (default is now sorted)
from codeart.graphics import generate_interactive_colormap
for folder in ['web', 'sorted']:
    os.mkdir(folder)

generate_interactive_colormap(vectors=vectors, counts=counts, outdir="web")
