#!/usr/bin/env python3

# Derive a colormap (and generate into an animation) to show file prevalence
# across a codebase. This is a derivative of derive_colormap.ipynb
from codeart.main import CodeBase

# Import (or write) a function that takes a filename, and returns a group name
from codeart.utils import group_by_year_created

# Let's look at the change in Python code (and associated files) over time
root = "/home/vanessa/Documents/Dropbox/Code/Python"
code = CodeBase()
code.add_folder(root, func=group_by_year_created)

# What years did we capture?
# {2018: [codeart-files:94536],
# 2019: [codeart-files:9654],
# 2020: [codeart-files:101]}

# This doesn't capture what I intended - I want to know when I wrote the scripts,
# not when they were downloaded from online to my computer. Let's instead write a custom function.
# We will loop through folders, and for each one, look for a git folder.
# If we find it, we'll use the GitHub API to get an actual created date!
from codeart.utils import resursive_find_repos, write_json
import requests

metadata = dict()

api_base = "https://api.github.com"

# Make sure to export a GitHub token, likely you will need more than 60 requests
# https://developer.github.com/v3/#rate-limiting
headers = {"Authorization": "token %s" % os.environ.get("GITHUB_TOKEN")}
for repo in recursive_find_repos(folder):

    if repo in metadata:
        continue

    reponame = "/".join(repo.split("/")[-2:])
    url = "%s/repos/%s" % (api_base, reponame)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        metadata[repo] = data
    else:
        print("Error with %s" % repo)


# Save metadata to flie
write_json(metadata, "metadata.json")
code = CodeBase()

# For each repo, parse based on date created
# We could technically use code.add_repo(repo, group=year) to add fresh,
# but it will be easier to parse folders that we do have.
for repo, repo_folder in recursive_find_repos(root, return_folders=True).items():
    if repo in metadata:
        print("Adding %s" % repo_folder)
        data = metadata[repo]
        year = data["created_at"].split("-")[0]
        code.add_folder(repo_folder, group=year)


# Now we have a nice span of the decade!
code.codefiles
# {'2011': [codeart-files:24],
# '2014': [codeart-files:758],
# '2015': [codeart-files:9421],
# '2018': [codeart-files:1538],
# '2013': [codeart-files:535],
# '2019': [codeart-files:7043],
# '2017': [codeart-files:3545],
# '2016': [codeart-files:77982],
# '2012': [codeart-files:26]}

# Train a model for all years
code.train_all()

# extract vectors for all combined (to create colormap)
# normalized to RGB color space
vectors = code.get_vectors("all")
vectors.shape  # (48538, 3)

# Save the entire colormap (with words associated with each image), across languages
from codeart.graphics import save_vectors_gradient_grid
save_vectors_gradient_grid(vectors=vectors[[0,1,2]], width=6000, outfile='color-grid.png')

# prepare to visualize for each language in 2d
from sklearn import decomposition
from matplotlib.pylab import plt
pca = decomposition.PCA(n_components=2)
pca.fit(vectors)
data = pca.transform(vectors)

vectors["x_dim"] = data[:, 0]
vectors["y_dim"] = data[:, 1]

# Calculate color percentages
groups = code.get_groups()
groups.sort()
counts = code.get_color_percentages(groups, vectors)

# Save to file
vectors.to_csv("color-vectors.csv")
counts.to_csv("color-percentages.csv")

# Generate 2d plot of all colors
plt.figure(figsize=(20, 12))
plt.scatter(vectors["x_dim"], vectors["y_dim"], c=vectors[[0, 1, 2]].to_numpy() / 255)
plt.title("CodeArt Color Map, All Groups")
plt.axis("off")
plt.savefig("colormap-2d.png")

# We'll also save a gif
import imageio
images = []

# Generate a plot for each color
for group in groups:
    colors = vectors[[0, 1, 2]] / 255

    # Alpha layer (between 0 and 1 for matplotlib) based on year
    colors['alphas'] = counts.loc[:, "%s-percent" % group].tolist()

    plt.figure(figsize=(20, 12))
    plt.scatter(vectors["x_dim"], vectors["y_dim"], c=colors.to_numpy())
    plt.title("CodeArt Color Map for group %s" % group)
    plt.axis("off")
    plt.savefig("colormap-%s.png" % group)
    images.append("colormap-%s.png" % group)
    plt.close()

# Sort by date
images.sort()

# Write a gif, make sure there is a delay long enough to inspect
with imageio.get_writer("colormap-groups.gif", mode="I", duration=2) as writer:
    while images:
        pngfile = images.pop()
        writer.append_data(imageio.imread(pngfile))

# This is okay, but it doesn't really let me explore the data. Let's export
# for d3. We'll combine the colors and vectors to export data
# ! mkdir -p web
from codeart.graphics import generate_interactive_colormap
generate_interactive_colormap(vectors=vectors[[0,1,2]], counts=counts, outdir="web")
