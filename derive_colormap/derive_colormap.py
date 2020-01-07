#!/usr/bin/env python3

# Derive a colormap (and generate into an animation) to show file prevalence
# across a codebase. This is a derivative of derive_colormap.ipynb

import pandas
import numpy
import matplotlib.pyplot as plt
from codeart.main import CodeBase
from sklearn import decomposition

root = "/home/vanessa/Documents/Dropbox/Code"
code = CodeBase()
code.add_folder(root)

# We have a ton of codefiles (extensions)!
code.codefiles
len(code.codefiles)  # 2311

# How many extensions have >100 files?
len(code.threshold_files(100))  # 199

# let's filter this down to just programming languages and configuration files.
# I'm also removing data files like tsv, csv, json, but not markdown, rst, etc.

extensions = [
    ".c",
    "",
    ".md",
    ".cpp",
    ".sh",
    ".html",
    ".patch",
    ".rst",
    ".txt",
    ".h",
    ".conf",
    ".yml",
    ".pl",
    ".pm",
    ".sql",
    ".py",
    ".yaml",
    ".cwl",
    ".js",
    ".xml",
    ".svg",
    ".css",
    ".ini",
    ".par",
    ".mod",
    ".toml",
    ".go",
    ".bat",
    ".plist",
    ".tmpl",
    ".rb",
    ".rs",
    ".coffee",
    ".r",
    ".job",
    ".template",
    ".properties",
    ".doctree",
    ".in",
    ".tex",
    ".rake",
    ".erb",
    ".cfg",
    ".f90",
    ".cc",
    ".m",
    ".php",
    ".es6",
    ".config",
    ".styl",
    ".ts",
    ".def",
    ".info",
    ".mk",
    ".as",
    ".gitignore",
    ".java",
    ".class",
    ".cmake",
    ".cs",
    ".tcl",
    ".bazel",
    ".crl",
    ".proto",
    ".jade",
    ".hpp",
    ".eps",
    ".sub",
    ".wdl",
    ".scala",
]


# train single model for some subset of extensions (could also choose thresh=100)
code.train_all(extensions)

# extract vectors for an extension (pandas dataframe, words in rows)
# normalized to RGB color space
vectors = code.get_vectors("all")
vectors.shape # (178494, 3)

# prepare to visualize for each language in 2d
pca = decomposition.PCA(n_components=2)
pca.fit(vectors)
data = pca.transform(vectors)

# Generate the 2d lookup for the image
plt.scatter(data[:, 0], data[:, 1], c=vectors[[0, 1, 2]].to_numpy() / 255)
plt.axis("off")
plt.savefig("img/colormap-2d-example.png")

# Calculate color percentages
counts = code.get_color_percentages(extensions, vectors)

counts.to_csv("colormap-counts-all.csv")
vectors.to_csv("colormap-vectors-all.csv")

code.save_all(os.getcwd())

# generate graphic using counts and vectors
from codeart.graphics import generate_interactive_colormap

# let's only choose top extensions
groups = list(code.threshold_files(10).keys())
vectors = code.get_vectors('all')
counts = code.get_color_percentages(groups=groups, vectors=vectors)

vectors.to_csv("spack-colormap-vectors.csv")
counts.to_csv("spack-color-percentages.csv")

# !mkdir -p web
generate_interactive_colormap(vectors=vectors, counts=counts, outdir="web")
